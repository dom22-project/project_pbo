# Panduan Import Data Tindakan Items

## Deskripsi

Fitur ini memungkinkan import data tindakan items dari sheet "db nama tindakan" di file Excel. Data ini mencakup informasi detail tentang berbagai tindakan medis dengan kategori, tipe, dan biaya.

## Struktur Data

### Sheet "db nama tindakan"

File Excel harus memiliki sheet dengan nama **"db nama tindakan"** dengan struktur kolom sebagai berikut:

| Kolom | Posisi | Deskripsi | Contoh |
|-------|--------|-----------|--------|
| Nama Tindakan | B | Nama tindakan medis | ABLASI 3D |
| Kelas | C | Kelas layanan | BASIC, VIP, dll |
| Kategory | D | Kategori tindakan | Konsultasi Pre Tindakan, Obat dan Alkes |
| Sales Item Type | E | Tipe item penjualan | CONSULTATION AND VISIT, DRUGS, dll |
| AMOUNT | F | Biaya/harga | 1000000 |

**Catatan:** Kolom A biasanya kosong atau berisi nomor urut.

## Tabel Database

Data akan disimpan di tabel `tindakan_items` dengan struktur:

```sql
CREATE TABLE tindakan_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_tindakan TEXT,
    kelas TEXT,
    kategory TEXT,
    sales_item_type TEXT,
    amount REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Cara Menggunakan

### 1. Via Script Import (Command Line)

```bash
python import_excel_data.py
```

Script ini akan:
- Import data dari sheet "db table operasi"
- Import data dari sheet "db nama dokter"
- Import data dari sheet "db nama tindakan" (BARU!)

Output contoh:
```
============================================================
Importing Tindakan Items from 'db nama tindakan' sheet...
============================================================
Clearing existing tindakan items...

Tindakan Items Import Summary:
  - Successfully imported: 2131 items
  - Skipped: 0 rows

============================================================
Import Complete!
============================================================

✓ All data imported successfully!

Database Statistics:
  - Total operations: 1234
  - Total doctors: 56
  - Total tindakan items: 2131
```

### 2. Via Web Interface

1. Buka aplikasi web: `http://localhost:5000`
2. Klik menu **"Upload Database"** atau tombol **"Upload Database Terbaru"**
3. Pilih file Excel (.xlsx) yang berisi sheet "db nama tindakan"
4. Klik **"Upload & Import Database"**
5. Sistem akan menampilkan ringkasan import termasuk statistik tindakan items

## Fungsi API (models.py)

### 1. `add_tindakan_item(nama_tindakan, kelas, kategory, sales_item_type, amount)`
Menambahkan data tindakan item baru.

**Parameter:**
- `nama_tindakan` (str): Nama tindakan
- `kelas` (str): Kelas layanan
- `kategory` (str): Kategori tindakan
- `sales_item_type` (str): Tipe item penjualan
- `amount` (float): Biaya/harga

**Return:** ID item yang baru ditambahkan

**Contoh:**
```python
from models import Database

db = Database()
item_id = db.add_tindakan_item(
    nama_tindakan="ABLASI 3D",
    kelas="BASIC",
    kategory="Konsultasi Pre Tindakan",
    sales_item_type="CONSULTATION AND VISIT",
    amount=1000000
)
print(f"Item ID: {item_id}")
```

### 2. `get_all_tindakan_items()`
Mengambil semua data tindakan items.

**Return:** List of dictionaries

**Contoh:**
```python
items = db.get_all_tindakan_items()
for item in items:
    print(f"{item['nama_tindakan']} - Rp {item['amount']:,.0f}")
```

### 3. `delete_all_tindakan_items()`
Menghapus semua data tindakan items (biasanya sebelum import baru).

**Contoh:**
```python
db.delete_all_tindakan_items()
print("Semua tindakan items telah dihapus")
```

### 4. `count_tindakan_items()`
Menghitung total tindakan items di database.

