import struct
def read_uint8(stream) -> int:
    return struct.unpack("<B", stream.read(1))[0]

def read_uint16(stream) -> int:
    return struct.unpack("<H", stream.read(2))[0]

def read_uint32(stream) -> int:
    return struct.unpack("<I", stream.read(4))[0]

def read_int32(stream) -> int:
    return struct.unpack("<i", stream.read(4))[0]

def read_float(stream) -> float:
    return struct.unpack("<f", stream.read(4))[0]