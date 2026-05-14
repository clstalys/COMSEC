"""
Simulation: remove trailing .locked from filenames in dummy-files/ (rename only).
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DUMMY_DIR = BASE_DIR / "dummy-files"
SUFFIX = ".locked"


def main() -> None:
    if not DUMMY_DIR.is_dir():
        print(f"Folder tidak ditemukan: {DUMMY_DIR}")
        return

    restored = 0
    skipped = 0

    for path in sorted(DUMMY_DIR.iterdir()):
        if not path.is_file():
            continue
        name = path.name
        if not name.endswith(SUFFIX):
            skipped += 1
            continue

        original_name = name[: -len(SUFFIX)]
        if not original_name:
            print(f"Lewati nama tidak valid: {name}")
            skipped += 1
            continue

        target = path.with_name(original_name)
        if target.exists():
            print(f"Lewati (file target sudah ada): {name} -> {original_name}")
            skipped += 1
            continue

        path.rename(target)
        print(f"Restored: {name} -> {original_name}")
        restored += 1

    print(f"Selesai. Dipulihkan: {restored}, dilewati: {skipped}")


if __name__ == "__main__":
    main()
