# TODO: Tambah Input Tabel Tindakan Tambahan

## Task Description
Menambahkan input tabel untuk tindakan tambahan di halaman input PBO yang berisi:
- Nama Tindakan (dropdown dari db nama tindakan)
- Kategory (otomatis dari data tindakan yang dipilih)
- Kelas (mengikuti kelas pasien yang dipilih)
- Harga (otomatis ke rincian biaya sesuai kategory)

## Data Source
- Excel: `data/db pbo.xlsx` - Sheet "db nama tindakan"
- Database: Table `tindakan_items` dengan kolom:
  - id
  - nama_tindakan
  - kelas
  - kategory
  - sales_item_type
  - amount

## Plan

### Step 1: Analisis Struktur Data
- [x] Pahami struktur tabel `tindakan_items`
- [x] Pahami bagaimana data tindakan digunakan di aplikasi
- [ ] Tentukan mapping kategory ke field rincian biaya

### Step 2: Update Database Schema
- [ ] Tambah kolom di tabel `database` untuk menyimpan tindakan tambahan yang dipilih
- [ ] Buat struktur JSON untuk menyimpan multiple tindakan tambahan

### Step 3: Update Backend (app.py)
- [ ] Tambah API endpoint untuk filter tindakan berdasarkan kelas
- [ ] Update route `/input` untuk handle data tindakan tambahan
- [ ] Update route `/edit` untuk handle data tindakan tambahan
- [ ] Update logic perhitungan biaya untuk include tindakan tambahan

### Step 4: Update Frontend (templates/input_pbo.html)
- [ ] Tambah section "Tindakan Tambahan" setelah "Tabel Operasi"
- [ ] Buat tabel dinamis untuk input multiple tindakan
- [ ] Tambah tombol "Tambah Tindakan" dan "Hapus Tindakan"
- [ ] Implementasi dropdown nama tindakan dengan Select2
- [ ] Auto-populate kategory saat tindakan dipilih
- [ ] Filter tindakan berdasarkan kelas pasien
- [ ] Auto-calculate harga ke rincian biaya sesuai kategory

### Step 5: Update JavaScript
- [ ] Implementasi fungsi untuk add/remove row tindakan
- [ ] Implementasi fungsi untuk filter tindakan by kelas
- [ ] Implementasi fungsi untuk auto-populate kategory
- [ ] Implementasi fungsi untuk map harga ke rincian biaya
- [ ] Update fungsi calculateTotal untuk include tindakan tambahan

### Step 6: Update Templates Lain
- [ ] Update `edit_pbo.html` untuk support tindakan tambahan
- [ ] Update `detail_pbo.html` untuk display tindakan tambahan
- [ ] Update `print_pbo.html` untuk print tindakan tambahan

## Mapping Kategory ke Rincian Biaya

Berdasarkan kategory di data tindakan, mapping ke field rincian biaya:
- **Konsultasi** → konsultasi_pre_tindakan
- **Diagnostic** → diagnostic atau diagnostic_pre_tindakan
- **Medical Equipment** → medical_equipment
- **Obat dan Alkes** → obat_dan_alkes
- **Alat** → alat
- **Recovery** → recovery_room_charge
- **Lainnya** → (perlu ditentukan)

## Notes
- Tindakan akan difilter berdasarkan kelas pasien yang dipilih
- Harga akan otomatis ditambahkan ke field rincian biaya sesuai kategory
- User masih bisa edit manual field rincian biaya setelah auto-calculate
- Data tindakan tambahan akan disimpan sebagai JSON di database
