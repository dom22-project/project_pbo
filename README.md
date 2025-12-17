# Sistem Manajemen PBO - RS Siloam TB Simatupang

Aplikasi desktop untuk mengelola Perkiraan Biaya Operasi (PBO) di Rumah Sakit Sumber Hidup.

## Fitur Utama

- ✅ Input data PBO dengan form lengkap
- ✅ Perhitungan otomatis biaya operasi berdasarkan tabel operasi
- ✅ Perhitungan surcharge untuk operasi CITO dan Penyulit
- ✅ Manajemen data pasien dan operasi
- ✅ Pencarian dan filter data
- ✅ Cetak form PBO
- ✅ Database SQLite untuk penyimpanan data
- ✅ Interface GUI yang user-friendly dengan PyQt5

## Persyaratan Sistem

- Python 3.7 atau lebih tinggi
- Windows/Linux/MacOS
- Minimal 4GB RAM
- 100MB ruang disk kosong

## Instalasi

### 1. Install Python
Pastikan Python 3.7+ sudah terinstall di sistem Anda. Cek dengan:
```bash
python --version
```

### 2. Install Dependencies
Buka terminal/command prompt di folder project, lalu jalankan:
```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install PyQt5
```

### 3. Inisialisasi Database (Opsional)
Jika ingin menambahkan data operasi dari CSV:
```bash
python .vscode/import_data.py
```

## Cara Menjalankan Aplikasi

### Windows
```bash
python .vscode/main.py
```

### Linux/MacOS
```bash
python3 .vscode/main.py
```

## Panduan Penggunaan

### 1. Input Data PBO

1. Buka tab **"Input Data PBO"**
2. Isi form dengan data pasien:
   - Diagnosa
   - Nama Operasi
   - Sifat Operasi (Elektif/CITO/Penyulit)
   - Nama Dokter
   - Kelas Perawatan
3. Pilih Tabel Operasi (1-4) dari dropdown
4. Pilih persentase untuk setiap operasi (100% atau 50%)
5. Isi biaya tambahan jika ada:
   - Konsultasi Pre Tindakan
   - Diagnostic Pre Tindakan
   - Recovery Room Charge
   - Alat, Medical Equipment
   - Obat dan Alkes
6. Klik **"Hitung Total"** untuk menghitung total biaya
7. Klik **"Simpan Data"** untuk menyimpan ke database

### 2. Pencarian Data

1. Buka tab **"Cari Data PBO"**
2. Pilih kriteria pencarian (Nama Pasien, Nama Operasi, dll)
3. Masukkan kata kunci
4. Klik **"Cari"**
5. Double-click pada baris untuk melihat detail lengkap

### 3. Cetak Form

- Dari tab Input: Klik **"Cetak Form"** untuk mencetak form yang sedang diisi
- Dari tab Pencarian: Pilih data, lalu klik **"Cetak Data Terpilih"**

### 4. Hapus Data

1. Buka tab **"Cari Data PBO"**
2. Pilih data yang ingin dihapus
3. Klik **"Hapus Data Terpilih"**
4. Konfirmasi penghapusan

## Perhitungan Biaya

### Biaya Dokter (Surgeon)
- Dihitung dari Tabel Operasi yang dipilih
- Dikalikan dengan persentase (100% atau 50%)
- Ditambah surcharge sesuai sifat operasi:
  - Elektif: 0% (1.0x)
  - CITO: 25% (1.25x)
  - Penyulit: 30% (1.30x)

### Biaya Anesthesi
- Dihitung dari Tabel Operasi (biaya RS)
- Dikalikan dengan persentase
- Ditambah surcharge yang sama dengan surgeon

### OT Room Charge
- 30% dari biaya surgeon (sudah termasuk surcharge)

### Tarif Kamar per Hari
Otomatis terisi berdasarkan kelas:
- BASIC: Rp 350.000
- STANDARD: Rp 650.000
- DELUXE: Rp 900.000
- VIP: Rp 1.800.000
- VVIP: Rp 1.900.000
- SUITE: Rp 5.000.000
- PRESIDENTIAL SUITE: Rp 7.500.000
- ODC: Rp 500.000

### Total Biaya
Penjumlahan dari semua komponen biaya di atas.

## Struktur Database

### Tabel: database
Menyimpan data PBO lengkap dengan semua field form.

### Tabel: operation_tables
Menyimpan master data tabel operasi dengan:
- Kode operasi
- Nama tindakan
- Kelas
- Biaya dokter
- Biaya RS
- Total biaya

## Troubleshooting

### Error: "No module named 'PyQt5'"
**Solusi:** Install PyQt5 dengan `pip install PyQt5`

### Error: "Unable to open database file"
**Solusi:** Pastikan folder `data/` ada dan memiliki permission write

### Aplikasi tidak muncul
**Solusi:** 
1. Cek apakah Python terinstall dengan benar
2. Pastikan PyQt5 terinstall
3. Jalankan dari terminal untuk melihat error message

### Data tidak tersimpan
**Solusi:**
1. Pastikan field "Nama Pasien" terisi
2. Cek permission folder `data/`
3. Lihat error message yang muncul

## File Penting

```
app pbo/
├── .vscode/
│   ├── main.py           # File utama aplikasi
│   ├── database.py       # Helper functions database
│   ├── import_data.py    # Import data dari CSV
│   └── coba1.py          # Backup file
├── data/
│   └── pbo_database.db   # Database SQLite
├── requirements.txt      # Dependencies
├── README.md            # Dokumentasi ini
└── TODO.md              # Task list
```

## Pengembangan Lebih Lanjut

Fitur yang bisa ditambahkan:
- [ ] Export ke Excel/PDF
- [ ] Laporan statistik
- [ ] Backup/restore database
- [ ] Multi-user dengan login
- [ ] Integrasi dengan sistem RS lainnya

## Kontak & Support

Untuk pertanyaan atau bantuan:
- Email: support@rssumberhidup.com
- Telp: (021) 29531900 Ext. 29790

## Lisensi

© 2024 RS Siloam TB Simatupang. All rights reserved.

---

**Versi:** 1.0.0  
**Terakhir diupdate:** 2024
