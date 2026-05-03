# DES Encryption Suite

A pure-Python, from-scratch implementation of the **Data Encryption Standard (DES)** — readable enough to trace with your eyes, complete enough to actually encrypt and decrypt real strings. Built entirely on the Python standard library, with an interactive terminal UI that lets you step inside the Feistel network instead of just calling a black-box function.

This project is for developers who want to **see how DES actually works**, not just call `encrypt()` and hope for the best.

---

## ⚠️ Security Warning

> **DES is cryptographically broken.**
> Its 56-bit effective key length is trivially brute-forced by modern hardware, and ECB mode leaks structural information about the plaintext (identical blocks encrypt to identical ciphertext).
>
> **Do not use this to protect real data.** This codebase is for education, auditing legacy systems, and understanding a foundational cipher — not for production security.

---

## What it does

- **Encrypts & decrypts** arbitrary UTF-8 strings using DES in ECB mode with automatic PKCS#5 padding
- **Reveals the internals** — inspect all 16 round keys or watch a full 16-round Feistel trace with L/R halves and subkeys
- **Exports ciphertext** in both hex and Base64 for interoperability
- **Runs zero-dependency** — every bit shuffle, S-box lookup, and key shift is explicit Python, not a call to an opaque library

---

## Requirements

- **Python 3.10+** (uses `X | Y` union type syntax in `des.py`)
- No third-party packages — standard library only

---

## Quick start

```bash
# Clone the repository
git clone https://github.com/Lucky-Roux-007/DES.git
cd DES

# Launch the interactive terminal UI
python main.py

# Or run the core engine directly on the classic test vector
python -m crypto.des

# Or run the ECB self-test
python -m crypto.ECB
```

---

## Project structure

```text
DES/
├── main.py              # Interactive TUI — menus, validation, ANSI UI
└── crypto/
    ├── __init__.py      # Package exports (des, ECB, encrypt, decrypt)
    ├── des.py           # Core DES engine — tables, key schedule, Feistel rounds
    └── ECB.py           # ECB mode wrapper — PKCS#5, UTF-8/bytes/hex bridge
```

| File | Role |
|------|------|
| `main.py` | Menu loop, four interactive screens, ANSI colour helpers, input validation |
| `crypto/des.py` | All DES constants (IP, FP, S-boxes, P-box, expansion table, key tables), `generate_round_keys()`, `des_process_block()` |
| `crypto/ECB.py` | `encrypt()` / `decrypt()` for multi-block ECB with PKCS#5 padding and UTF-8 handling |
| `crypto/__init__.py` | Re-exports `encrypt` and `decrypt` from `ECB` for one-line imports |

---

## How it works

DES is a **Feistel cipher**: the left and right halves of a 64-bit block trade places each round, and only one half is transformed per round. This elegant design means the encryption and decryption circuits are identical — only the order of the round keys changes.

### The DES pipeline

1. **Key schedule** — your 8-character ASCII key is converted to hex, then run through **PC-1** to discard parity bits, yielding two 28-bit halves. Each round, both halves are circularly shifted (1 or 2 bits according to the shift schedule), then compressed through **PC-2** to produce a unique 48-bit **round key**. This happens 16 times.

2. **Initial permutation** — the 64-bit plaintext block is shuffled by the **IP table**.

3. **16 Feistel rounds** — each round:
   - The right 32 bits are expanded to 48 bits via the **E-box**
   - XORed with the 48-bit round key
   - Fed into the **8 S-boxes** (6 bits → 4 bits each), producing 32 bits
   - Permuted by the **P-box**
   - XORed with the left 32 bits
   - Halves swap for the next round

4. **Final permutation** — after round 16, the combined block passes through the **FP table** (inverse of IP).

5. **Decryption** runs the exact same pipeline, but the 16 round keys are applied in **reverse order**.

### ECB wrapper data flow

The core engine only speaks 64-bit hex blocks. The `ECB.py` layer bridges real-world strings to the engine:

```
Encryption
──────────
UTF-8 string
  → encode to bytes
  → PKCS#5 pad to multiple of 8 bytes
  → hex string
  → split into 16-char (64-bit) blocks
  → each block: des_process_block(block, round_keys)
  → concatenate → uppercase hex ciphertext

Decryption
──────────
hex ciphertext
  → split into 16-char blocks
  → each block: des_process_block(block, round_keys_reversed)
  → concatenate hex → bytes
  → PKCS#5 unpad → decode UTF-8
```

---

## Interactive TUI

Run `python main.py` and choose from the menu:

