#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# multiply_uv.py
#
# Аналог оригинального 010 Editor скрипта "UpscaleDAT":
# для каждого WorldModel каждого BSP умножает
#   Surfaces[i].UV2.{x,y,z} *= ScaleFactor
#   Surfaces[i].UV3.{x,y,z} *= ScaleFactor
#
# Использование:
#   python multiply_uv.py <scale> <file1.dat> [file2.dat ...] [-o <out_dir>]
#
# Пример:
#   python multiply_uv.py 2.0 map.dat -o out/
#   python multiply_uv.py 4.0 *.dat -o fixed/

import argparse
import os
import struct
import sys


def u16(d, p): return struct.unpack_from("<H", d, p)[0]
def i16(d, p): return struct.unpack_from("<h", d, p)[0]
def u32(d, p): return struct.unpack_from("<I", d, p)[0]
def i32(d, p): return struct.unpack_from("<i", d, p)[0]


def read_ltstring(d, p):
    """LTString: short Length; char Value[Length]; Возвращает новую позицию."""
    length = i16(d, p)
    p += 2
    if length > 0:
        p += length
    return p


def skip_subdivision(d, p):
    """Эмуляция read_layout() из шаблона."""
    current_byte = 0
    current_bit = 8

    def read_layout(depth):
        nonlocal p, current_byte, current_bit

        if current_bit == 8:
            current_byte = d[p]
            p += 1
            current_bit = 0

        subdivide = (current_byte & (1 << current_bit)) != 0
        current_bit += 1

        if depth > 16:
            return

        if subdivide:
            for _ in range(4):
                read_layout(depth + 1)

    read_layout(0)
    return p


def skip_leaf(d, p):
    leaf_list_count = u16(d, p)
    p += 2

    if leaf_list_count == 0xFFFF:
        p += 2  # ushort LeafListIndex
    else:
        for _ in range(leaf_list_count):
            p += 2  # short PortalID
            size = u16(d, p)
            p += 2
            p += size

    poly_count = i32(d, p)
    p += 4
    if poly_count > 0:
        p += poly_count * 4

    p += 4  # int Unk1
    return p


def skip_surface(d, p):
    """Skip a Surface, return end position."""
    p += 12 * 3   # UV1, UV2, UV3
    p += 2        # ushort Texture
    p += 4        # int Unk1
    p += 4        # int Flags
    p += 4        # uchar Unk2[4]

    use_effects = d[p]
    p += 1

    if use_effects > 0:
        p = read_ltstring(d, p)  # Effect
        p = read_ltstring(d, p)  # EffectParam

    p += 2  # ushort TextureFlags
    return p


def skip_polygon(d, p, vertex_info):
    count, extra = vertex_info
    p += 12 + 2 + 2  # Center + LightmapWidth + LightmapHeight

    unknown = i16(d, p)
    p += 2
    if unknown > 0:
        p += unknown * 4  # short MoreUnknown[Unknown * 2]

    p += 2 + 2  # SurfaceIndex + PlaneIndex
    p += (count + extra) * 5  # DiskVert Verts[Count+Extra]
    return p


