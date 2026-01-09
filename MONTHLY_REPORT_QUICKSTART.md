# 📊 MONTHLY REPORT FEATURE - QUICK START GUIDE

## ✨ Apa itu Monthly Report?

Monthly Report adalah dashboard bulanan yang menampilkan ringkasan semua operasi dalam sebuah bulan tertentu dengan informasi:
- **Nama Operasi** - Jenis prosedur medis
- **Nama Dokter** - Dokter yang melakukan operasi
- **Perusahaan/Asuransi** - Pihak yang menanggung biaya

## 🚀 Cara Akses

### Method 1: Dari Menu Navigasi
```
Klik: Menu Navigasi > Laporan Bulanan
```

### Method 2: Dari Dashboard
```
Klik: Dashboard > Aksi Cepat > Laporan Bulanan
```

### Method 3: Direct URL
```
http://localhost:5000/monthly-report
```

## 📋 Langkah-Langkah Penggunaan

### 1️⃣ Login ke Aplikasi
- Username: `admin`
- Password: `admin123`

### 2️⃣ Pilih Bulan dan Tahun
```
┌─────────────────────────┐
│ Pilih Bulan & Tahun     │
├─────────────────────────┤
│ [Januari 2026] ▼        │ ← Click untuk pilih bulan
│ [2026]        ↔ Tahun   │ ← Sesuaikan tahun jika perlu
│ [Tampilkan Data]        │ ← Click untuk update laporan
└─────────────────────────┘
```

### 3️⃣ Lihat Statistik
```
┌──────────────┬──────────────┬─────────────┬──────────────┐
│ Total Operasi│ Total Denda  │ Dokter Unik │ Asuransi Unik│
├──────────────┼──────────────┼─────────────┼──────────────┤
│ 15           │ Rp 2.5M      │ 8           │ 5            │
└──────────────┴──────────────┴─────────────┴──────────────┘
```

### 4️⃣ Lihat Tabel Detail
| No | Tanggal | Nama Operasi | Nama Dokter | Asuransi | Kelas | Total |
|:--:|:-------:|:-----:|:------:|:---:|:---:|:---:|
| 1 | 01/01/2026 | Operasi ABC | Dr. Budi | Asuransi A | VIP | Rp 500K |
| 2 | 02/01/2026 | Operasi XYZ | Dr. Andi | Asuransi B | 1 | Rp 300K |

**Klik ikon mata** di kolom Aksi untuk lihat detail lengkap

### 5️⃣ Export Data (Optional)
**Ada 2 pilihan:**

**A. Export ke CSV** (Untuk Excel)
```
Klik: [Export CSV]
File akan otomatis diunduh dengan nama:
laporan_Januari_2026.csv
```
Buka file dengan:
- Microsoft Excel
- Google Sheets
- LibreOffice Calc

**B. Export ke PDF** (Untuk Print/Share)
```
Klik: [Cetak]
Di dialog Print:
  - Pilih printer: "Save as PDF"
  - Klik: Save
```

## 📊 Informasi yang Ditampilkan

### Statistik Ringkasan
| Statistik | Penjelasan | Contoh |
|-----------|-----------|--------|
| Total Operasi | Berapa banyak operasi dalam bulan | 15 operasi |
| Total Pendapatan | Jumlah semua biaya operasi | Rp 2.500.000 |
| Dokter Unik | Berapa dokter berbeda yang melakukan operasi | 8 dokter |
| Asuransi Unik | Berapa asuransi/perusahaan berbeda | 5 asuransi |

### Tabel Detail
Setiap baris menampilkan:
- **Tanggal**: Tanggal operasi (format: DD/MM/YYYY)
- **Nama Operasi**: Jenis prosedur medis
- **Nama Dokter**: Dokter yang melakukan (dalam badge biru)
- **Perusahaan/Asuransi**: Pihak penanggung (dalam badge kuning)
- **Kelas**: Klasifikasi operasi (VIP, 1, 2, 3, dll)
- **Total Biaya**: Biaya operasi (format: Rp. XXXXX)

## 💡 Tips & Trik

### Tip 1: Tracking Produktivitas Dokter
```
Bulan Januari:
- Dr. Budi: 8 operasi
- Dr. Andi: 5 operasi
- Dr. Citra: 2 operasi
⟹ Dr. Budi paling produktif
```

### Tip 2: Tracking Klien Asuransi
```
Bulan Januari:
- Asuransi A: 7 operasi
- Asuransi B: 5 operasi
- Asuransi C: 3 operasi
⟹ Asuransi A klien terbesar
```