| Key | Screen | What it does |
|-----|--------|--------------|
| `1` | **Encrypt** | Enter plaintext + 8-char key → returns hex & Base64 ciphertext |
| `2` | **Decrypt** | Enter hex or Base64 ciphertext + key → returns plaintext |
| `3` | **Inspect round keys** | Enter a key → displays all 16 subkeys (K01–K16) |
| `4` | **Verbose demo** | Runs the classic test vector with full round-by-round output |
| `0` | **Exit** | Quit |

### Encrypt example

```
  ❯ Plaintext: Hello, World!
  ❯ Key (8 chars): 12345678

  Encrypting  [████████████████]  done ✔

  ────────────────────────────────────────────────────
    RESULT
  ────────────────────────────────────────────────────
    Plaintext       Hello, World!
    Key             12345678
    Cipher (hex)    E0FDB6B0587BE967ED58F69D3C6B35C8
    Cipher (b64)    4P22sFh76Wftg...
    Blocks          2
  ────────────────────────────────────────────────────
```

### Decrypt example

```
  Input format:
  [1] Hex   [2] Base-64   ❯ 1

  ❯ Ciphertext (hex): E0FDB6B0587BE967ED58F69D3C6B35C8
  ❯ Key (8 chars): 12345678

  ────────────────────────────────────────────────────
    RESULT
  ────────────────────────────────────────────────────
    Cipher (hex)    E0FDB6B0587BE967ED58F69D3C6B35C8
    Key             12345678
    Plaintext       Hello, World!
  ────────────────────────────────────────────────────
```

---

## Use as a library

You don't have to use the TUI. Import the package directly:

```python
from crypto import encrypt, decrypt

# Encrypt a message
cipher_hex = encrypt("Attack at dawn", "myp4ssw0")
print(cipher_hex)
# → 8A3B... (hex ciphertext)

# Decrypt back
plain = decrypt(cipher_hex, "myp4ssw0")
print(plain)
# → Attack at dawn
```

Or drop down to the core engine for single-block operations:

```python
from crypto import des

# Generate round keys from a 16-char hex key
round_keys_bin, round_keys_hex = des.generate_round_keys("AABB09182736CCDD")

# Encrypt a single 64-bit block (16 hex chars)
cipher_bin = des.des_process_block("123456ABCD132536", round_keys_bin)
cipher_hex = des.binary_string_to_hex(cipher_bin)
print(cipher_hex)
```

---

## Classic test vector

The built-in verbose demo (option `[4]` in the TUI, or `python -m crypto.des`) uses the standard DES test vector:

| Field | Value |
|-------|-------|
| Plaintext | `123456ABCD132536` |
| Key | `AABB09182736CCDD` |
| Expected cipher | `C0B7A8D05F3A829C` |

The demo prints the L/R halves and the active round key after each of the 16 Feistel rounds for both encryption and decryption, making it easy to trace the state evolution by hand if you're studying the algorithm.

---

## Key constraints

| Parameter | Constraint |
|-----------|------------|
| Key | Exactly **8 ASCII characters** (64-bit input; parity bits discarded by PC-1) |
| Plaintext | Any UTF-8 string; padded automatically with PKCS#5 to 8-byte multiples |
| Ciphertext (hex) | Uppercase hex string; length must be a multiple of 16 characters |
| Block size | 64 bits (8 bytes) |
| Rounds | 16 |

> **Note:** The key must be exactly 8 ASCII characters. DES ignores the high bit of each byte (parity), so keys like `"password"` and `"password\x80"` are treated identically after byte-to-hex conversion.

---

## Limitations

- **ECB mode only** — no CBC, CTR, GCM, or other chaining modes
- **Single-key DES only** — no 3DES (Triple-DES)
- **ASCII keys only** — binary keys are not supported through the TUI
- **No authentication** — no MAC, HMAC, or AEAD
- **No IV / nonce** — ECB mode has none by design
- **Pure Python speed** — this is readable reference code, not a performance implementation. Large file encryption will be slow.
- **Cosmetic progress bar** — the TUI's animated 16-step bar is a fixed visual delay (0.03 s/step), not a real progress indicator

---

## Possible improvements

- **CBC mode** — add an initialization vector and XOR chaining to eliminate ECB's block-repetition leakage
- **3DES / Triple-DES** — stack three DES operations with two or three independent keys for a modest security upgrade
- **File I/O support** — extend the TUI to read and write binary files instead of only terminal strings
- **Performance layer** — rewrite hot paths (S-box lookups, permutations) with `bytearray` or `int` bit-twiddling instead of Python string operations
- **Unit tests** — add NIST-style test vectors and round-trip property tests with `pytest`

---

## License

Public domain / do whatever you want. This code exists so people can learn.