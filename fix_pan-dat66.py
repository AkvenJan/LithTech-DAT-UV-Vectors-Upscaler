#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# fix_pan_dat.py
#
# Для LithTech DAT v66 (NOLF).
# Ищет Surfaces[].Effect == "Pan" (без учёта регистра)
# и делит все целые числа в EffectParam на divisor.
#
# Использование:
#   python fix_pan_dat.py <divisor> <input.dat> <output.dat>
#
# Пример:
#   python fix_pan_dat.py 4 map.dat map_fixed.dat

import argparse
import math
import re
import struct
import sys


def u16(data, pos):
    return struct.unpack_from("<H", data, pos)[0]


def i16(data, pos):
    return struct.unpack_from("<h", data, pos)[0]


def u32(data, pos):
    return struct.unpack_from("<I", data, pos)[0]


def i32(data, pos):
    return struct.unpack_from("<i", data, pos)[0]


def read_ltstring(data, pos):
    """
    LTString:
        short Length;
        if Length > 0: char Value[Length];
    Возвращает (value_bytes, new_pos, start_pos).
    """
    start = pos
    length = i16(data, pos)
    pos += 2
    if length > 0:
        value = data[pos:pos + length]
        pos += length
    else:
        value = b""
    return value, pos, start


def skip_subdivision(data, pos):
    """
    Эмуляция read_layout() из шаблона 010 Editor.
    Нужна, чтобы корректно перейти к WorldModelHeader.
    """
    current_byte = 0
    current_bit = 8

    def read_layout(depth):
        nonlocal pos, current_byte, current_bit

        if current_bit == 8:
            current_byte = data[pos]
            pos += 1
            current_bit = 0

        subdivide = (current_byte & (1 << current_bit)) != 0
        current_bit += 1

        if depth > 16:
            return

        if subdivide:
            for _ in range(4):
                read_layout(depth + 1)

    read_layout(0)
    return pos


def skip_leaf(data, pos):
    leaf_list_count = u16(data, pos)
    pos += 2

    if leaf_list_count == 0xFFFF:
        pos += 2  # ushort LeafListIndex
    else:
        for _ in range(leaf_list_count):
            pos += 2  # short PortalID
            size = u16(data, pos)
            pos += 2
            pos += size  # uchar Contents[Size]

    polygon_count = i32(data, pos)
    pos += 4
    if polygon_count > 0:
        pos += polygon_count * 4  # char Polygons[PolygonCount * 4]

    pos += 4  # int Unk1
    return pos


def parse_surface(data, pos):
    start = pos

    # LTVector UV1, UV2, UV3
    pos += 12 * 3

    pos += 2  # ushort Texture
    pos += 4  # int Unk1
    pos += 4  # int Flags
    pos += 4  # uchar Unk2[4]

    use_effects = data[pos]
    pos += 1

    effect = b""
    effect_param = b""
    effect_param_start = None
    effect_param_end = None

    if use_effects > 0:
        effect, pos, _ = read_ltstring(data, pos)
        effect_param_start = pos
        effect_param, pos, _ = read_ltstring(data, pos)
        effect_param_end = pos

    pos += 2  # ushort TextureFlags

    return {
        "start": start,
        "end": pos,
        "use_effects": use_effects,
        "effect": effect,
        "effect_param": effect_param,
        "effect_param_start": effect_param_start,
        "effect_param_end": effect_param_end,
    }


def skip_polygon(data, pos, vertex_info):
    count, extra = vertex_info

    pos += 12  # LTVector Center
    pos += 2   # short LightmapWidth
    pos += 2   # short LightmapHeight

    unknown = i16(data, pos)
    pos += 2

    if unknown > 0:
        # short MoreUnknown[Unknown * 2]
        pos += unknown * 2 * 2

    pos += 2  # short SurfaceIndex
    pos += 2  # short PlaneIndex

    # DiskVert Verts[Count + Extra]
    # DiskVert: short Verts; uchar Dummy[3]; => 5 bytes
    pos += (count + extra) * 5

    return pos


