"""
Simulasi dekripsi/recovery file menggunakan AES-128 CBC (educational only).
Membaca key & IV dari encryption_key.json, lalu mendekripsi semua file .locked.
"""

import json
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

BASE_DIR  = Path(__file__).resolve().parent
DUMMY_DIR = BASE_DIR / "dummy-files"
KEY_FILE  = BASE_DIR / "encryption_key.json"
SUFFIX    = ".locked"
BLOCK_SIZE = 128


def unpad_data(data: bytes) -> bytes:
    """Hapus PKCS7 padding setelah dekripsi."""
    unpadder = padding.PKCS7(BLOCK_SIZE).unpadder()
    return unpadder.update(data) + unpadder.finalize()


def decrypt_file(path: Path, key: bytes, iv: bytes) -> dict:
    """Dekripsi satu file .locked kembali ke file asli."""
    encrypted_size = path.stat().st_size
    ciphertext     = path.read_bytes()

    cipher    = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext = unpad_data(decryptor.update(ciphertext) + decryptor.finalize())

    original_name = path.name[: -len(SUFFIX)]
    original_path = path.with_name(original_name)
    original_path.write_bytes(plaintext)
    path.unlink()

    restored_size = original_path.stat().st_size
    size_diff     = encrypted_size - restored_size

    print(
        f"[RESTORED] {path.name} -> {original_name} | "
        f"Encrypted: {encrypted_size} B | Restored: {restored_size} B | "
        f"Selisih: -{size_diff} B"
    )

    return {
        "encrypted_name": path.name,
        "restored_name":  original_name,
        "encrypted_size": encrypted_size,
        "restored_size":  restored_size,
        "size_difference": size_diff,
    }


def main() -> list:
    if not DUMMY_DIR.is_dir():
        print(f"Folder tidak ditemukan: {DUMMY_DIR}")
        return []

    if not KEY_FILE.exists():
        print(f"Key file tidak ditemukan: {KEY_FILE}")
        print("Jalankan encrypt_simulation.py terlebih dahulu.")
        return []

    key_data  = json.loads(KEY_FILE.read_text())
    key       = bytes.fromhex(key_data["key_hex"])
    iv        = bytes.fromhex(key_data["iv_hex"])
    algorithm = key_data.get("algorithm", "AES-128-CBC")

    results  = []
    restored = 0
    skipped  = 0

    print(f"=== RECOVERY SIMULATION — {algorithm} ===")
    print(f"Key (hex): {key.hex()}")
    print(f"IV  (hex): {iv.hex()}")
    print("=" * 45)

    for path in sorted(DUMMY_DIR.iterdir()):
        if not path.is_file():
            continue
        if not path.name.endswith(SUFFIX):
            print(f"[SKIP] Bukan file terenkripsi: {path.name}")
            skipped += 1
            continue

        info = decrypt_file(path, key, iv)
        results.append(info)
        restored += 1

    # Hapus key file setelah recovery (simulasi key dihapus)
    KEY_FILE.unlink(missing_ok=True)

    print("=" * 45)
    print(f"Selesai. Dipulihkan: {restored}, dilewati: {skipped}")
    print("Key file dihapus setelah recovery.")
    return results


if __name__ == "__main__":
    main()
