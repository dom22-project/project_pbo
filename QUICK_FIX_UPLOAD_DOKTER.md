# PANDUAN UPLOAD NAMA DOKTER - QUICK FIX

## ❌ Masalah Asli
Nama dokter tidak terupload ke database saat menggunakan fitur Upload Database.

## ✅ Solusi

### Root Cause
Nama sheet dalam file Excel user mungkin berbeda case dengan expected name. Contoh:
- File user punya: `DB NAMA DOKTER` atau `Db Nama Dokter`
- System expect: `db nama dokter`

### Yang Sudah Diperbaiki

#### 1. **Case-Insensitive Sheet Matching**
Sekarang system bisa recognize sheet names dalam case apapun:
- ✅ `db nama dokter` ← original
- ✅ `DB NAMA DOKTER` ← uppercase
- ✅ `Db Nama Dokter` ← mixed case
- ✅ `DB nama DOKTER` ← random case

#### 2. **Better Error Messages**
Kalau ada error, user sekarang lihat:
- Sheet mana yang missing
- Sheet apa saja yang ada dalam file Excel mereka

Contoh pesan error:
```
File Excel tidak memiliki sheet yang diperlukan:
- db table operasi

Sheet yang ditemukan dalam file Anda:
- DB NAMA DOKTER
- Data Dokter
```

#### 3. **Import Logging**
System sekarang log setiap dokter yang diimport:
```
[IMPORT] Doctor imported: Dr. Budi Santoso
[IMPORT] Doctor imported: Dr. Siti Nurhaliza
[IMPORT] Total doctors imported: 2
```

#### 4. **Warnings Display**
Setelah import, user lihat apa yang happening dengan data mereka.

---

## 📋 Cara Benar Upload Dokter

### Format File Excel

**Sheet 1: "db table operasi"**
| No | Fee Operator | Kelas | Harga Operator | Harga Anestesi |
|---|---|---|---|---|
| 1 | Operasi Umum | GENERAL | 1000000 | 500000 |
| 2 | Operasi Spesialis | SPESIALIS | 2000000 | 1000000 |

**Sheet 2: "db nama dokter"**
| No | Nama Dokter |
|---|---|
| 1 | Dr. Budi Santoso |
| 2 | Dr. Siti Nurhaliza |
| 3 | Dr. Andi Prasetyo |

### Langkah-Langkah

1. **Siapkan file Excel** dengan 2 sheet (case tidak penting):
   - Sheet operasi
   - Sheet dokter

2. **Buka aplikasi** → Kelola Data → Upload Database

3. **Pilih file** dan klik Upload

4. **Lihat hasil** → Statistics untuk setiap jenis data

---

## 🔍 Troubleshooting

### "Sheet tidak ditemukan"
**Solusi:** Cek nama sheet dalam file Excel Anda harus ada:
- Sheet untuk operasi
- Sheet untuk dokter

### "Dokter tidak terimport"
**Solusi:** Pastikan:
- ✅ Sheet nama sudah benar
- ✅ Kolom B berisi nama dokter (atau A jika B kosong)
- ✅ Nama dokter tidak kosong

### "Duplikat dokter"
**Solusi:** Nama dokter sudah ada di database. Gunakan mode "GANTI" jika ingin replace semua.

---

## 💡 Tips

1. **Download template** dari aplikasi untuk format yang benar
2. **Gunakan Merge Mode** (default) untuk tambah data baru
3. **Gunakan Replace Mode** untuk ganti semua data lama

---

**Status:** ✅ Sudah Diperbaiki  
**Version:** 2.0  
**Last Updated:** 2025-12-31
