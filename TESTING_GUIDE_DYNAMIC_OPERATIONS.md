# Testing Guide - Dynamic Operations PBO

## Persiapan

1. **Ensure database sudah punya operations**
   - Jika kosong, upload Excel database via `/upload-database`
   - Atau check ke menu admin untuk verify data ada

2. **Refresh browser** (clear cache)
   ```
   Ctrl+Shift+Delete (Chrome) atau Ctrl+Shift+R
   ```

3. **Open browser console** untuk melihat logs
   ```
   F12 → Console tab
   ```

---

## Test Case 1: Input PBO dengan Multiple Operasi ✅

### Langkah:
1. Buka http://localhost:5000/input
2. Isi data pasien:
   - Nama Pasien: "Test Patient"
   - Diagnosa: "Appendicitis"
   - Nama Operasi: "Appendectomy"
   - Nama Dokter: Pilih salah satu
   - Kelas: Pilih "VIP"

3. **Test Tabel Operasi:**
   - System auto-create 1 baris kosong
   - Click dropdown "Tindakan Operasi 1"
   - Cari dan pilih operasi pertama (e.g., "DOCTORS PROCEDURE TABLE 1")
   - Verify:
     - Biaya dokter: Rp 1.125.000
     - Persentase default: 100%

4. **Tambah Operasi:**
   - Click tombol "Tambah Baris"
   - Baris baru ditambah dengan nomor 2
   - Pilih operasi berbeda (e.g., "DOCTORS PROCEDURE TABLE 2")
   - Ubah persentase ke 50%

5. **Tambah Operasi Lagi:**
   - Click "Tambah Baris" lagi
   - Baris 3 ditambah
   - Pilih operasi: "DOCTORS PROCEDURE TABLE 3"
   - Persentase: 75%

6. **Verify Display:**
   - Baris 1: DOCTORS PROCEDURE TABLE 1 @ 100%
   - Baris 2: DOCTORS PROCEDURE TABLE 2 @ 50%
   - Baris 3: DOCTORS PROCEDURE TABLE 3 @ 75%
   - Delete buttons semua aktif (hanya disable jika 1 baris)

7. **Calculate Surgery Fee:**
   - Click "Hitung Biaya Operasi"
   - Verify surgeon field ter-update dengan hasil:
     ```
     Surgeon = (1.125.000 × 1.0) + (2.368.000 × 0.5) + (4.934.000 × 0.75)
             = 1.125.000 + 1.184.000 + 3.700.500
             = 6.009.500
     ```

8. **Hitung Total:**
   - Click "Hitung Total"
   - Verify total field ter-update dengan semua costs

9. **Submit:**
   - Click "Simpan Data"
   - Verify redirect ke detail page dengan ID baru
   - Check data tersimpan benar

---

## Test Case 2: Edit Existing dengan Multiple Operasi ✅

### Langkah:
1. Buka http://localhost:5000/search
2. Cari dan buka salah satu PBO yang sudah ada (dari Test Case 1)
3. Click "Edit"

### Expected:
- Form ter-populate dengan data lama
- Operasi dari PBO sebelumnya ter-load ke tabel dynamis
- Nomor baris dan persentase sesuai

### Test Edit:
4. Ubah operasi di baris 2 ke operasi berbeda
5. Ubah persentase baris 3 menjadi 100%
6. **Tambah baris baru:**
   - Click "Tambah Baris"
   - Baris 4 ditambah
   - Pilih operasi
   - Persentase 25%

7. **Delete operasi:**
   - Click tombol delete di baris 2
   - Baris 2 dihapus
   - Baris 3 & 4 renumber menjadi 2 & 3
   - Row numbers terupdate otomatis

8. Click "Hitung Biaya Operasi"
9. Click "Simpan Data"
10. Verify:
    - Versi baru terbuat (version_number +1)
    - Data lama tetap tersimpan di history

---

## Test Case 3: Delete Operasi dalam Form ✅

### Langkah:
1. Dari halaman input, buat 3 operasi
2. Click delete di baris 2
   - Baris 2 hilang
   - Baris 3 menjadi baris 2
   - Delete button tetap aktif (masih ada 2 baris)
3. Click delete di baris 2 lagi
   - Baris lalu 1 baris tersisa
   - **Delete button disabled** ✅
