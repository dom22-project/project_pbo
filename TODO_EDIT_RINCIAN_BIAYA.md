# TODO: Edit Rincian Biaya Form

## Task Description
Mengubah form input PBO agar field di bagian Rincian Biaya yang editable dan readonly sesuai kebutuhan:
- **READONLY (Locked)**: Surgeon, Tarif Kamar per Hari
- **EDITABLE**: Anesthesi, OT Room Charge, dan field lainnya

## Progress

### Step 1: Modify templates/input_pbo.html ✅ SELESAI
- [x] Hapus atribut `readonly` dari field `anesthesi`
- [x] Hapus atribut `readonly` dari field `ot_room_charge`
- [x] Tambahkan class `cost-input` ke field `anesthesi`
- [x] Tambahkan class `cost-input` ke field `ot_room_charge`
- [x] Tambahkan atribut `min="0"` dan `step="1000"` ke kedua field

### Step 2: Testing ⏳ PENDING
- [ ] Verifikasi field Anesthesi bisa diedit manual
- [ ] Verifikasi field OT Room Charge bisa diedit manual
- [ ] Verifikasi field Surgeon tetap readonly
- [ ] Verifikasi field Tarif Kamar per Hari tetap readonly
- [ ] Verifikasi perhitungan total masih berfungsi dengan benar

**Note:** Testing akan dilakukan oleh user secara manual.

## Perubahan yang Dilakukan

### File: templates/input_pbo.html

**Field Anesthesi (Baris 165-167):**
```html
<!-- SEBELUM -->
<input type="number" class="form-control" name="anesthesi" id="anesthesi" value="0" readonly>

<!-- SESUDAH -->
<input type="number" class="form-control cost-input" name="anesthesi" id="anesthesi" value="0" min="0" step="1000">
```

**Field OT Room Charge (Baris 169-171):**
```html
<!-- SEBELUM -->
<input type="number" class="form-control" name="ot_room_charge" id="ot_room_charge" value="0" readonly>

<!-- SESUDAH -->
<input type="number" class="form-control cost-input" name="ot_room_charge" id="ot_room_charge" value="0" min="0" step="1000">
```

**Field yang TETAP Readonly:**
- Surgeon (Baris 161-163): `readonly` ✅
- Tarif Kamar per Hari (Baris 193-195): `readonly` ✅

## Notes
- Field lain di Rincian Biaya sudah editable dan tidak perlu diubah
- JavaScript sudah mendukung auto-calculate untuk field dengan class `cost-input`
