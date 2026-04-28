from types import *
from typing import List, BinaryIO, Any

class WorldHeader:
    def __init__(self, stream: BinaryIO):
        self.Version = read_uint32(stream)
        self.ObjectDataPosition = read_uint32(stream)
        self.RenderDataPosition = read_uint32(stream)

class WorldInfo:
    def __init__(self, stream: BinaryIO):
        self.Length = read_uint32(stream)
        self.Value = stream.read(self.Length).decode('utf-8', errors='replace')
        self.Padding = [read_int32(stream) for _ in range(8)]

class ObjectProperty:
    def __init__(self, stream: BinaryIO):
        self.Name = read_ltstring(stream)
        self.Code = stream.read(1)[0]
        self.Flags = read_int32(stream)
        self.DataLength = read_uint16(stream)
        # Value depends on Code
        if self.Code == 0:      # string
            self.Value = read_ltstring(stream)
        elif self.Code == 1 or self.Code == 2:  # vector or color
            self.Value = read_ltvector(stream)
        elif self.Code == 3:    # float
            self.Value = read_float(stream)
        elif self.Code == 5:    # bool
            self.Value = bool(stream.read(1)[0])
        elif self.Code == 4 or self.Code == 6:  # flags or long int
            self.Value = read_uint32(stream)
        elif self.Code == 7:    # rotation
            self.Value = read_ltquat(stream)
        else:
            self.Value = stream.read(self.DataLength)

class WorldObject:
    def __init__(self, stream: BinaryIO):
        self.DataLength = read_uint16(stream)
        self.TypeString = read_ltstring(stream)
        self.PropertyCount = read_int32(stream)
        self.Properties = [ObjectProperty(stream) for _ in range(self.PropertyCount)]

class WorldObjectHeader:
    def __init__(self, stream: BinaryIO):
        self.Count = read_int32(stream)
        self.Objects = [WorldObject(stream) for _ in range(self.Count)]

# --- BSP structures -------------------------------------------------
class VertexInfo:
    def __init__(self, stream: BinaryIO):
        self.Count = read_uint8(stream)
        self.Extra = read_uint8(stream)

class LeafData:
    def __init__(self, stream: BinaryIO, size: int):
        self.PortalID = read_uint16(stream)
        self.Size = read_uint16(stream)  # unused, size already known
        self.Contents = stream.read(size)

class Leaf:
    def __init__(self, stream: BinaryIO):
        self.LeafListCount = read_uint16(stream)
        if self.LeafListCount == 0xFFFF:
            self.LeafListIndex = read_uint16(stream)
            self.Data = None
        else:
            self.Data = []
            for _ in range(self.LeafListCount):
                sz = read_uint16(stream)
                self.Data.append(LeafData(stream, sz))
        self.PolygonCount = read_uint16(stream)
        self.Polygons = stream.read(self.PolygonCount * 4)
        self.Unk1 = read_float(stream)

class Plane:
    def __init__(self, stream: BinaryIO):
        self.Normal = read_ltvector(stream)
        self.Distance = read_float(stream)

class Surface:
    def __init__(self, stream: BinaryIO):
        self.UV1 = read_ltvector(stream)
        self.UV2 = read_ltvector(stream)
        self.UV3 = read_ltvector(stream)
        self.UnkVec1 = read_ltvector(stream)
        self.UnkVec2 = read_ltvector(stream)
        self.UnkVec3 = read_ltvector(stream)
        self.Texture = read_uint16(stream)
        self.PlaneIndex = read_int32(stream)
        self.Flags = read_int32(stream)
        self.Unk2 = stream.read(4)
        self.UseEffects = read_uint8(stream)
        if self.UseEffects > 0:
            self.Effect = read_ltstring(stream)
            self.EffectParam = read_ltstring(stream)
        else:
            self.Effect = ""
            self.EffectParam = ""
        self.TextureFlags = read_uint16(stream)

class Point:
    def __init__(self, stream: BinaryIO):
        self.Data = read_ltvector(stream)

class DiskVert:
    def __init__(self, stream: BinaryIO):
        self.Verts = read_uint16(stream)
        self.Dummy = stream.read(3)

class Polygon:
    def __init__(self, stream: BinaryIO, vertex_info: VertexInfo):
        self.LightmapWidth = read_uint16(stream)
        self.LightmapHeight = read_uint16(stream)
        self.Unknown1 = read_float(stream)
        self.Unknown2 = read_float(stream)
        self.SurfaceIndex = read_int32(stream)
        self.Verts = []
        total_verts = vertex_info.Count + vertex_info.Extra
        for _ in range(total_verts):
            self.Verts.append(DiskVert(stream))