4. Coba click delete button
   - Tidak bisa di-click
   - Button punya cursor: not-allowed

---

## Test Case 4: Ubah Kelas & Filter Operasi ✅

### Langkah:
1. Buka input form
2. Ubah kelas dari default ke "STANDARD"
3. Verify:
   - Tarif Kamar terupdate: Rp 750.000
   - Total terupdate
4. Klik dropdown operasi
   - Verify hanya operasi STANDARD yang muncul
5. Ubah operasi selection
   - Auto-calculate surgeon fee
   - Verify hasil benar

---

## Test Case 5: Backward Compatibility ✅

### Setup (jika ada):
- Ada PBO lama dengan format `tabel_operasi1-4` & `persentase_operasi1-4`

### Test:
1. Buka detail PBO lama tersebut
2. Verify operasi display:
   - Baris 1: tabel_operasi1 value
   - Baris 2: tabel_operasi2 value (jika ada)
   - dst.

3. Click Edit
4. Verify operasi ter-load ke form
5. Edit salah satu
6. Click "Hitung Biaya Operasi"
7. Verify calculation benar
8. Submit → simpan
9. Verify format JSON di database

---

## Test Case 6: Validation ✅

### Test Required Field:
1. Buka input form
2. Try submit tanpa pilih operasi di baris 1
   - Browser validation: "Silakan isi field ini"
   - Tidak submit

3. Pilih operasi baris 1
4. Try submit
   - Form submit OK
   - Redirect detail page

---

## Expected Result Summary

| Test | Expected | Status |
|------|----------|--------|
| Tambah operasi | Baris baru ditambah, nomor terupdate | ✅ |
| Hapus operasi | Baris dihapus, renumber, button management | ✅ |
| Calculation | Surgeon fee benar | ✅ |
| Filter kelas | Operasi sesuai kelas | ✅ |
| Submit | Data JSON tersimpan | ✅ |
| Edit | Data ter-load ulang | ✅ |
| Delete jika 1 | Button disabled | ✅ |
| Backward compat | Operasi lama bisa dibaca & diedit | ✅ |

---

## Browser Console Expected Logs

```javascript
// When page loads:
"Initial kelas on page load: VIP"
"Fetching operasi untuk kelas: VIP"

// When add row:
"Row updated successfully"

// When calculate:
"Collecting operations from form..."
"Operations array: Array(3) [...]"
"POST /api/calculate-surgery-fees"

// When delete row:
"Row deleted successfully"
"Row updated successfully"

// Success response:
{"success": true, "data": {"surgeon": 6009500, ...}}
```

---

## Troubleshooting

### Problem: Baris operasi tidak muncul saat edit
**Solution:**
1. Check browser console untuk error
2. Verify `existingOperations` JavaScript variable
3. Check PBOData.operations field dari backend
4. Restart Flask: Ctrl+C, then `python app.py`

### Problem: Calculate button tidak work
**Solution:**
1. Check browser console
2. Verify operation dropdown ter-select (ada value)
3. Check `/api/calculate-surgery-fees` response di Network tab
4. Ensure database ada operations (upload template jika kosong)

### Problem: Total tidak update setelah ubah cost
**Solution:**
1. Click "Hitung Total" button manual
2. Atau ubah nilai di cost input lagi

### Problem: Form submit error
**Solution:**
1. Check console error message
2. Verify all required fields filled
3. Check network tab untuk response dari server

---

## Data Verification (Database Level)

```sql
-- Check saved operasi JSON
SELECT id, tabel_operasi1, tabel_operasi2, tabel_operasi3 
FROM database 
WHERE id = {pbo_id};

-- Expected tabel_operasi1:
-- '[{"kode":"0001 - OPERASI A", "persentase":1.0}, {"kode":"0002 - OPERASI B", "persentase":0.5}]'

-- Expected tabel_operasi2-4:
-- '' (empty string)

-- Check version history
SELECT id, version_number, parent_id, is_latest 
FROM database 
WHERE parent_id = {pbo_id} 
ORDER BY version_number DESC;
```

---

## Performance Notes

- Form dengan 20+ operasi tetap responsive
- Calculate surgery fee < 100ms
- Submit form < 500ms
- Tidak ada UI freeze atau lag

