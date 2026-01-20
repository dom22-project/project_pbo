# Dynamic Operations Implementation - PBO Aplikasi

## Ringkasan Perubahan

Fitur **Dynamic Operations Table** telah diimplementasikan untuk memungkinkan user menambahkan **unlimited operasi** ke form PBO dengan kemampuan:
- ✅ Tambah/hapus baris operasi secara dinamis tanpa batasan jumlah
- ✅ Hitung otomatis biaya dokter (surgeon) dari semua operasi
- ✅ Support persentase untuk setiap operasi
- ✅ Formula: `surgeon = Σ(biaya_dokter_operasi × persentase_operasi)`
- ✅ Backward compatible dengan format lama (tabel_operasi1-4)

---

## Perubahan Backend (app.py)

### 1. Route `/input` (Input PBO)
**Perubahan:**
- Parsing form operasi dinamis menggunakan array naming convention: `operations[index][kode]` dan `operations[index][persentase]`
- Jika tidak ada format baru, fallback ke format lama untuk backward compatibility
- Operasi disimpan sebagai JSON string di kolom `tabel_operasi1`

**Struktur Form Data:**
```python
# Format Baru (Dynamic)
operations[0][kode] = "0001 - OPERASI MAYOR"
operations[0][persentase] = 100
operations[1][kode] = "0002 - OPERASI MINOR"
operations[1][persentase] = 50

# Disimpan sebagai JSON:
tabel_operasi1 = '[{"kode":"0001 - OPERASI MAYOR", "persentase":1.0}, {"kode":"0002 - OPERASI MINOR", "persentase":0.5}]'
```

### 2. Route `/edit/<pbo_id>` (Edit PBO)
- Menggunakan logic yang sama dengan route `/input`
- Membuat versi baru ketika save (existing behavior preserved)

### 3. API Endpoint `/api/calculate-surgery-fees`
**Update:**
```javascript
// Support format baru: array operasi
{
  "sifat_operasi": "Elektif / Tentative",
  "operations": [
    {"kode": "0001 - OPERASI MAYOR", "persentase": 1.0},
    {"kode": "0002 - OPERASI MINOR", "persentase": 0.5}
  ]
}
```

**Backward Compatible:**
- Masih support format lama: `tabel_operasi1`, `tabel_operasi2`, dst.
- Otomatis fallback jika format baru tidak ditemukan

### 4. API Endpoint `/api/get-operation-details` (BARU)
**Purpose:** Mendapatkan detail operasi berdasarkan kode untuk perhitungan
```
POST /api/get-operation-details
Payload: {"kode": "0001"}
Response: {"success": true, "data": {operation_details}}
```

---

## Perubahan Frontend (input_pbo.html)

### 1. Dynamic Operation Rows
```html
<!-- Dihasilkan oleh JavaScript, struktur per row: -->
<div class="operation-row" data-row-id="1">
  <select name="operations[0][kode]" id="operation_kode_1">...</select>
  <select name="operations[0][persentase]" id="operation_persentase_1">...</select>
  <button class="remove-operation" data-row-id="1">Hapus</button>
</div>
```

### 2. JavaScript Functions

#### `addOperationRow()`
- Tambah baris operasi baru ke tabel
- Update array indices secara otomatis
- Initialize Select2 untuk dropdown
- Disable tombol hapus jika hanya 1 baris

#### `calculateSurgeryFees()`
- **BARU:** Parsing dynamic rows untuk get operasi array
- Extract kode dari format "kode - nama"
- Send ke API `/api/calculate-surgery-fees`
- Update fields: surgeon, anesthesi, ot_room_charge
- Trigger `calculateTotal()`

#### `updateRowNumbers()`
- **ENHANCED:** Update nomor urut row
- **BARU:** Update array indices (operations[n]) otomatis
- Ensure indices konsisten setelah tambah/hapus

#### `updateRemoveButtons()`
- **BARU:** Disable tombol delete jika hanya 1 baris
- Enable jika lebih dari 1 baris

#### `updateAllOperationDropdowns()`
- Update semua dropdown operasi saat kelas berubah
- Maintain current selection jika mungkin

---

## Perubahan Database Model (models_sqlalchemy.py)

### PBOData.to_dict()
**Enhancement:**
```python
def to_dict(self):
    # Parse operations JSON jika ada di tabel_operasi1
    operations = []
    try:
        if self.tabel_operasi1:
            import json
            operations = json.loads(self.tabel_operasi1)
    except (json.JSONDecodeError, TypeError):
        # Fallback ke format lama
        # Convert tabel_operasi1-4 ke array format
    
    return {
        ...
        'operations': operations,  # ← NEW FIELD
        'tabel_operasi1': self.tabel_operasi1,  # ← KEPT for backward compat
        ...
    }
```

**Keuntungan:**
- Data baru dengan format JSON tersimpan di kolom existing
- Tidak butuh migrasi database
- Backward compatible dengan data lama

