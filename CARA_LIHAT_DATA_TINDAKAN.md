# Cara Melihat Data Tindakan yang Sudah Masuk ke Aplikasi

## 🎯 Ringkasan Cepat

Setelah mengupload file Excel dengan sheet "db nama tindakan", Anda dapat melihat data yang sudah masuk melalui **3 cara**:

---

## 📱 Cara 1: Melalui Web Interface (PALING MUDAH)

### Langkah-langkah:

1. **Buka aplikasi web**
   ```
   http://localhost:5000
   ```

2. **Klik menu "Database" di navigation bar**
   - Menu dropdown akan muncul

3. **Pilih "Lihat Data Tindakan"**
   - Anda akan diarahkan ke halaman daftar tindakan

4. **Lihat data yang sudah masuk**
   - Tabel interaktif dengan fitur pencarian
   - Sorting berdasarkan kolom
   - Pagination (25 data per halaman)
   - Total: **2,131 tindakan items**

### Fitur di Halaman View Tindakan:

✅ **Tabel Interaktif**
- Pencarian real-time
- Sort by kolom (klik header tabel)
- Pagination otomatis

✅ **Informasi Lengkap**
- Nama Tindakan
- Kelas (BASIC, VIP, dll)
- Kategory
- Sales Item Type
- Amount (harga)

✅ **Detail Modal**
- Klik tombol 👁️ untuk melihat detail lengkap
- Informasi created_at

✅ **Statistik**
- Total tindakan items di database
- Info sheet sumber data

---

## 💻 Cara 2: Melalui Command Line (Python Script)

### Opsi A: Menggunakan Test Script

```bash
python test_tindakan_import.py
```

**Output yang ditampilkan:**
```
============================================================
TEST 2: Hitung Data Tindakan Items
============================================================
Total tindakan items di database: 2131
✓ Berhasil menemukan 2131 tindakan items

============================================================
TEST 3: Ambil Sample Data Tindakan Items
============================================================
✓ Berhasil mengambil 2131 tindakan items

Sample data (5 pertama):
------------------------------------------------------------

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
...
```

### Opsi B: Menggunakan Python Interactive

```python
from models import Database

# Initialize database
db = Database()

# Hitung total data
total = db.count_tindakan_items()
print(f"Total tindakan items: {total}")

# Ambil semua data
items = db.get_all_tindakan_items()

# Tampilkan 10 data pertama
for i, item in enumerate(items[:10], 1):
    print(f"\n{i}. {item['nama_tindakan']}")
    print(f"   Kelas: {item['kelas']}")
    print(f"   Kategory: {item['kategory']}")
    print(f"   Amount: Rp {item['amount']:,.0f}")
```

---

## 🗄️ Cara 3: Melalui Database Viewer (SQLite)

### Menggunakan DB Browser for SQLite:

1. **Download DB Browser for SQLite**
   - https://sqlitebrowser.org/

2. **Buka database file**
   ```
   data/pbo_database.db
   ```

3. **Pilih tabel "tindakan_items"**
   - Klik tab "Browse Data"
   - Pilih tabel: `tindakan_items`

4. **Lihat semua data**
   - Semua 2,131 records akan ditampilkan
   - Bisa export ke CSV/Excel

### Query SQL Manual:

```sql
-- Hitung total data
SELECT COUNT(*) as total FROM tindakan_items;

-- Lihat 10 data pertama
SELECT * FROM tindakan_items LIMIT 10;

-- Cari berdasarkan nama tindakan
SELECT * FROM tindakan_items 
WHERE nama_tindakan LIKE '%ABLASI%';

-- Group by kelas
SELECT kelas, COUNT(*) as jumlah 
FROM tindakan_items 
GROUP BY kelas;

-- Group by kategory
SELECT kategory, COUNT(*) as jumlah 
FROM tindakan_items 
GROUP BY kategory 
ORDER BY jumlah DESC;
```

---

## 📊 Informasi Data yang Tersimpan

### Struktur Tabel `tindakan_items`:

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| id | INTEGER | Primary key (auto increment) |
| nama_tindakan | TEXT | Nama tindakan medis |
| kelas | TEXT | Kelas layanan (BASIC, VIP, dll) |
| kategory | TEXT | Kategori tindakan |
| sales_item_type | TEXT | Tipe item penjualan |
| amount | REAL | Biaya/harga |
| created_at | TIMESTAMP | Waktu data dibuat |

### Statistik Data Anda:

- **Total Records**: 2,131 tindakan items
- **Sumber Data**: Sheet "db nama tindakan" dari file `data/db pbo.xlsx`
- **Status Import**: ✅ Berhasil 100% (0 data dilewati)

---

## 🔍 Cara Mencari Data Spesifik

### Di Web Interface:

1. Buka halaman "Lihat Data Tindakan"
2. Gunakan kotak pencarian di kanan atas tabel
3. Ketik nama tindakan, kelas, atau kategory
4. Hasil akan difilter secara real-time

### Contoh Pencarian:

- Cari "ABLASI" → Menampilkan semua tindakan ABLASI
- Cari "BASIC" → Menampilkan semua kelas BASIC
- Cari "CONSULTATION" → Menampilkan semua tipe konsultasi

---

## ✅ Verifikasi Data Sudah Masuk

### Checklist Verifikasi:

- [ ] Total tindakan items = 2,131 ✅
- [ ] Data bisa dilihat di web interface ✅
- [ ] Tabel interaktif berfungsi (search, sort, pagination) ✅
- [ ] Detail modal bisa dibuka ✅
- [ ] Data sesuai dengan file Excel ✅

### Jika Data Tidak Muncul:

1. **Cek apakah import berhasil**
   ```bash
   python test_tindakan_import.py
   ```

2. **Cek file database ada**
   ```bash
   ls -la data/pbo_database.db
   ```

3. **Re-import data**
   ```bash
   python import_excel_data.py
   ```

4. **Restart aplikasi Flask**
   - Stop aplikasi (Ctrl+C)
   - Jalankan lagi: `python app.py`

---

## 🎨 Screenshot Lokasi Menu

```
Navigation Bar:
┌─────────────────────────────────────────────────────┐
│ [Logo] Dashboard | Input PBO | Cari Data | Database ▼│
│                                              ↓        │
│                                    ┌─────────────────┤
│                                    │ Upload Database │
│                                    │ Lihat Data      │ ← KLIK INI
│                                    │   Tindakan      │
│                                    └─────────────────┘
└─────────────────────────────────────────────────────┘
```

---

## 📞 Troubleshooting

### Problem: Menu "Lihat Data Tindakan" tidak muncul

**Solusi:**
1. Refresh browser (F5)
2. Clear cache browser
3. Restart aplikasi Flask

### Problem: Tabel kosong / tidak ada data

**Solusi:**
1. Jalankan test: `python test_tindakan_import.py`
2. Jika test gagal, re-import: `python import_excel_data.py`
3. Cek file Excel memiliki sheet "db nama tindakan"

### Problem: Error saat membuka halaman

**Solusi:**
1. Cek aplikasi Flask berjalan
2. Cek URL: `http://localhost:5000/view-tindakan`
3. Lihat error di terminal Flask

---

## 🎯 Kesimpulan

**Cara Tercepat Melihat Data:**

1. Buka browser → `http://localhost:5000`
2. Klik menu "Database" → "Lihat Data Tindakan"
3. Lihat 2,131 tindakan items yang sudah masuk!

**URL Langsung:**
```
http://localhost:5000/view-tindakan
```

---

**Selamat! Data tindakan Anda sudah berhasil masuk ke sistem! 🎉**
