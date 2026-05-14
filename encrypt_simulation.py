"""
Simulation: append .locked to every filename in dummy-files/ (rename only, no encryption).
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DUMMY_DIR = BASE_DIR / "dummy-files"
SUFFIX = ".locked"


def main() -> None:
    if not DUMMY_DIR.is_dir():
        print(f"Folder tidak ditemukan: {DUMMY_DIR}")
        return

    renamed = 0
    skipped = 0

    for path in sorted(DUMMY_DIR.iterdir()):
        if not path.is_file():
            continue
        name = path.name
        if name.endswith(SUFFIX):
            skipped += 1
            continue

        target = path.with_name(name + SUFFIX)
        if target.exists():
            print(f"Lewati (target sudah ada): {name} -> {target.name}")
            skipped += 1
            continue

        path.rename(target)
        print(f"Renamed: {name} -> {target.name}")
        renamed += 1

    print(f"Selesai. Di-rename: {renamed}, dilewati: {skipped}")


if __name__ == "__main__":
    main()