def parse_bsp(data, pos):
    start = pos

    pos += 4  # int InfoFlags
    pos += 4  # int Unknown

    _, pos, _ = read_ltstring(data, pos)  # LTString WorldName

    counts = struct.unpack_from("<10i", data, pos)
    pos += 40

    (
        point_count,
        plane_count,
        surface_count,
        user_portal_count,
        poly_count,
        leaf_count,
        vert_count,
        total_vis_list_size,
        leaf_list_count,
        node_count,
    ) = counts

    pos += 4  # int Unknown2
    pos += 4  # int Unknown3

    pos += 12 * 3  # MinBox, MaxBox, WorldTranslation

    texture_name_length = i32(data, pos)
    texture_count = i32(data, pos + 4)
    pos += 8

    # WorldTexture WorldTextures(TextureNameLength)
    pos += texture_name_length

    # Vertex Vertices[PolyCount]
    vertices = []
    for _ in range(poly_count):
        count = data[pos]
        extra = data[pos + 1]
        pos += 2
        vertices.append((count, extra))

    # Leaf LeafList[LeafCount]
    if leaf_count > 0:
        for _ in range(leaf_count):
            pos = skip_leaf(data, pos)

    # Plane Planes[PlaneCount]
    pos += plane_count * 16

    # Surface Surfaces[SurfaceCount]
    surfaces = []
    for _ in range(surface_count):
        surf = parse_surface(data, pos)
        surfaces.append(surf)
        pos = surf["end"]

    # Polygon Poly(Vertices[i]) для каждого полигона
    for i in range(poly_count):
        pos = skip_polygon(data, pos, vertices[i])

    # Node Nodes[NodeCount]
    if node_count > 0:
        pos += node_count * 14  # 4 + 2 + 8

    # UserPortal Portals[UserPortalCount]
    if user_portal_count > 0:
        for _ in range(user_portal_count):
            _, pos, _ = read_ltstring(data, pos)  # LTString Name
            pos += 4   # int Unk1
            pos += 2   # short Unk2
            pos += 12  # LTVector Center
            pos += 12  # LTVector Dims

    # Point Points[PointCount]
    pos += point_count * 24

    # PBlockTable BlockTable
    grid_x = i32(data, pos)
    grid_y = i32(data, pos + 4)
    grid_z = i32(data, pos + 8)
    pos += 12

    block_count = grid_x * grid_y * grid_z

    pos += 12  # LTVector BoundsMax
    pos += 12  # LTVector BoundsMin

    if block_count > 0:
        for _ in range(block_count):
            size = u16(data, pos)
            pos += 2
            pos += 2  # ushort Max
            pos += size * 6  # PBlockContents: 3 * short

    pos += 4  # int RootNodeIndex
    sections = i32(data, pos)
    pos += 4

    return {
        "start": start,
        "end": pos,
        "sections": sections,
        "surfaces": surfaces,
    }


def parse_dat(data):
    if len(data) < 44:
        raise ValueError("Файл слишком маленький для WorldHeader")

    version = u32(data, 0)
    if version != 66:
        print(f"WARNING: Version = {version}, ожидался 66", file=sys.stderr)

    object_data_position = u32(data, 4)
    render_data_position = u32(data, 8)

    offset_fields = [
        (4, object_data_position, "WorldHeader.ObjectDataPosition"),
        (8, render_data_position, "WorldHeader.RenderDataPosition"),
    ]

    pos = 44

    # WorldInfo
    info_length = u32(data, pos)
    pos += 4
    pos += info_length
    pos += 4   # float LMGridSize
    pos += 12  # LTVector BoundaryMin
    pos += 12  # LTVector BoundaryMax

    # WorldTree
    pos += 32

    # subdivision_data
    pos = skip_subdivision(data, pos)

    # WorldModelHeader
    model_count = i32(data, pos)
    pos += 4

    models = []
    current = pos

    for mi in range(model_count):
        model_start = current
        next_world_item = i32(data, model_start)

        # WorldModel:
        #   int NextWorldItem;
        #   char Padding2[32];
        #   WorldBSP BSPData;
        bsp_start = model_start + 4 + 32
        bsp = parse_bsp(data, bsp_start)

        models.append({
            "start": model_start,
            "next_world_item": next_world_item,
            "bsp": bsp,
        })

        if next_world_item > 0 and next_world_item <= len(data):
            offset_fields.append((
                model_start,
                next_world_item,
                f"model[{mi}].NextWorldItem",
            ))

        if bsp["sections"] > 0:
            if next_world_item <= 0 or next_world_item > len(data):
                raise ValueError(f"Некорректный NextWorldItem для model[{mi}]")
            current = next_world_item
        else:
            current = bsp["end"]

    return models, offset_fields


