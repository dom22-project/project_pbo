# Laporan Bulanan (Monthly Report Dashboard)

## Deskripsi Fitur
Fitur Laporan Bulanan adalah dashboard interaktif untuk melihat ringkasan data operasi setiap bulannya. Dengan fitur ini, Anda dapat melihat semua data operasi yang dilakukan dalam bulan tertentu dengan informasi penting seperti:

- **Nama Operasi** - Jenis tindakan medis yang dilakukan
- **Nama Dokter** - Dokter yang melakukan operasi
- **Perusahaan/Asuransi Penanggung** - Pihak asuransi atau perusahaan yang menanggung biaya

## Fitur-Fitur Utama

### 1. Statistik Ringkasan
Di bagian atas dashboard, Anda akan melihat 4 kartu statistik:
- **Total Operasi**: Jumlah operasi yang dilakukan dalam bulan tersebut
- **Total Pendapatan**: Jumlah total biaya operasi dalam bulan tersebut
- **Dokter Unik**: Jumlah dokter yang melakukan operasi
- **Asuransi Unik**: Jumlah perusahaan/asuransi yang berbeda

### 2. Pemilihan Bulan dan Tahun
Gunakan dropdown untuk memilih bulan dan tahun yang ingin dilihat. Sistem akan menampilkan hanya bulan-bulan yang memiliki data.

### 3. Tabel Detail
Tabel menampilkan informasi lengkap setiap operasi dengan kolom:
| No | Tanggal | Nama Operasi | Nama Dokter | Perusahaan/Asuransi | Kelas | Total Biaya | Aksi |
|:--:|:-------:|:------------:|:-----------:|:------------------:|:-----:|:-----------:|:----:|

### 4. Fitur Ekspor
Anda dapat mengekspor data laporan dalam format:
- **CSV**: File yang dapat dibuka di Excel/Spreadsheet
- **PDF**: Melalui fitur Print (Ctrl+P)

### 5. Aksi Cepat
Dari setiap baris, Anda dapat:
- Klik ikon mata untuk melihat detail lengkap operasi

## Cara Menggunakan

### Mengakses Laporan Bulanan
1. Klik menu "Laporan Bulanan" di navbar
2. Atau dari Dashboard, klik tombol "Laporan Bulanan" di bagian Aksi Cepat

### Menampilkan Data Bulan Tertentu
1. Gunakan dropdown "Pilih Bulan & Tahun"
2. Dropdown menampilkan bulan-bulan yang memiliki data lengkap dengan jumlah record
3. Klik "Tampilkan Data" atau dropdown akan otomatis update

### Melihat Detail Operasi
1. Di tabel, klik ikon mata di kolom "Aksi"
2. Anda akan diarahkan ke halaman detail operasi lengkap

### Mengekspor Laporan
1. **Export CSV**:
   - Klik tombol "Export CSV" di bagian "Opsi Ekspor"
   - File CSV akan terunduh dengan nama `laporan_[BULAN]_[TAHUN].csv`
   - File dapat dibuka di Microsoft Excel atau Google Sheets

2. **Export PDF**:
   - Klik tombol "Cetak" di bagian header
   - Browser akan membuka dialog print
   - Ubah tujuan printer ke "Save as PDF"
   - Klik "Save"

## Database Query

Fitur ini menggunakan 2 query utama:

### 1. `get_monthly_report(year, month)`
Mengambil semua data operasi untuk bulan dan tahun tertentu dengan filter:
- Hanya menampilkan data terbaru (is_latest = 1)
- Diurutkan berdasarkan tanggal terbaru
- Mengembalikan: nama_operasi, nama_dokter, perusahaan_asuransi, tanggal, kelas, total biaya

### 2. `get_available_months()`
Mengambil daftar bulan-bulan yang memiliki data dengan informasi:
- Tahun dan bulan yang tersedia
- Jumlah record untuk setiap bulan
- Diurutkan dari bulan terbaru ke tertua

## Struktur File

```
app.py
├── Route: /monthly-report (GET)
│   └── Function: monthly_report()
│       - Mengambil available_months
│       - Mengambil report_data untuk bulan yang dipilih
│       - Menghitung statistik
│       - Render template

models.py
├── get_monthly_report(year, month)
│   └── Query data operasi per bulan
├── get_available_months()
    └── Query daftar bulan yang tersedia

templates/monthly_report.html
├── Header dengan statistik
├── Month selector
├── Report table
└── Export options
```

## Catatan Penting

1. **Data yang Ditampilkan**: Hanya data operasi terbaru (versi terbaru) yang ditampilkan
2. **Filter Tanggal**: Jika data tidak memiliki tanggal, data tidak akan muncul di laporan bulanan
3. **Format Mata Uang**: Semua nilai ditampilkan dalam format Rupiah (Rp.)
4. **Responsif**: Dashboard dapat diakses dari desktop, tablet, dan mobile
5. **Print Friendly**: Layout otomatis menyembunyikan elemen yang tidak perlu saat print

## Tips Penggunaan

1. **Untuk Audit Bulanan**: Export ke CSV dan buka di Excel untuk analisis lebih lanjut
2. **Untuk Presentasi**: Gunakan fitur Print dan simpan sebagai PDF
3. **Tracking Dokter**: Gunakan kolom Dokter untuk melihat produktivitas dokter per bulan
4. **Tracking Asuransi**: Gunakan kolom Asuransi untuk melihat klien asuransi yang paling banyak
5. **Verifikasi Revenue**: Total Pendapatan menunjukkan revenue operasional bulan tersebut

## Troubleshooting

**Q: Data tidak muncul di laporan bulan tertentu?**
A: Pastikan:
- Data tersebut punya tanggal yang valid
- Data adalah versi terbaru (bukan versi lama yang sudah di-edit)
- Filter tanggal tepat dengan bulan/tahun yang dipilih

**Q: Dropdown bulan kosong?**
A: Belum ada data operasi dalam sistem. Input beberapa data operasi terlebih dahulu.

**Q: Export CSV tidak berfungsi?**
A: Coba gunakan browser yang berbeda atau clear cache browser Anda.

---
Fitur ini memudahkan Anda untuk membuat laporan operasional bulanan dengan cepat dan akurat!
