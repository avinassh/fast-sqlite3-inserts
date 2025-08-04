# based on https://github.com/osoken/pyvlq/blob/main/src/pyvlq/core.py

from io import BytesIO


def encode(value: int) -> bytes:
    """Encode a value into a VLQ byte sequence."""
    if value < 0:
        raise ValueError("Value must be non-negative")
    if value == 0:
        return b"\x00"
    result = bytearray()
    while value:
        byte = value & 0x7F
        value >>= 7
        result.append(byte | 0x80)
    result.reverse()
    result[-1] &= 0x7F
    return bytes(result)


def decode(data: bytes) -> int:
    """Decode a VLQ byte sequence into a value."""
    value = 0
    for byte in data:
        value <<= 7
        value |= byte & 0x7F
        if not byte & 0x80:
            return value
    raise ValueError("Malformed VLQ byte sequence")


def decode_stream(data: BytesIO) -> int:
    """Decode a VLQ byte sequence into a value."""
    value = 0
    while True:
        byte = data.read(1)
        if not byte:
            raise ValueError("Malformed VLQ byte sequence")
        value <<= 7
        value |= byte[0] & 0x7F
        if not byte[0] & 0x80:
            return value
