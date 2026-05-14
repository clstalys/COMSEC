"""
Flask backend for ransomware rename simulation (educational only).
Serves templates/static and exposes /api/files from dummy-files/.
"""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, render_template, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
DUMMY_DIR = BASE_DIR / "dummy-files"

# Serve static assets from / so existing href="style.css" and src="login.js" keep working.
app = Flask(__name__, static_folder="static", static_url_path="")


def _format_size(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} B"
    kb = num_bytes / 1024.0
    if kb < 1024:
        return f"{kb:.1f} KB"
    mb = kb / 1024.0
    return f"{mb:.1f} MB"


def _file_kind(filename: str) -> tuple[str, str]:
    """Return (icon_label, human_type) based on original logical name."""
    lower = filename.lower()
    if lower.endswith(".locked"):
        lower = lower[: -len(".locked")]
    ext = Path(lower).suffix.lower()
    mapping = {
        ".pdf": ("PDF", "PDF Document"),
        ".csv": ("CSV", "CSV File"),
        ".docx": ("DOC", "Word Document"),
        ".doc": ("DOC", "Word Document"),
        ".png": ("PNG", "Image File"),
        ".jpg": ("IMG", "Image File"),
        ".jpeg": ("IMG", "Image File"),
        ".gif": ("IMG", "Image File"),
        ".sql": ("SQL", "Database Backup"),
        ".txt": ("TXT", "Text File"),
    }
    return mapping.get(ext, ("FILE", "File"))


def _logical_original_name(filename: str) -> str:
    if filename.endswith(".locked"):
        return filename[: -len(".locked")]
    return filename


def build_files_payload() -> list[dict]:
    if not DUMMY_DIR.is_dir():
        return []

    rows: list[dict] = []
    for name in sorted(os.listdir(DUMMY_DIR)):
        path = DUMMY_DIR / name
        if not path.is_file():
            continue

        original_name = _logical_original_name(name)
        current_name = name
        is_locked = name.endswith(".locked")
        status = "Encrypted" if is_locked else "Normal"

        icon, doc_type = _file_kind(original_name)
        size_str = _format_size(path.stat().st_size)

        rows.append(
            {
                "originalName": original_name,
                "currentName": current_name,
                "status": status,
                "type": doc_type,
                "size": size_str,
                "icon": icon,
                "originalUrl": f"/dummy-files/{original_name}",
                "currentUrl": f"/dummy-files/{current_name}",
            }
        )

    return rows


@app.route("/")
@app.route("/login.html")
def login_page():
    """Login: `/` dan `/login.html` (link dari signup & bookmark)."""
    return render_template("login.html")


@app.route("/dashboard")
@app.route("/index.html")
def dashboard():
    return render_template("index.html")


@app.route("/files")
@app.route("/file.html")
def files_page():
    return render_template("file.html")


@app.route("/signup.html")
def signup_page():
    return render_template("signup.html")


@app.route("/api/files")
def api_files():
    return jsonify(build_files_payload())


@app.route("/dummy-files/<path:filename>")
def serve_dummy_file(filename):
    return send_from_directory(DUMMY_DIR, filename, as_attachment=False)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
