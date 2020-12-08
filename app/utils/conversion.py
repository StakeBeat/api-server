import base64


def b64_to_hex(s: str) -> str:
    return f'0x{base64.b64decode(s).hex()}'
