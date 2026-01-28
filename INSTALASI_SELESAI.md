# ✅ Setup Selesai - Database MySQL XAMPP

## Status Instalasi

✅ **Dependencies sudah diinstall dengan sukses!**

Semua package Python telah terinstall di virtual environment:
- Flask 3.0.0
- SQLAlchemy 2.0.45
- MySQL Connector Python 8.2.0
- dan semua dependencies lainnya

## Mengapa Error Connection MySQL?

Error `Can't connect to MySQL server on 'localhost:3306'` itu **NORMAL** karena:
- MySQL server XAMPP **belum dijalankan**
- Database `pbo_db` **belum dibuat di phpMyAdmin**

## Langkah Berikutnya - Setup Database

### 1️⃣ Start MySQL di XAMPP Control Panel

1. Buka **XAMPP Control Panel**
2. Klik tombol **"Start"** untuk **Apache** dan **MySQL**
3. Tunggu hingga status menunjukkan "Running" (hijau)

```
[✓] Apache   - Running
[✓] MySQL    - Running
```

### 2️⃣ Buat Database di phpMyAdmin

1. Buka browser: http://localhost/phpmyadmin
2. Login dengan:
   - Username: `root`
   - Password: (kosong / biarkan blank)
3. Buat database baru:
   - Klik tab "Databases"
   - Ketik nama: `pbo_db`
   - Collation: `utf8mb4_unicode_ci`
   - Klik "Create"

### 3️⃣ Jalankan Aplikasi

Buka terminal di folder project dan jalankan:

```bash
.venv/Scripts/python.exe app.py
```

Atau gunakan shortcut:

```bash
python app.py
```

**Output yang benar:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 4️⃣ Akses Aplikasi

Buka browser: **http://localhost:5000**

Login dengan:
- **Username:** admin
- **Password:** admin123

atau

- **Username:** user
- **Password:** user123

## Konfigurasi MySQL (File: config.py)

Jika ingin mengubah user/password MySQL, edit file `config.py`:

```python
MYSQL_HOST = 'localhost'      # Host MySQL
MYSQL_USER = 'root'            # Username MySQL
MYSQL_PASSWORD = ''            # Password (kosong untuk XAMPP default)
MYSQL_DATABASE = 'pbo_db'      # Nama database
```

## Troubleshooting

### ❌ "Can't connect to MySQL server"

**Solusi:**
- ✅ Pastikan MySQL sudah di-start di XAMPP Control Panel
- ✅ Pastikan MySQL berjalan di port 3306 (default)
- ✅ Periksa username/password di config.py

### ❌ "Database pbo_db doesn't exist"

**Solusi:**
- ✅ Buat database `pbo_db` di phpMyAdmin terlebih dahulu
- ✅ Pastikan collation: `utf8mb4_unicode_ci`

### ❌ "Module not found" errors

**Solusi:**
```bash
# Pastikan virtual environment aktif
.venv/Scripts/activate

# Install ulang requirements
pip install -r requirements.txt
```

## Backup Database

Untuk backup data MySQL:

1. Buka phpMyAdmin: http://localhost/phpmyadmin
2. Pilih database `pbo_db`
3. Klik tab "Export"
4. Format: **SQL**
5. Klik "Go"

File SQL akan di-download dan bisa di-import kembali kapan saja.

## File Penting

- `config.py` - Konfigurasi MySQL
- `requirements.txt` - List dependencies Python
- `app.py` - Main aplikasi Flask
- `models_sqlalchemy.py` - Model database

---

**Status:** ✅ Ready to Run!

Setelah MySQL XAMPP dijalankan dan database dibuat, aplikasi siap digunakan!
