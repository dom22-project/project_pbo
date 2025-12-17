# TODO: Integrasi Data Tindakan ke Form Input PBO

## 📋 Requirement dari User

User ingin data dari sheet "db nama tindakan" diintegrasikan ke form input PBO dengan mapping:

| Sheet Column | Target di Form PBO | Deskripsi |
|--------------|-------------------|-----------|
| Kolom B (nama_tindakan) | Dropdown "Nama Operasi" | Menambahkan pilihan operasi dari tindakan items |
| Kolom C (kelas) | Filter Kelas Perawatan | Data difilter berdasarkan kelas yang dipilih user |
| Kolom D (kategory) | Form Rincian Biaya | Auto-fill ke field yang sesuai dengan kategory |
| Kolom F (amount) | Jumlah (Rp) | Auto-fill harga sesuai kelas kamar |

## 🎯 Analisis Kebutuhan

### Mapping Kategory ke Field Form:

Berdasarkan data yang ada, kategory di sheet "db nama tindakan" perlu dimapping ke field di form PBO:

**Kategory yang ada:**
- "Konsultasi Pre Tindakan" → Field: `konsultasi_pre_tindakan`
- "Diagnostic Pre Tindakan" → Field: `diagnostic_pre_tindakan`
- "Obat dan Alkes" → Field: `obat_dan_alkes`
- "Alat" → Field: `alat`
- "Diagnostic" → Field: `diagnostic`
- "Medical Equipment" → Field: `medical_equipment`
- (kosong/lainnya) → Perlu ditentukan

### Kompleksitas:

1. **Dropdown Nama Operasi**
   - Saat ini: Menggunakan data dari `operation_tables`
   - Perlu: Menggabungkan dengan data dari `tindakan_items`
   - Challenge: Struktur data berbeda

2. **Filter Berdasarkan Kelas**
   - Perlu: AJAX untuk filter real-time
   - Ketika user pilih kelas → Filter tindakan yang sesuai

3. **Auto-fill Rincian Biaya**
   - Perlu: JavaScript untuk mapping kategory ke field
   - Ketika user pilih tindakan → Auto-fill field yang sesuai

4. **Auto-fill Amount**
   - Perlu: Ambil amount dari tindakan yang dipilih
   - Sesuaikan dengan kelas kamar

## 🔧 Rencana Implementasi

### Phase 1: Backend API (app.py)

**File: app.py**

1. **API Endpoint Baru:**
   ```python
   @app.route('/api/get-tindakan-by-kelas', methods=['POST'])
   def api_get_tindakan_by_kelas():
       """Get tindakan items filtered by kelas"""
       # Return tindakan items yang sesuai dengan kelas
   ```

2. **API Endpoint untuk Detail Tindakan:**
   ```python
   @app.route('/api/get-tindakan-detail', methods=['POST'])
   def api_get_tindakan_detail():
       """Get detail tindakan including kategory and amount"""
       # Return detail lengkap tindakan
   ```

### Phase 2: Database Query (models.py)

**File: models.py**

1. **Fungsi Filter by Kelas:**
   ```python
   def get_tindakan_by_kelas(self, kelas):
       """Get tindakan items filtered by kelas"""
   ```

2. **Fungsi Get by Nama:**
   ```python
   def get_tindakan_by_nama(self, nama_tindakan, kelas):
       """Get specific tindakan item"""
   ```

### Phase 3: Frontend Integration (input_pbo.html)

**File: templates/input_pbo.html**

1. **Update Dropdown Nama Operasi:**
   - Tambah section untuk tindakan items
   - Group by source (operation_tables vs tindakan_items)

2. **JavaScript untuk Auto-fill:**
   ```javascript
   // Ketika kelas dipilih → Filter tindakan
   $('#kelas').change(function() {
       loadTindakanByKelas($(this).val());
   });
   
   // Ketika tindakan dipilih → Auto-fill fields
   $('#nama_operasi').change(function() {
       autoFillFromTindakan($(this).val());
   });
   ```

