# COMSEC — Ransomware Rename Simulation (Flask)

Simulasi edukasi: file di folder `dummy-files/` hanya di-rename dengan ekstensi `.locked` (bukan enkripsi sungguhan).

## Struktur folder

```
COMSEC/
├── app.py
├── encrypt_simulation.py
├── recovery.py
├── requirements.txt
├── README.md
├── dummy-files/
│   ├── data.csv
│   ├── database_backup.sql
│   ├── employee.docx
│   ├── foto_karyawan.png
│   ├── laporan.pdf
│   └── test.txt
├── templates/
│   ├── index.html
│   ├── file.html
│   ├── login.html
│   └── signup.html
└── static/
    ├── style.css
    ├── login.js
    ├── signup.js
    └── images/          (letakkan logo, contoh: logoBSI.png, bsi.png)
```

`static_url_path` dikosongkan agar `href="style.css"` dan `src="login.js"` pada template tetap valid tanpa mengubah layout.

## Persiapan

1. Pasang Python 3.9+ dari [python.org](https://www.python.org/downloads/) (centang **Add python.exe to PATH**).
2. Di folder `COMSEC`:

```text
python -m pip install -r requirements.txt
```

## Menjalankan Flask (`app.py`)

```text
cd COMSEC
python app.py
```

Buka peramban: `http://127.0.0.1:5000/`

| Rute | Halaman |
|------|---------|
| `/` atau `/login.html` | Login (sama; `/login.html` dipakai setelah sign up) |
| `/dashboard` atau `/index.html` | Dashboard |
| `/files` atau `/file.html` | File Management (memuat data dari `GET /api/files`) |
| `/api/files` | JSON daftar file dari `dummy-files/` |
| `/dummy-files/<nama_file>` | Mengunduh/menampilkan file dummy |
| `/signup.html` | Sign up (jika template ada) |

## Menjalankan simulasi “enkripsi” (rename saja)

```text
cd COMSEC
python encrypt_simulation.py
```

Semua file di `dummy-files/` yang belum berakhiran `.locked` akan di-rename menjadi `nama.ext.locked`.

## Menjalankan recovery (kembalikan nama file)

```text
cd COMSEC
python recovery.py
```

Semua file `*.locked` di `dummy-files/` akan di-rename kembali tanpa sufiks `.locked` (asalkan nama target belum dipakai file lain).

## API `GET /api/files`

Contoh elemen (ukuran dihitung dari disk; field `icon`, `originalUrl`, `currentUrl` disertakan agar cocok dengan fungsi `renderFiles` di `file.html`):

```json
[
  {
    "originalName": "employee.docx",
    "currentName": "employee.docx.locked",
    "status": "Encrypted",
    "type": "Word Document",
    "size": "1.2 MB",
    "icon": "DOC",
    "originalUrl": "/dummy-files/employee.docx",
    "currentUrl": "/dummy-files/employee.docx.locked"
  }
]
```

## Catatan

- Tidak ada database; semua data berasal dari isi folder `dummy-files/`.
- Login/signup memakai `localStorage` di sisi klien (`login.js`); backend tidak memverifikasi kredensial.
- Letakkan aset gambar login di `static/images/` sesuai path pada template (mis. `logoBSI.png`, `bsi.png` untuk background CSS).
