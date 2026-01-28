# Setup MySQL XAMPP untuk PBO Application

## Langkah 1: Pastikan XAMPP Terinstall dan MySQL Berjalan

1. Buka XAMPP Control Panel
2. Klik tombol "Start" untuk **Apache** dan **MySQL**
3. Pastikan keduanya menunjukkan status "Running" (hijau)

## Langkah 2: Buat Database MySQL

1. Buka phpMyAdmin melalui browser: `http://localhost/phpmyadmin`
2. Login dengan username: `root` (password kosong)
3. Buat database baru dengan langkah berikut:
   - Klik tab "Databases"
   - Isikan nama database: `pbo_db`
   - Pilih "utf8mb4_unicode_ci" sebagai collation
   - Klik tombol "Create"

## Langkah 3: Install Dependencies Python

Buka terminal/command prompt di folder project dan jalankan:

```bash
pip install -r requirements.txt
```

Atau jika menggunakan pip3:

```bash
pip3 install -r requirements.txt
```

## Langkah 4: Jalankan Aplikasi

Jalankan aplikasi Flask:

```bash
python app.py
```

Aplikasi akan otomatis:
- Membuat semua tabel yang diperlukan di database MySQL
- Mengisi data default (users, operations, room types)
- Siap digunakan

## Langkah 5: Akses Aplikasi

Buka browser dan akses: `http://localhost:5000`

Login dengan credentials default:
- Username: `admin`
- Password: `admin123`

ATAU

- Username: `user`
- Password: `user123`

## Konfigurasi MySQL (Opsional)

Jika ingin mengubah username, password, atau nama database, edit file `config.py`:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'           # Username MySQL
MYSQL_PASSWORD = ''            # Password MySQL (kosong untuk default XAMPP)
MYSQL_DATABASE = 'pbo_db'     # Nama database
```

## Troubleshooting

### Error: "Can't connect to MySQL server"
- Pastikan MySQL sudah dijalankan di XAMPP Control Panel
- Periksa apakah MySQL berjalan di port 3306 (default)

### Error: "Database pbo_db doesn't exist"
- Pastikan sudah membuat database `pbo_db` di phpMyAdmin
- Atau tunggu aplikasi membuat database otomatis saat startup

### Error: "mysql-connector-python not found"
- Jalankan: `pip install mysql-connector-python`

### Tables tidak terbuat otomatis
- Pastikan sudah membuat database `pbo_db` terlebih dahulu
- Jalankan ulang aplikasi: `python app.py`

## Backup Data

Untuk backup database MySQL:

1. Buka phpMyAdmin
2. Pilih database `pbo_db`
3. Klik tab "Export"
4. Pilih format SQL dan klik "Go"

File backup SQL akan tersimpan dan dapat di-import kembali jika diperlukan.
