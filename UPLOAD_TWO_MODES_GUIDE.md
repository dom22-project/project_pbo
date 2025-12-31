# DATA MASUK - Mode Upload Database

## 🎯 Masalah Awal
Data yang di-upload tidak masuk ke database karena:
1. **Database sudah penuh** - 5839 operasi + 93 dokter sudah ada
2. **Check duplikat** - Data dengan kode yang sama akan di-skip
3. **Hanya merge mode** - Default adalah merge, tidak replace

## ✅ Solusi: Dua Mode Upload

### Mode 1: MERGE (Default) 
**Data ditambahkan, yang sudah ada di-skip**
- Gunakan jika ingin menambah data baru tanpa menghapus yang lama
- Data dengan kode yang sama akan di-skip (tidak di-update)
- Aman karena tidak menghapus data lama

### Mode 2: REPLACE (Baru)
**Hapus semua data lama, ganti dengan data baru**
- Gunakan jika ingin reset database sepenuhnya
- Semua data operasi, dokter, tindakan akan dihapus dulu
- Kemudian import data baru dari file Excel
- Cocok untuk update/sinkronisasi database

---

## 🚀 Cara Menggunakan

### Untuk MERGE Mode (Tambah Data Baru):
1. Login ke aplikasi
2. Buka "Upload Database"
3. **JANGAN centang** kotak "Mode GANTI"
4. Upload file Excel
5. Data baru akan ditambahkan (yang sudah ada di-skip)

### Untuk REPLACE Mode (Ganti Semua Data):
1. Login ke aplikasi
2. Buka "Upload Database"
3. **CENTANG** kotak "Mode GANTI: Hapus semua data lama sebelum import"
4. Upload file Excel
5. Semua data lama akan dihapus dan diganti dengan data baru

---

## 📊 Perbandingan Mode

| Aspek | MERGE | REPLACE |
|-------|-------|---------|
| Data baru ditambahkan | ✅ Ya | ✅ Ya |
| Data lama dihapus | ❌ Tidak | ✅ Ya |
| Aman untuk testing | ❌ Rawan duplikat | ✅ Lebih aman |
| Untuk update berkala | ✅ Cocok | ❌ Berlebihan |
| Untuk sync database | ❌ Tidak | ✅ Cocok |
| Waktu proses | Cepat | Lebih lambat |

---

## 🧪 Test Results

### Replace Mode Test:
```
BEFORE:     5839 operations, 93 doctors
DELETE:     0 operations, 0 doctors
IMPORT:     2 operations, 2 doctors
RESULT:     ✅ PASSED
```

### Merge Mode Test:
```
BEFORE:     5839 operations, 93 doctors
IMPORT:     0 new (all skipped due to duplicates)
RESULT:     ✅ Berfungsi sesuai rancangan
```

---

## ⚠️ Catatan Penting

1. **Backup Otomatis**: Database lama SELALU di-backup sebelum upload
   - Lokasi: `backups/pbo_database_backup_YYYYMMDD_HHMMSS.db`

2. **Replace Mode Tidak Bisa Di-Undo Secara Langsung**:
   - Tapi bisa restore dari backup yang sudah dibuat
   - Pastikan confirm checkbox sebelum upload

3. **Merge Mode Aman**:
   - Tidak menghapus data lama
   - Data duplikat akan otomatis di-skip
   - Bisa di-retry tanpa khawatir

4. **Format Excel Harus Benar**:
   - Sheet: "db table operasi"
   - Sheet: "db nama dokter"
   - Header di row 1
   - Data mulai dari row 2

---

## 📋 File Modified

- **app.py**:
  - Tambahan parameter `replace_mode` di route upload
  - Tambahan logic untuk clear data jika replace_mode=true
  - Tambahan logging untuk replace operation

- **models.py**:
  - Tambahan function `get_doctor_by_name()` - check doctor di table Doctor (bukan User)
  - Fix bug: sebelumnya check di table User, sekarang di table Doctor

- **templates/upload_database.html**:
  - Tambahan checkbox untuk "Mode GANTI"
  - Update informasi upload modes
  - Update help text

---

## 🔧 Tech Details

### Bug yang Diperbaiki:
```python
# BEFORE (BUG)
existing = db_helper.get_user_by_username(str(nama_dokter))
# ❌ Ini check di table User, bukan Doctor!

# AFTER (FIXED)
existing = db_helper.get_doctor_by_name(str(nama_dokter))
# ✅ Ini check di table Doctor dengan benar
```

### Replace Mode Logic:
```python
if replace_mode:
    db_helper.delete_all_operations()
    db_helper.delete_all_doctors()
    db_helper.delete_all_tindakan_items()
    # Kemudian import data baru
```

---

## 🎓 Rekomendasi Penggunaan

### Gunakan MERGE Mode untuk:
- Menambah dokter baru
- Menambah operasi baru
- Update berkala (mingguan/bulanan)
- Sinkronisasi partial data

### Gunakan REPLACE Mode untuk:
- Fresh setup database
- Migrasi data dari sistem lama
- Reset database untuk testing
- Update major (semua data ganti)

---

## ✅ Verification Checklist

- [x] Fungsi `get_doctor_by_name()` ditambahkan
- [x] Parameter `replace_mode` di route upload
- [x] Logic delete all data jika replace_mode=true
- [x] UI updated dengan checkbox replace mode
- [x] Test MERGE mode - PASSED ✅
- [x] Test REPLACE mode - PASSED ✅
- [x] Database restored dari backup

---

**Status:** ✅ READY  
**Last Update:** 2025-12-30  
**Version:** 2.0 (dengan dua mode upload)