class Node:
    def __init__(self, stream: BinaryIO):
        self.Unknown = read_int32(stream)
        self.PolyIndex = read_int32(stream)
        self.LeafIndex = read_uint16(stream)
        self.NodeIndexes = [read_int32(stream), read_int32(stream)]
        self.UnknownQuat = read_ltquat(stream)

class UserPortal:
    def __init__(self, stream: BinaryIO):
        self.Name = read_ltstring(stream)
        self.Unk1 = read_int32(stream)
        self.Unk3 = read_uint16(stream)
        self.Center = read_ltvector(stream)
        self.Dims = read_ltvector(stream)

class PBlockContents:
    def __init__(self, stream: BinaryIO):
        self.VertIndex = read_uint8(stream)
        self.Padding = read_uint8(stream)
        self.Quat = stream.read(4)

class PBlock:
    def __init__(self, stream: BinaryIO):
        self.Size = read_uint16(stream)
        self.Unk1 = read_uint16(stream)
        self.Contents = [PBlockContents(stream) for _ in range(self.Size)]

class PBlockTable:
    def __init__(self, stream: BinaryIO):
        self.Unk1 = read_int32(stream)
        self.Unk2 = read_int32(stream)
        self.Unk3 = read_int32(stream)
        self.Unk4 = read_ltvector(stream)
        self.Unk5 = read_ltvector(stream)
        size = self.Unk1 * self.Unk2 * self.Unk3
        self.Blocks = [PBlock(stream) for _ in range(size)]

class WorldTexture:
    def __init__(self, stream: BinaryIO, name_length: int):
        self.Name = stream.read(name_length).decode('utf-8', errors='replace')

class WorldBSP:
    def __init__(self, stream: BinaryIO):
        self.InfoFlags = read_int32(stream)
        self.WorldName = read_ltstring(stream)
        self.NextPosition = read_int32(stream)
        self.PointCount = read_int32(stream)
        self.PlaneCount = read_int32(stream)
        self.SurfaceCount = read_int32(stream)
        self.UserPortalCount = read_int32(stream)
        self.PolyCount = read_int32(stream)
        self.LeafCount = read_int32(stream)
        self.VertCount = read_int32(stream)
        self.TotalVisListSize = read_int32(stream)
        self.LeafListCount = read_int32(stream)
        self.NodeCount = read_int32(stream)
        self.Unknown2 = read_int32(stream)
        self.MinBox = read_ltvector(stream)
        self.MaxBox = read_ltvector(stream)
        self.WorldTranslation = read_ltvector(stream)
        self.TextureNameLength = read_int32(stream)
        self.TextureCount = read_int32(stream)

        # Textures
        self.Textures = [WorldTexture(stream, self.TextureNameLength) for _ in range(self.TextureCount)]

        # Vertices for polygons
        self.Vertices = [VertexInfo(stream) for _ in range(self.PolyCount)]

        # Leaves
        self.LeafList = [Leaf(stream) for _ in range(self.LeafCount)]

        # Planes
        self.Planes = [Plane(stream) for _ in range(self.PlaneCount)]

        # Surfaces
        self.Surfaces = [Surface(stream) for _ in range(self.SurfaceCount)]

        # Polygons
        self.Polygons = []
        for i in range(self.PolyCount):
            self.Polygons.append(Polygon(stream, self.Vertices[i]))

        # Nodes
        self.Nodes = [Node(stream) for _ in range(self.NodeCount)]

        # Portals
        self.Portals = [UserPortal(stream) for _ in range(self.UserPortalCount)]

        # Points
        self.Points = [Point(stream) for _ in range(self.PointCount)]

        # PBlockTable
        self.BlockTable = PBlockTable(stream)

        # RootNodeIndex
        self.RootNodeIndex = read_int32(stream)

        # UnknownCount
        self.UnknownCount = read_int32(stream)

        # PolygonList (LTVector per polygon)
        self.PolygonList = [read_ltvector(stream) for _ in range(self.PolyCount)]

        # Lightmap data
        self.LightmapDataCount = read_int32(stream)
        self.LightmapData = stream.read(self.LightmapDataCount)

class WorldModel:
    def __init__(self, stream: BinaryIO):
        self.NextSection = read_int32(stream)
        self.Padding = [read_int32(stream) for _ in range(8)]
        self.BSPData = WorldBSP(stream)

class WorldModelHeader:
    def __init__(self, stream: BinaryIO):
        self.Count = read_int32(stream)
        self.Models = [WorldModel(stream) for _ in range(self.Count)]

class DATFileV56:
    def __init__(self, stream: BinaryIO):
        self.header = WorldHeader(stream)
        self.info = WorldInfo(stream)
        self.objectHeader = WorldObjectHeader(stream)
        self.modelHeader = WorldModelHeader(stream)

def parse(stream: BinaryIO) -> DATFileV56:
    return DATFileV56(stream)