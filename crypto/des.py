#!/usr/bin/env python3
from typing import Sequence

# fmt: off
INITIAL_PERMUTATION_TABLE: Sequence[int] = (
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
)
# fmt: on

# fmt: off
EXPANSION_TABLE: Sequence[int] = (
    32, 1, 2, 3, 4, 5, 4, 5,
    6, 7, 8, 9, 8, 9, 10, 11,
    12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21,
    22, 23, 24, 25, 24, 25, 26, 27,
    28, 29, 28, 29, 30, 31, 32, 1,
)
# fmt: on

# fmt: off
P_BOX_TABLE: Sequence[int] = (
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25,
)
# fmt: on

# fmt: off
S_BOXES: Sequence[Sequence[Sequence[int]]] = (
    (
        (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
        (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
        (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
        (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13),
    ),
    (
        (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
        (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
        (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
        (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),
    ),
    (
        (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
        (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
        (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
        (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),
    ),
    (
        (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
        (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
        (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
        (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),
    ),
    (
        (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
        (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
        (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
        (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),
    ),
    (
        (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
        (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
        (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
        (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),
    ),
    (
        (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
        (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
        (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
        (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),
    ),
    (
        (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
        (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
        (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
        (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),
    ),
)
# fmt: on

# fmt: off
FINAL_PERMUTATION_TABLE: Sequence[int] = (
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25,
)
# fmt: on

# fmt: off
KEY_PERMUTATION_56: Sequence[int] = (
    57, 49, 41, 33, 25, 17, 9, 1,
    58, 50, 42, 34, 26, 18, 10, 2,
    59, 51, 43, 35, 27, 19, 11, 3,
    60, 52, 44, 36, 63, 55, 47, 39,
    31, 23, 15, 7, 62, 54, 46, 38,
    30, 22, 14, 6, 61, 53, 45, 37,
    29, 21, 13, 5, 28, 20, 12, 4,
)
# fmt: on

# fmt: off
KEY_SHIFT_TABLE: Sequence[int] = (
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
)
# fmt: on

# fmt: off
KEY_COMPRESSION_TABLE: Sequence[int] = (
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32,
)
# fmt: on


def hex_string_to_binary(hex_string: str) -> str:
    return "".join(f"{int(char, 16):04b}" for char in hex_string.upper())


def binary_string_to_hex(binary_string: str) -> str:
    if len(binary_string) % 4 != 0:
        raise ValueError("Binary string length must be a multiple of 4")
    return "".join(
        f"{int(binary_string[i : i + 4], 2):X}" for i in range(0, len(binary_string), 4)
    )


def permute_bits(bit_string: str, permutation_table: Sequence[int]) -> str:
    return "".join(bit_string[i - 1] for i in permutation_table)


def circular_shift_left(bit_string: str, shifts: int) -> str:
    shifts = shifts % len(bit_string)
    return bit_string[shifts:] + bit_string[:shifts]


def xor_bits(a: str, b: str) -> str:
    if len(a) != len(b):
        raise ValueError(f"XOR operands must have equal length ({len(a)} vs {len(b)})")
    return "".join("0" if x == y else "1" for x, y in zip(a, b))


def generate_round_keys(key_hex: str) -> tuple[list[str], list[str]]:
    key_binary = hex_string_to_binary(key_hex)
    key_56 = permute_bits(key_binary, KEY_PERMUTATION_56)

    left_half = key_56[:28]
    right_half = key_56[28:]

    round_keys_binary: list[str] = []
    round_keys_hex: list[str] = []

    for shift in KEY_SHIFT_TABLE:
        left_half = circular_shift_left(left_half, shift)
        right_half = circular_shift_left(right_half, shift)
        combined = left_half + right_half
        round_key = permute_bits(combined, KEY_COMPRESSION_TABLE)
        round_keys_binary.append(round_key)
        round_keys_hex.append(binary_string_to_hex(round_key))

    return round_keys_binary, round_keys_hex


def des_process_block(
    block_hex: str,
    round_keys_binary: list[str],
    *,
    verbose: bool = False,
    round_keys_hex: list[str] | None = None,
) -> str:
    if verbose and round_keys_hex is None:
        round_keys_hex = [binary_string_to_hex(rk) for rk in round_keys_binary]

    block_binary = hex_string_to_binary(block_hex)
    permuted = permute_bits(block_binary, INITIAL_PERMUTATION_TABLE)

    if verbose:
        print(f"After initial permutation : {binary_string_to_hex(permuted)}")

    left = permuted[:32]
    right = permuted[32:]

    for i in range(16):
        right_expanded = permute_bits(right, EXPANSION_TABLE)

        xor_result = xor_bits(right_expanded, round_keys_binary[i])

        sbox_result = ""
        for box_idx in range(8):
            chunk = xor_result[box_idx * 6 : (box_idx + 1) * 6]
            row = int(chunk[0] + chunk[5], 2)
            col = int(chunk[1:5], 2)
            val = S_BOXES[box_idx][row][col]
            sbox_result += f"{val:04b}"

        sbox_permuted = permute_bits(sbox_result, P_BOX_TABLE)

        feistel_output = xor_bits(left, sbox_permuted)
        left, right = right, feistel_output

        if verbose:
            print(
                f"Round {i + 1:02d} : "
                f"{binary_string_to_hex(left)}  "
                f"{binary_string_to_hex(right)}  "
                f" {round_keys_hex[i]}"
            )

    combined = right + left
    cipher_binary = permute_bits(combined, FINAL_PERMUTATION_TABLE)
    return cipher_binary


def main() -> None:
    plain_text = "123456ABCD132536"
    key = "AABB09182736CCDD"

    round_keys_bin, round_keys_hex = generate_round_keys(key)

    print("=" * 16, "Encryption", "=" * 16)
    cipher_binary = des_process_block(
        plain_text, round_keys_bin, verbose=True, round_keys_hex=round_keys_hex
    )
    cipher_text = binary_string_to_hex(cipher_binary)
    print("Cipher Text :", cipher_text)

    print()

    print("=" * 16, "Decryption", "=" * 16)
    decipher_binary = des_process_block(
        cipher_text,
        round_keys_bin[::-1],
        verbose=True,
        round_keys_hex=round_keys_hex[::-1],
    )
    plain_decrypted = binary_string_to_hex(decipher_binary)
    print("Plain Text  :", plain_decrypted)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}")