### Tip 3: Analisis Revenue
```
Total Revenue = Total Pendapatan dari semua operasi
⟹ Bandingkan dengan bulan sebelumnya
⟹ Lihat trend kenaikan/penurunan
```

### Tip 4: Export Bulanan
```
Setiap akhir bulan:
1. Buka Monthly Report
2. Pilih bulan sebelumnya
3. Export ke CSV
4. Simpan sebagai archieve
⟹ Dokumentasi lengkap per bulan
```

## ❓ FAQ (Frequently Asked Questions)

### Q: Mengapa data tidak muncul?
**A:** Pastikan:
- ✓ Data sudah di-input dalam aplikasi
- ✓ Data memiliki tanggal yang valid
- ✓ Anda memilih bulan yang benar

### Q: Bisa nggak lihat laporan tahun lalu?
**A:** Bisa! Gunakan dropdown untuk pilih bulan/tahun yang ada data-nya.

### Q: Export CSV buat apa?
**A:** Untuk:
- Analisis lebih mendalam di Excel
- Membuat grafik/chart
- Backup data
- Share dengan kolega

### Q: Bisa print langsung tanpa PDF?
**A:** Bisa! Klik tombol "Cetak" → Gunakan printer fisik biasa

### Q: Kenapa kolom "Asuransi" ada yang kosong?
**A:** Operasi tersebut tidak punya asuransi (pasien umum/swasta)

## 🔍 Contoh Penggunaan

### Scenario 1: Laporan Harian Rutin
```
Waktu: Setiap hari kerja pukul 16.00
Proses:
1. Login ke aplikasi
2. Klik Laporan Bulanan
3. Dashboard otomatis menampilkan bulan sekarang
4. Lihat progress operasi bulan ini
5. Logout
```

### Scenario 2: Laporan Bulanan ke Manajemen
```
Waktu: Akhir bulan
Proses:
1. Klik Laporan Bulanan
2. Pastikan bulan yang dipilih benar
3. Klik Export CSV
4. Buka file di Excel
5. Tambahkan grafik/analisis
6. Send ke manager
```

### Scenario 3: Cek Operasi Dokter Tertentu
```
Proses:
1. Klik Laporan Bulanan
2. Lihat tabel
3. Cari nama dokter di kolom "Nama Dokter"
4. Hitung/scroll berapa banyak operasi dari dokter itu
5. Atau export CSV dan filter di Excel
```

## ⚙️ Teknis (Developer Info)

### Database Queries
```python
# Query 1: Get data operasi per bulan
SELECT * FROM database 
WHERE YEAR(tanggal) = 2026 AND MONTH(tanggal) = 1
  AND is_latest = 1
ORDER BY tanggal DESC

# Query 2: Get list bulan yang punya data
SELECT YEAR(tanggal), MONTH(tanggal), COUNT(*)
FROM database
WHERE tanggal IS NOT NULL AND is_latest = 1
GROUP BY YEAR(tanggal), MONTH(tanggal)
```

### Endpoint
```
GET /monthly-report?year=2026&month=1
```

### Files
- Backend: `models.py` (2 functions baru)
- Backend: `app.py` (1 route baru)
- Frontend: `templates/monthly_report.html` (template baru)

## 🎓 Troubleshooting

### Problem: "Tidak Ada Data" muncul
**Solution:**
1. Pastikan sudah input data operasi
2. Pastikan data punya tanggal (jangan kosong)
3. Pilih bulan yang benar di dropdown
4. Refresh page (F5)

### Problem: Export CSV tidak work
**Solution:**
1. Pastikan browser allow download
2. Check folder Downloads
3. Coba browser lain (Chrome/Firefox)
4. Clear browser cache

### Problem: Total revenue tidak akurat
**Solution:**
1. Pastikan semua data punya "Total" biaya
2. Edit data yang kosong di bagian "Total"
3. Refresh page untuk lihat perubahan

### Problem: Dokter/Asuransi salah
**Solution:**
1. Klik mata → Edit → Perbaiki
2. Save
3. Kembali ke laporan bulanan

## 📚 Dokumentasi Lengkap

Untuk dokumentasi lebih detail, lihat:
- `MONTHLY_REPORT_GUIDE.md` - Panduan lengkap pengguna
- `MONTHLY_REPORT_IMPLEMENTATION.md` - Info teknis implementasi

## 🆘 Support

Jika ada pertanyaan atau masalah:
1. Baca FAQ di atas
2. Cek troubleshooting
3. Lihat dokumentasi lengkap
4. Hubungi IT Support

---

**Selamat menggunakan Monthly Report Dashboard! 🎉**
