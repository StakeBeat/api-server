import base64


def b64_to_hex(s: str) -> str:
    return f'0x{base64.b64decode(s).hex()}'


def gwei_to_ether(s: str) -> str:
    ether = int(s) / 10 ** 9
    return str(round(ether, 4))