---

## Alur Kerja Pengguna

### Input PBO Baru dengan Multiple Operasi

1. **Load Form**
   - Sistem otomatis create 1 baris operasi kosong
   - User dapat langsung select operasi atau tambah lebih banyak

2. **Tambah Operasi**
   - Click "Tambah Baris" button
   - Baris baru ditambah dengan field kode, persentase, dan tombol hapus
   - Nomor urut terupdate otomatis
   - Select2 diinit untuk search operasi

3. **Pilih Operasi & Persentase**
   ```
   Baris 1: [OPERASI MAYOR] @ [100%]
   Baris 2: [OPERASI MINOR] @ [50%]
   Baris 3: [KONSULTASI] @ [75%]
   ```

4. **Hitung Surgeon Fee**
   - System otomatis hitung saat ada perubahan
   - `surgeon = (1M × 1.0) + (2M × 0.5) + (0.5M × 0.75) = 2.875M`
   - Trigger by:
     - Perubahan operasi selection
     - Perubahan persentase
     - Perubahan "Sifat Operasi"

5. **Hapus Operasi** (jika ada lebih dari 1)
   - Click tombol hapus di baris yang ingin dihapus
   - Baris terupdate, nomor urut direnumber
   - Calculation dijalankan ulang

6. **Submit Form**
   - Semua operasi & persentase tersimpan sebagai JSON di `tabel_operasi1`
   - Fields `tabel_operasi2-4` dan `persentase_operasi1-4` di-set empty (deprecated)

---

## Fitur Perhitungan Surgery Fee

### Formula

```
Surgeon = Σ (biaya_dokter_operasi_i × persentase_operasi_i)

Contoh:
- Operasi A: biaya_dokter = 1.000.000, persentase = 100% → 1.000.000
- Operasi B: biaya_dokter = 2.000.000, persentase = 50%  → 1.000.000
- Operasi C: biaya_dokter = 500.000, persentase = 75%    → 375.000
────────────────────────────────────────────────────────────────
Total Surgeon Fee                                        → 2.375.000
```

### Trigger Points
- Saat form first load (calculate untuk default operations)
- Saat select operasi berubah
- Saat persentase berubah
- Saat "Sifat Operasi" berubah (CITO/Penyulit bisa affect costing)
- Saat tombol "Hitung Biaya Operasi" diklik manual

---

## Backward Compatibility

### Data Lama (Existing Records)
Data yang tersimpan dengan format lama (tabel_operasi1-4, persentase_operasi1-4) tetap readable:

```python
# Old format in database
tabel_operasi1 = "0001 - OPERASI MAYOR"
persentase_operasi1 = 1.0
tabel_operasi2 = "0002 - OPERASI MINOR"
persentase_operasi2 = 0.5

# to_dict() akan convert ke new format
'operations': [
    {'kode': '0001 - OPERASI MAYOR', 'persentase': 1.0},
    {'kode': '0002 - OPERASI MINOR', 'persentase': 0.5}
]
```

### API Compatibility
- `/api/calculate-surgery-fees` accept both format
- Form parsing support both format
- Edit existing data tetap work

---

## Testing Checklist

- [ ] Tambah 1 operasi - hitung benar
- [ ] Tambah 5+ operasi - hitung benar, form responsive
- [ ] Hapus operasi tengah - reindexing benar
- [ ] Ubah persentase - recalculate otomatis
- [ ] Ubah kelas - filter operasi benar
- [ ] Edit existing data lama - konversi format benar
- [ ] Perubahan sifat operasi - recalculate benar
- [ ] Filter tindakan by kelas - update dropdown semua rows
- [ ] Submit dengan multiple operasi - JSON tersimpan benar

---

## Troubleshooting

### Q: Data tidak tersimpan saat submit
**A:** Check browser console untuk error. Ensure semua form field ter-submit dengan naming convention `operations[n][kode]` dan `operations[n][persentase]`

### Q: Surgeon fee tidak ter-hitung
**A:** 
1. Ensure Select2 initialized untuk operation select
2. Check operation kode valid (ada di database)
3. Check browser console untuk AJAX error
4. Verify persentase format (20, 50, 100 untuk %, atau 0.2, 0.5, 1.0 untuk decimal)

### Q: Baris operasi tidak terupdate saat drag or reorder
**A:** Fitur drag-drop belum diimplementasikan. Manual delete dan tambah baru saja. Bisa ditambahkan di future jika diperlukan.

### Q: Tombol hapus disabled padahal ada 2+ rows
**A:** Bug di updateRemoveButtons(). Reload halaman atau clear browser cache.

---

## Roadmap Improvement

- [ ] Drag-drop reorder rows
- [ ] Copy-paste operasi dari row lain
- [ ] Bulk import operasi dari Excel
- [ ] Export template dengan pre-filled operasi
- [ ] Auto-calculate persentase berdasarkan severity
- [ ] Operasi template/preset untuk common cases

