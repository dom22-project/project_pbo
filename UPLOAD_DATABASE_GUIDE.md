# Panduan Upload Database

## Deskripsi Fitur

Fitur Upload Database memungkinkan Anda untuk memperbarui data operasi dan dokter dengan mudah melalui interface web. Fitur ini menggantikan cara manual menggunakan script `import_excel_data.py`.

## Fitur Utama

### 1. **Upload File Excel**
- Upload file Excel (.xlsx) langsung dari browser
- Validasi otomatis format dan struktur file
- Ukuran maksimal: 16 MB

### 2. **Backup Otomatis**
- Database lama akan di-backup secara otomatis sebelum import
- Backup disimpan di folder `backups/` dengan timestamp
- Format nama: `pbo_database_backup_YYYYMMDD_HHMMSS.db`

### 3. **Import Data**
- Import data operasi dari sheet "db table operasi"
- Import data dokter dari sheet "db nama dokter"
- Data lama akan diganti dengan data baru

### 4. **Laporan Import**
- Statistik lengkap hasil import
- Jumlah data berhasil diimport
- Jumlah data yang dilewati
- Total data di database setelah import

## Cara Menggunakan

### Langkah 1: Persiapan File Excel

Pastikan file Excel Anda memiliki struktur yang benar:

#### Sheet "db table operasi"
Kolom yang diperlukan (mulai dari kolom B):
- **Kolom B**: Fee Operator (Nama Tindakan)
- **Kolom C**: Kelas
- **Kolom D**: Harga Operator (Biaya Dokter)
- **Kolom E**: Harga Anestesi (Biaya RS)

#### Sheet "db nama dokter"
Kolom yang diperlukan:
- **Kolom B**: Nama Dokter

### Langkah 2: Akses Halaman Upload

Ada 3 cara untuk mengakses halaman upload:

1. **Dari Navigation Bar**: Klik menu "Upload Database" di navigation bar
2. **Dari Dashboard**: Klik tombol "Upload Database Terbaru" di bagian Aksi Cepat
3. **URL Langsung**: Akses `http://localhost:5000/upload-database`

### Langkah 3: Upload File

1. Klik tombol "Choose File" atau "Pilih File"
2. Pilih file Excel (.xlsx) yang sudah disiapkan
3. Sistem akan menampilkan informasi file (nama, ukuran, tipe)
4. Centang kotak konfirmasi untuk melanjutkan
5. Klik tombol "Upload & Import Database"
6. Tunggu hingga proses selesai (jangan tutup halaman)

### Langkah 4: Verifikasi Hasil

Setelah upload berhasil, Anda akan melihat:
- Ringkasan import (jumlah data berhasil/gagal)
- Statistik database terkini
- Lokasi file backup
- Tombol untuk kembali ke dashboard atau melihat data

## Validasi & Keamanan

### Validasi File
- ✅ Format file harus .xlsx
- ✅ Ukuran maksimal 16 MB
- ✅ Harus memiliki 2 sheet yang diperlukan
- ✅ Struktur kolom harus sesuai

### Keamanan
- ✅ Nama file di-sanitasi untuk mencegah path traversal
- ✅ File temporary dihapus setelah import
- ✅ Backup otomatis sebelum perubahan
- ✅ Error handling yang baik

## Troubleshooting

### Error: "Format file tidak valid"
**Solusi**: Pastikan file berekstensi .xlsx (bukan .xls atau format lain)

### Error: "File Excel tidak memiliki sheet yang diperlukan"
**Solusi**: Pastikan file memiliki sheet "db table operasi" dan "db nama dokter" (perhatikan huruf besar/kecil)

### Error: "Ukuran file terlalu besar"
**Solusi**: Kompres file atau kurangi jumlah data. Maksimal 16 MB.

### Data tidak muncul setelah import
**Solusi**: 
1. Periksa format data di Excel
2. Pastikan tidak ada baris kosong di awal
3. Periksa log error di halaman hasil import

## Restore dari Backup

Jika terjadi kesalahan dan Anda perlu restore database:

1. Tutup aplikasi Flask
2. Buka folder `backups/`
3. Cari file backup yang sesuai (berdasarkan timestamp)
4. Copy file backup ke `data/pbo_database.db`
5. Jalankan kembali aplikasi

## Tips & Best Practices

1. **Backup Manual**: Selalu buat backup manual sebelum upload data penting
2. **Verifikasi Data**: Periksa data di Excel sebelum upload
3. **Test dengan Data Kecil**: Coba upload dengan data sample terlebih dahulu
4. **Simpan Backup**: Jangan hapus file backup lama sampai yakin data baru sudah benar
5. **Dokumentasi**: Catat setiap perubahan database untuk tracking

## Struktur Folder

```
app pbo/
├── uploads/          # Temporary upload folder (auto-created)
├── backups/          # Database backups (auto-created)
├── data/
│   └── pbo_database.db
└── templates/
    ├── upload_database.html
    └── upload_success.html
```

## Changelog

### Version 1.0 (2024)
- ✅ Fitur upload file Excel
- ✅ Validasi file otomatis
- ✅ Backup database otomatis
- ✅ Import data operasi dan dokter
- ✅ Laporan hasil import
- ✅ Interface user-friendly

## Support

Jika mengalami masalah atau memiliki pertanyaan:
1. Periksa file log aplikasi
2. Baca dokumentasi ini dengan teliti
3. Hubungi administrator sistem

---

**Catatan**: Fitur ini menggantikan data lama dengan data baru. Pastikan Anda memahami konsekuensinya sebelum melakukan upload.
