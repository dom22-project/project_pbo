# 🔍 DEBUGGING - Data Terlewat Saat Upload

## Status Sekarang
Database sudah ada **11,301 operasi**, **95 dokter**, dan **15 tindakan items**.

Tapi user report data masih masuk ke "terlewat" saat upload.

---

## ⚠️ Kemungkinan Penyebab

1. **Format Excel tidak sesuai**
   - Sheet name berbeda (misal: "db table operasi" vs "Operasi")
   - Header di row berbeda
   - Kolom kosong atau tidak lengkap

2. **Data duplikat**
   - Data sudah ada di database sebelumnya
   - Data masuk ke kategori "Duplikat" bukan "Terlewat"

3. **Data tidak valid**
   - Ada kolom yang kosong (terutama "Fee Operator" untuk operasi atau "Nama Dokter" untuk dokter)
   - Data tidak bisa di-parse sebagai angka (untuk Harga Operator, Harga Anestesi)

4. **Header row tidak terdeteksi**
   - Header ada di row 2 atau row berbeda, bukan row 1

---

## 🔧 Cara Debug

### Langkah 1: Download Template yang Benar
1. Masuk ke aplikasi
2. Klik menu "Upload Database"
3. Klik tombol "Download Template"
4. Lihat struktur template-nya

### Langkah 2: Gunakan Debug Script
Jalankan perintah di terminal:

```bash
python debug_excel_upload.py <path_file_excel>
```

Contoh:
```bash
python debug_excel_upload.py C:\Users\agung.daniel\Desktop\database.xlsx
```

Ini akan menampilkan:
- Struktur file Excel
- Jumlah data per sheet
- Analisis kualitas data
- Identifikasi masalah spesifik

### Langkah 3: Share Output

Setelah jalankan script, share output lengkapnya ke sini.

---

## 📋 Checklist untuk User

Sebelum upload, pastikan:

- [ ] File format: **.xlsx** (bukan .xls atau .csv)
- [ ] Sheet names TEPAT:
  - [ ] `db table operasi` (exact case!)
  - [ ] `db nama dokter` (exact case!)
  - [ ] `db nama tindakan` (optional, tapi jika ada harus exact)
  
- [ ] **Sheet: db table operasi**
  - [ ] Header row 1: No, Fee Operator, Kelas, Harga Operator, Harga Anestesi
  - [ ] Data mulai dari row 2
  - [ ] Kolom "Fee Operator" (B) TIDAK BOLEH KOSONG
  - [ ] Kolom "Kelas" (C) TIDAK BOLEH KOSONG
  - [ ] Kolom harga berisi angka (atau kosong, akan jadi 0)
  
- [ ] **Sheet: db nama dokter**
  - [ ] Header row 1: No, Nama Dokter
  - [ ] Data mulai dari row 2
  - [ ] Kolom "Nama Dokter" (B) TIDAK BOLEH KOSONG
  
- [ ] **Sheet: db nama tindakan** (jika ada)
  - [ ] Header row 1: No, Nama Tindakan, Kelas, Kategory, Sales Item Type, Amount
  - [ ] Data mulai dari row 2
  - [ ] Kolom "Nama Tindakan" (B) TIDAK BOLEH KOSONG
  - [ ] Kolom "Kelas" (C) TIDAK BOLEH KOSONG

---

## 📞 Info yang Saya Butuhkan dari User

1. **Output dari debug_excel_upload.py** untuk file yang di-upload
2. **Screenshot success page** yang menunjukkan import vs skipped
3. **File Excel** yang di-upload (atau sample dari structure-nya)

Dengan info ini, saya bisa identify masalah dengan pasti!

---

## 🎯 Contoh Output yang Berhasil

Jika upload berhasil, di success page akan terlihat:

```
OPERASI:
- Berhasil Diimport: 45
- Dilewati: 5

DOKTER:
- Berhasil Diimport: 20
- Duplikat: 0
- Dilewati: 5

TINDAKAN:
- Berhasil Diimport: 85
- Dilewati: 10

Statistik Database Saat Ini:
- Total Operasi: 11346 (sebelumnya 11301)
- Total Dokter: 115 (sebelumnya 95)
- Total Tindakan Items: 100 (sebelumnya 15)
```

---

## 🚫 Contoh Output yang BERMASALAH

Jika semua data terlewat:

```
OPERASI:
- Berhasil Diimport: 0
- Dilewati: 50  ⚠️ SEMUA TERLEWAT!

DOKTER:
- Berhasil Diimport: 0
- Duplikat: 0
- Dilewati: 20  ⚠️ SEMUA TERLEWAT!

Statistik Database Saat Ini:
- Total Operasi: 11301 (tidak berubah)
- Total Dokter: 95 (tidak berubah)
```

Ini berarti ada masalah dengan format file Excel!

---

## 📝 Action Items untuk Kita

- [ ] User jalankan `python debug_excel_upload.py <file>`
- [ ] Share output lengkapnya
- [ ] Saya analisis root cause
- [ ] Buat fix atau perbaikan data format
- [ ] Test upload ulang