def divide_number(n, divisor):
    """
    Делит n на divisor.

    Округление:
      - до ближайшего целого;
      - ровно .5 округляется к нулю (чтобы 6/4 -> 1, как в примере);
      - результат не может быть 0, если исходное число не 0:
        минимум по модулю = 1.
    """
    if n == 0:
        return 0

    if divisor <= 0:
        raise ValueError("divisor должен быть > 0")

    sign = -1 if n < 0 else 1
    a = abs(n)
    x = a / float(divisor)

    q = int(math.floor(x))
    frac = x - q

    if frac > 0.5:
        q += 1
    # frac == 0.5: оставляем q, то есть округляем к нулю

    if q == 0:
        q = 1

    return sign * q


def collect_replacements(data, models, divisor):
    replacements = []

    for model in models:
        for surf in model["bsp"]["surfaces"]:
            if surf["use_effects"] <= 0:
                continue

            effect = surf["effect"]
            if effect.lower() != b"pan":
                continue

            if surf["effect_param_start"] is None:
                continue

            old_value = surf["effect_param"] or b""

            # Достаём все целые числа: -36, 2, 0, 16 и т.п.
            tokens = re.findall(rb"[+-]?\d+", old_value)
            if not tokens:
                continue

            new_tokens = []
            for tok in tokens:
                n = int(tok)
                new_n = divide_number(n, divisor)
                new_tokens.append(str(new_n).encode("ascii"))

            new_value = b" ".join(new_tokens)

            if len(new_value) > 32767:
                raise ValueError("Новая длина EffectParam > 32767")

            new_chunk = struct.pack("<h", len(new_value)) + new_value

            start = surf["effect_param_start"]
            end = surf["effect_param_end"]
            old_chunk = data[start:end]

            if new_chunk != old_chunk:
                replacements.append((start, end, new_chunk))

    replacements.sort(key=lambda x: x[0])

    # Проверка на пересечения
    for i in range(1, len(replacements)):
        if replacements[i][0] < replacements[i - 1][1]:
            raise ValueError("Пересекающиеся замены EffectParam")

    return replacements


def apply_replacements_and_patch_offsets(data, replacements, offset_fields):
    if not replacements:
        return data

    replacements.sort(key=lambda x: x[0])

    out = bytearray()
    last = 0

    for start, end, new_chunk in replacements:
        out += data[last:start]
        out += new_chunk
        last = end

    out += data[last:]

    def map_old_offset(old_offset):
        delta = 0
        for start, end, new_chunk in replacements:
            if old_offset >= end:
                delta += len(new_chunk) - (end - start)
            elif old_offset > start:
                # Offset внутрь заменяемой строки — не ожидается.
                return start + delta
            else:
                break
        return old_offset + delta

    for old_field_pos, old_target, name in offset_fields:
        if old_target <= 0 or old_target > len(data):
            continue

        new_field_pos = map_old_offset(old_field_pos)
        new_target = map_old_offset(old_target)

        struct.pack_into("<i", out, new_field_pos, new_target)

    return bytes(out)


def main():
    parser = argparse.ArgumentParser(
        description="Fix Pan EffectParam in LithTech DAT v66"
    )
    parser.add_argument("divisor", type=float, help="Делитель, например 4")
    parser.add_argument("input", help="Исходный .dat")
    parser.add_argument("output", help="Куда сохранить результат")
    args = parser.parse_args()

    if args.divisor <= 0:
        parser.error("divisor должен быть > 0")

    with open(args.input, "rb") as f:
        data = f.read()

    models, offset_fields = parse_dat(data)
    replacements = collect_replacements(data, models, args.divisor)
    result = apply_replacements_and_patch_offsets(data, replacements, offset_fields)

    with open(args.output, "wb") as f:
        f.write(result)

    print(f"Готово. Заменено EffectParam: {len(replacements)}")
    print(f"Результат: {args.output}")


if __name__ == "__main__":
    main()