3. **Mapping Kategory ke Field:**
   ```javascript
   const kategoryMapping = {
       'Konsultasi Pre Tindakan': 'konsultasi_pre_tindakan',
       'Diagnostic Pre Tindakan': 'diagnostic_pre_tindakan',
       'Obat dan Alkes': 'obat_dan_alkes',
       // ... dst
   };
   ```

### Phase 4: JavaScript Logic (main.js)

**File: static/js/main.js**

1. **Function loadTindakanByKelas()**
2. **Function autoFillFromTindakan()**
3. **Function mapKategoryToField()**

## ⚠️ Pertimbangan & Tantangan

### 1. **Struktur Data Berbeda**
- `operation_tables`: Memiliki biaya_dokter dan biaya_rs terpisah
- `tindakan_items`: Hanya memiliki amount total

**Solusi:** Perlu mapping atau konversi

### 2. **Multiple Tindakan dengan Nama Sama**
- Satu nama tindakan bisa punya multiple entries dengan kategory berbeda
- Contoh: "ABLASI 3D" ada untuk Konsultasi, Diagnostic, Obat, dll

**Solusi:** 
- Option A: Tampilkan semua sebagai pilihan terpisah
- Option B: Ketika pilih nama, auto-fill semua kategory sekaligus

### 3. **Kelas Tidak Match**
- Kelas di tindakan_items mungkin tidak sama persis dengan kelas kamar
- Contoh: "BASIC" vs "Kelas 1"

**Solusi:** Perlu mapping kelas atau standardisasi

### 4. **UX Complexity**
- Form sudah kompleks, menambah auto-fill bisa membingungkan user
- Perlu UI/UX yang jelas

**Solusi:** 
- Tambah indicator/badge untuk tindakan dari database baru
- Tambah tooltip/help text

## 📊 Estimasi Effort

| Task | Complexity | Estimated Time |
|------|-----------|----------------|
| Backend API | Medium | 2-3 hours |
| Database Queries | Low | 1 hour |
| Frontend Integration | High | 4-5 hours |
| JavaScript Logic | High | 3-4 hours |
| Testing | Medium | 2-3 hours |
| **TOTAL** | **High** | **12-16 hours** |

## 🤔 Pertanyaan untuk User

Sebelum implementasi, perlu klarifikasi:

1. **Untuk nama tindakan yang sama tapi beda kategory:**
   - Apakah ingin semua kategory auto-fill sekaligus?
   - Atau user pilih satu per satu?

2. **Mapping kelas:**
   - Apakah kelas di tindakan_items sudah sesuai dengan kelas kamar?
   - Perlu mapping manual?

3. **Prioritas:**
   - Apakah ini urgent atau bisa dikerjakan bertahap?
   - Mana yang paling penting: dropdown, filter, atau auto-fill?

4. **Existing data:**
   - Apakah data di `operation_tables` masih digunakan?
   - Atau diganti sepenuhnya dengan `tindakan_items`?

## 🎯 Rekomendasi

Mengingat kompleksitas tinggi, saya rekomendasikan:

**Option 1: Implementasi Bertahap**
1. Phase 1: Tambah tindakan ke dropdown (tanpa auto-fill)
2. Phase 2: Tambah filter by kelas
3. Phase 3: Tambah auto-fill rincian biaya

**Option 2: Implementasi Sederhana**
- Buat halaman terpisah khusus untuk input PBO dari tindakan items
- Lebih mudah maintain dan tidak mengganggu form existing

**Option 3: Hybrid**
- Tambah toggle/switch di form: "Gunakan Data Tindakan"
- Jika aktif → Load dari tindakan_items
- Jika tidak → Tetap gunakan operation_tables

## 📝 Next Steps

1. **Konfirmasi requirement** dengan user
2. **Pilih approach** (Option 1, 2, atau 3)
3. **Buat prototype** untuk validasi UX
4. **Implementasi** sesuai pilihan
5. **Testing** menyeluruh
6. **Dokumentasi** penggunaan

---

**Status:** ⏸️ PENDING - Menunggu klarifikasi dari user
**Priority:** 🔴 HIGH (jika urgent) / 🟡 MEDIUM (jika bisa bertahap)
**Complexity:** 🔴 HIGH
