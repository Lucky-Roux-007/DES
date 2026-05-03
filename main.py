#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║         DES Encryption Suite  v1.0           ║
║   Electronic Codebook (ECB) Mode  ·  64-bit  ║
╚══════════════════════════════════════════════╝
"""

import sys
import base64
import os
import time

from crypto import des, ECB

# ── ANSI colour helpers ──────────────────────────────────────────────────────

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

BLACK = "\033[30m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"

BG_BLACK = "\033[40m"


def c(text: str, *styles: str) -> str:
    """Wrap text in ANSI styles."""
    return "".join(styles) + text + RESET


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def hr(char: str = "─", width: int = 52, color: str = GRAY) -> None:
    print(c(char * width, color))


def banner() -> None:
    print()
    print(c("  ╔══════════════════════════════════════════════╗", CYAN, BOLD))
    print(
        c("  ║", CYAN, BOLD)
        + c("         DES Encryption Suite  v1.0           ", WHITE, BOLD)
        + c("║", CYAN, BOLD)
    )
    print(
        c("  ║", CYAN, BOLD)
        + c("   Electronic Codebook (ECB) Mode  ·  64-bit  ", GRAY)
        + c("║", CYAN, BOLD)
    )
    print(c("  ╚══════════════════════════════════════════════╝", CYAN, BOLD))
    print()


def tag(label: str, color: str = CYAN) -> str:
    return c(f" {label} ", color, BOLD, BG_BLACK)


def prompt(text: str, hint: str = "") -> str:
    hint_str = c(f"  {hint}", GRAY) if hint else ""
    print(hint_str)
    return input(c(f"  ❯ {text}: ", CYAN, BOLD)).strip()


def success(msg: str) -> None:
    print(c(f"\n  ✔  {msg}", GREEN, BOLD))


def error(msg: str) -> None:
    print(c(f"\n  ✖  {msg}", RED, BOLD))


def info(label: str, value: str, label_color: str = GRAY) -> None:
    print(f"  {c(label.ljust(14), label_color)}  {c(value, WHITE)}")


def loading(label: str = "Processing", steps: int = 16) -> None:
    blocks = "█▓▒░"
    sys.stdout.write(f"\n  {c(label, CYAN)}  ")
    for i in range(steps):
        bar = c("█" * (i + 1), CYAN) + c("░" * (steps - i - 1), GRAY)
        sys.stdout.write(
            f"\r  {c(label, CYAN)}  [{bar}]  {c(f'round {i+1:02d}/16', GRAY)}"
        )
        sys.stdout.flush()
        time.sleep(0.03)
    sys.stdout.write(
        f"\r  {c(label, GREEN)}  [{c('█' * steps, GREEN)}]  {c('done ✔', GREEN)}\n"
    )
    sys.stdout.flush()


# ── Validation ───────────────────────────────────────────────────────────────


def validate_key(key: str) -> str | None:
    """Return error message or None if valid."""
    if len(key.encode("utf-8")) != 8:
        return f"Key must be exactly 8 ASCII characters (got {len(key)})."
    return None


def validate_hex(text: str) -> str | None:
    if len(text) % 16 != 0:
        return "Ciphertext hex length must be a multiple of 16."
    try:
        bytes.fromhex(text)
    except ValueError:
        return "Not valid hexadecimal."
    return None


# ── Feature screens ──────────────────────────────────────────────────────────


def screen_encrypt() -> None:
    clear()
    banner()
    print(c("  ── ENCRYPT ─────────────────────────────────────", CYAN))
    print()

    plain = prompt("Plaintext", "Enter the message you want to encrypt")
    if not plain:
        error("Plaintext cannot be empty.")
        input(c("\n  Press Enter to continue…", GRAY))
        return

    key = prompt("Key (8 chars)", "Exactly 8 ASCII characters  e.g. 12345678")
    err = validate_key(key)
    if err:
        error(err)
        input(c("\n  Press Enter to continue…", GRAY))
        return

    print()
    loading("Encrypting")

    try:
        cipher_hex = ECB.encrypt(plain, key)
    except Exception as exc:
        error(str(exc))
        input(c("\n  Press Enter to continue…", GRAY))
        return

    cipher_b64 = base64.b64encode(bytes.fromhex(cipher_hex)).decode()

    print()
    hr()
    print(c("  RESULT", CYAN, BOLD))
    hr()
    info("Plaintext", plain)
    info("Key", key)
    info("Cipher (hex)", cipher_hex)
    info("Cipher (b64)", cipher_b64)
    info("Blocks", str(len(cipher_hex) // 16))
    hr()

    input(c("\n  Press Enter to continue…", GRAY))


def screen_decrypt() -> None:
    clear()
    banner()
    print(c("  ── DECRYPT ─────────────────────────────────────", YELLOW))
    print()

    print(c("  Input format:", GRAY))
    fmt_choice = input(
        f"  {c('[1]', CYAN)} Hex   {c('[2]', CYAN)} Base-64   {c('❯', CYAN, BOLD)} "
    ).strip()

    cipher_hex: str
    if fmt_choice == "2":
        raw = prompt("Ciphertext (base-64)")
        try:
            cipher_hex = base64.b64decode(raw).hex().upper()
        except Exception:
            error("Invalid base-64 string.")
            input(c("\n  Press Enter to continue…", GRAY))
            return
    else:
        cipher_hex = prompt("Ciphertext (hex)").upper()

    err = validate_hex(cipher_hex)
    if err:
        error(err)
        input(c("\n  Press Enter to continue…", GRAY))
        return

    key = prompt("Key (8 chars)", "Same key used during encryption")
    err = validate_key(key)
    if err:
        error(err)
        input(c("\n  Press Enter to continue…", GRAY))
        return

    print()
    loading("Decrypting")

    try:
        plain = ECB.decrypt(cipher_hex, key)
    except Exception as exc:
        error(str(exc))
        input(c("\n  Press Enter to continue…", GRAY))
        return

    print()
    hr()
    print(c("  RESULT", YELLOW, BOLD))
    hr()
    info("Cipher (hex)", cipher_hex)
    info("Key", key)
    info("Plaintext", plain, GREEN)
    hr()

    input(c("\n  Press Enter to continue…", GRAY))


def screen_round_keys() -> None:
    clear()
    banner()
    print(c("  ── ROUND KEYS ───────────────────────────────────", BLUE))
    print()

    key = prompt("Key (8 chars)", "Inspect all 16 subkeys derived from your key")
    err = validate_key(key)
    if err:
        error(err)
        input(c("\n  Press Enter to continue…", GRAY))
        return

    key_hex = key.encode("utf-8").hex().upper()
    _, round_keys_hex = des.generate_round_keys(key_hex)

    print()
    hr()
    print(c("  KEY SCHEDULE", BLUE, BOLD))
    hr()
    info("Master key", key)
    info("Key (hex)", key_hex)
    print()
    for i, rk in enumerate(round_keys_hex, 1):
        num = c(f"  K{i:02d}", BLUE, BOLD)
        value = c(rk, WHITE)
        bits = c(f"  ({len(rk)*4} bits)", GRAY)
        print(f"{num}  {value}{bits}")
    hr()

    input(c("\n  Press Enter to continue…", GRAY))


def screen_demo() -> None:
    clear()
    banner()
    print(c("  ── VERBOSE DEMO ─────────────────────────────────", GREEN))
    print()
    print(c("  Running the classic DES test vector:", GRAY))
    print(c("  Plaintext : 123456ABCD132536", WHITE))
    print(c("  Key       : AABB09182736CCDD", WHITE))
    print()
    hr()

    # Capture des.main() output by calling internals directly
    plain_text = "123456ABCD132536"
    key = "AABB09182736CCDD"

    round_keys_bin, round_keys_hex = des.generate_round_keys(key)

    print(c("  ENCRYPTION – round-by-round", GREEN, BOLD))
    hr()

    cipher_binary = des.des_process_block(
        plain_text, round_keys_bin, verbose=True, round_keys_hex=round_keys_hex
    )
    cipher_text = des.binary_string_to_hex(cipher_binary)
    print(c(f"\n  Cipher Text : {cipher_text}", GREEN, BOLD))

    print()
    hr()
    print(c("  DECRYPTION – round-by-round", YELLOW, BOLD))
    hr()

    decipher_binary = des.des_process_block(
        cipher_text,
        round_keys_bin[::-1],
        verbose=True,
        round_keys_hex=round_keys_hex[::-1],
    )
    plain_decrypted = des.binary_string_to_hex(decipher_binary)
    print(c(f"\n  Plain Text  : {plain_decrypted}", YELLOW, BOLD))
    hr()

    input(c("\n  Press Enter to continue…", GRAY))


# ── Main menu ────────────────────────────────────────────────────────────────

MENU_ITEMS = [
    ("1", "Encrypt", CYAN),
    ("2", "Decrypt", YELLOW),
    ("3", "Inspect round keys", BLUE),
    ("4", "Verbose demo", GREEN),
    ("0", "Exit", RED),
]


def menu() -> None:
    while True:
        clear()
        banner()
        hr()
        print(c("  MAIN MENU", WHITE, BOLD))
        hr()
        for key, label, color in MENU_ITEMS:
            print(f"  {c(f'[{key}]', color, BOLD)}  {c(label, WHITE)}")
        hr()
        print()

        choice = input(c("  ❯ Choose: ", CYAN, BOLD)).strip()

        if choice == "1":
            screen_encrypt()
        elif choice == "2":
            screen_decrypt()
        elif choice == "3":
            screen_round_keys()
        elif choice == "4":
            screen_demo()
        elif choice == "0":
            clear()
            banner()
            print(c("  Goodbye.\n", GRAY))
            sys.exit(0)
        else:
            error("Unknown option — press 1, 2, 3, 4, or 0.")
            time.sleep(0.8)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(c("\n\n  Interrupted.\n", GRAY))
        sys.exit(0)