def find_surfaces(d):
    """Возвращает список offset-ов начала каждой Surface во всём файле."""
    if len(d) < 44:
        raise ValueError("Файл слишком маленький для WorldHeader")

    version = u32(d, 0)
    if version != 66:
        print(f"WARNING: Version = {version}, ожидался 66", file=sys.stderr)

    p = 44  # WorldHeader = 4 + 4 + 4 + 8*4 = 44

    # WorldInfo
    info_length = u32(d, p)
    p += 4 + info_length
    p += 4          # float LMGridSize
    p += 12 + 12    # BoundaryMin, BoundaryMax

    # WorldTree
    p += 32

    # subdivision_data
    p = skip_subdivision(d, p)

    # WorldModelHeader
    model_count = i32(d, p)
    p += 4

    all_surfaces = []
    current = p

    for _ in range(model_count):
        model_start = current
        next_world_item = i32(d, model_start)

        bsp_start = model_start + 4 + 32  # NextWorldItem + Padding2[32]
        q = bsp_start

        q += 4 + 4                     # InfoFlags, Unknown
        q = read_ltstring(d, q)        # WorldName

        (point_count, plane_count, surface_count, user_portal_count,
         poly_count, leaf_count, vert_count, total_vis, leaf_list,
         node_count) = struct.unpack_from("<10i", d, q)
        q += 40

        q += 4 + 4   # Unknown2, Unknown3
        q += 12 * 3  # MinBox, MaxBox, WorldTranslation

        texture_name_length = i32(d, q)
        texture_count      = i32(d, q + 4)
        q += 8

        q += texture_name_length

        vertices = []
        for _ in range(poly_count):
            vertices.append((d[q], d[q + 1]))
            q += 2

        if leaf_count > 0:
            for _ in range(leaf_count):
                q = skip_leaf(d, q)

        q += plane_count * 16  # Plane

        # === Собственно Surfaces ===
        for _ in range(surface_count):
            all_surfaces.append(q)
            q = skip_surface(d, q)

        for i in range(poly_count):
            q = skip_polygon(d, q, vertices[i])

        if node_count > 0:
            q += node_count * 14  # Node

        if user_portal_count > 0:
            for _ in range(user_portal_count):
                q = read_ltstring(d, q)  # Name
                q += 4 + 2 + 12 + 12     # Unk1, Unk2, Center, Dims

        q += point_count * 24  # Point

        grid_x = i32(d, q)
        grid_y = i32(d, q + 4)
        grid_z = i32(d, q + 8)
        q += 12

        block_count = grid_x * grid_y * grid_z

        q += 12 + 12  # BoundsMax, BoundsMin

        if block_count > 0:
            for _ in range(block_count):
                size = u16(d, q)
                q += 4 + size * 6  # Size + Max + Contents[Size]

        q += 4  # RootNodeIndex
        sections = i32(d, q)
        q += 4

        if sections > 0 and 0 < next_world_item <= len(d):
            current = next_world_item
        else:
            current = q  # = BSP end

    return all_surfaces


def process_file(in_path, out_path, scale):
    with open(in_path, "rb") as f:
        data = bytearray(f.read())

    surfaces = find_surfaces(data)

    # UV2 = start+12, UV3 = start+24. Компоненты: x, y, z = +0, +4, +8
    uv_offsets = (12, 16, 20, 24, 28, 32)

    for surf_start in surfaces:
        for off in uv_offsets:
            pos = surf_start + off
            v = struct.unpack_from("<f", data, pos)[0]
            struct.pack_into("<f", data, pos, v * scale)

    with open(out_path, "wb") as f:
        f.write(data)

    return len(surfaces)


def main():
    parser = argparse.ArgumentParser(
        description="Multiply UV2 & UV3 of every Surface (LithTech DAT v66)"
    )
    parser.add_argument("scale", type=float,
                        help="Scale factor, e.g. 2.0 or 4.0")
    parser.add_argument("files", nargs="+",
                        help="Input .dat file(s)")
    parser.add_argument("-o", "--output-dir", default=".",
                        help="Output directory (default: current)")
    args = parser.parse_args()

    if args.scale == 0:
        parser.error("Scale factor must not be 0")

    os.makedirs(args.output_dir, exist_ok=True)

    errors = 0
    total  = 0

    for in_path in args.files:
        base_name = os.path.basename(in_path)
        out_path  = os.path.join(args.output_dir, base_name)
        try:
            n = process_file(in_path, out_path, args.scale)
            total += n
            print(f"{in_path}: {n} surfaces -> {out_path}")
        except Exception as e:
            print(f"ERROR: {in_path}: {e}", file=sys.stderr)
            errors += 1

    print()
    if errors:
        print(f"{errors} error(s) occurred. OK surfaces: {total}", file=sys.stderr)
        return 1
    else:
        print(f"Done. Total surfaces processed: {total}")
        return 0


if __name__ == "__main__":
    sys.exit(main())