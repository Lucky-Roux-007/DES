#!/usr/bin/env python3
from . import des
import base64


def pad_pkcs5(data: bytes) -> bytes:
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len] * pad_len)


def unpad_pkcs5(data: bytes) -> bytes:
    if not data:
        raise ValueError("Invalid padding: empty input")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 8:
        raise ValueError("Invalid padding")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid padding")
    return data[:-pad_len]


def encrypt(plain_text: str, key: str) -> str:
    key_bytes = key.encode("utf-8")
    if len(key_bytes) != 8:
        raise ValueError("Key must be 8 bytes (64-bit DES key)")
    key_hex = key_bytes.hex().upper()
    data = plain_text.encode("utf-8")
    padded = pad_pkcs5(data)
    hex_string = padded.hex().upper()
    round_keys_bin, _ = des.generate_round_keys(key_hex)
    blocks = []
    for i in range(0, len(hex_string), 16):
        block = hex_string[i : i + 16]
        cipher_bin = des.des_process_block(block, round_keys_bin)
        blocks.append(des.binary_string_to_hex(cipher_bin))
    return "".join(blocks)


def decrypt(cipher_text: str, key: str) -> str:
    key_bytes = key.encode("utf-8")
    if len(key_bytes) != 8:
        raise ValueError("Key must be 8 bytes (64-bit DES key)")
    key_hex = key_bytes.hex().upper()
    round_keys_bin, _ = des.generate_round_keys(key_hex)
    round_keys_bin = round_keys_bin[::-1]
    plain_hex = ""
    for i in range(0, len(cipher_text), 16):
        block = cipher_text[i : i + 16]
        plain_bin = des.des_process_block(block, round_keys_bin)
        plain_hex += des.binary_string_to_hex(plain_bin)
    data = bytes.fromhex(plain_hex)
    return unpad_pkcs5(data).decode("utf-8")


def main() -> None:
    text = "HELLO DES"
    key = "12345678"

    c = encrypt(text, key)
    p = decrypt(c, key)

    print(f"Text:        {text}")
    print(f"Cipher hex:  {c}")
    print(f"Cipher b64:  {base64.b64encode(bytes.fromhex(c)).decode()}")
    print(f"Plain Text:  {p}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}")