**Return:** Integer (jumlah items)

**Contoh:**
```python
count = db.count_tindakan_items()
print(f"Total tindakan items: {count}")
```

## Validasi Data

### Data yang Akan Diimport:
- ✅ Baris dengan `nama_tindakan` yang valid
- ✅ Kolom lain boleh kosong (akan diisi string kosong atau 0)

### Data yang Akan Dilewati:
- ❌ Baris kosong (semua kolom kosong)
- ❌ Baris tanpa `nama_tindakan`

## Testing

Untuk memverifikasi import berhasil, jalankan:

```bash
python test_tindakan_import.py
```

Test yang dilakukan:
1. ✓ Verifikasi tabel database
2. ✓ Verifikasi struktur tabel
3. ✓ Verifikasi file Excel dan sheet
4. ✓ Hitung data tindakan
5. ✓ Ambil sample data
6. ✓ Test fungsi add

## Contoh Data

Berikut contoh data yang berhasil diimport:

```
1. ABLASI 3D
   Kelas: BASIC
   Kategory: Konsultasi Pre Tindakan
   Sales Item Type: CONSULTATION AND VISIT
   Amount: Rp 1,000,000

2. ABLASI 3D
   Kelas: BASIC
   Kategory: Diagnostic Pre Tindakan
   Sales Item Type: LABORATORY
   Amount: Rp 3,659,000

3. ABLASI 3D
   Kelas: BASIC
   Kategory: Obat dan Alkes
   Sales Item Type: DRUGS
   Amount: Rp 10,742,650
```

## Statistik Import

Setelah import berhasil, sistem akan menampilkan:

### Via Command Line:
```
Tindakan Items Import Summary:
  - Successfully imported: 2131 items
  - Skipped: 0 rows
```

### Via Web Interface:
- **Data Tindakan Items**
  - Berhasil Diimport: 2131
  - Dilewati: 0
- **Total Tindakan Items**: 2131

## Troubleshooting

### Error: "Sheet 'db nama tindakan' not found"
**Solusi:** Pastikan file Excel memiliki sheet dengan nama persis "db nama tindakan" (huruf kecil semua, dengan spasi).

### Data tidak muncul setelah import
**Solusi:**
1. Periksa apakah sheet ada di file Excel
2. Periksa apakah ada data di sheet (minimal 1 baris selain header)
3. Jalankan test: `python test_tindakan_import.py`

### Import berhasil tapi jumlah data tidak sesuai
**Solusi:**
1. Periksa baris yang dilewati (skipped)
2. Pastikan kolom `nama_tindakan` (kolom B) tidak kosong
3. Periksa format data di Excel

## File yang Dimodifikasi

1. **models.py**
   - Tambah tabel `tindakan_items`
   - Tambah fungsi CRUD untuk tindakan items

2. **import_excel_data.py**
   - Tambah fungsi `import_tindakan_from_excel()`
   - Update fungsi `main()` untuk include import tindakan

3. **app.py**
   - Update fungsi `import_excel_to_database()` untuk import tindakan
   - Update statistik di route `/upload-database`

4. **templates/upload_success.html**
   - Tambah section untuk statistik tindakan items
   - Update layout untuk menampilkan 3 kategori data

## Changelog

### Version 1.0 (2024)
- ✅ Implementasi tabel `tindakan_items`
- ✅ Fungsi import dari sheet "db nama tindakan"
- ✅ Integrasi dengan web upload interface
- ✅ Test suite lengkap
- ✅ Dokumentasi

## Support

Jika mengalami masalah:
1. Jalankan test: `python test_tindakan_import.py`
2. Periksa log error di terminal
3. Verifikasi struktur file Excel
4. Hubungi administrator sistem

---

**Catatan Penting:** 
- Import akan menghapus data lama dan menggantinya dengan data baru
- Backup database otomatis dibuat sebelum import
- File backup tersimpan di folder `backups/`
