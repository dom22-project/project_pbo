# PERUBAHAN FORM - HANYA GUNAKAN KELAS

## ✅ Apa yang Diubah

Saya telah **menghapus dropdown "Tipe Kamar"** dari form Input PBO dan menggabungkannya dengan field "Kelas".

Sekarang hanya ada 1 field untuk menentukan harga kamar: **KELAS**

---

## 📊 Mapping Kelas ke Harga Kamar

| Kelas | Harga Kamar | Tipe Kamar |
|-------|---|---|
| ED | Rp 350.000 | Basic |
| OD | Rp 750.000 | Standard |
| ICCU | Rp 950.000 | Deluxe |
| PICU | Rp 1.900.000 | VIP |
| HDU | Rp 2.000.000 | VVIP |
| ICU | Rp 5.000.000 | Suite |
| OR | Rp 7.500.000 | Presidential Suite |

---

## 🎯 Bagaimana Menggunakannya

### Step 1: Buka Form Input PBO
```
Menu → Input PBO
```

### Step 2: Pilih Kelas
Di form, ada field "Kelas" (sudah ada sebelumnya)
```
Kelas ▼
├─ ED
├─ OD
├─ ICCU
├─ PICU
├─ HDU
├─ ICU
└─ OR
```

### Step 3: Harga Kamar Otomatis Terisi
Ketika Anda memilih kelas, field "Tarif Kamar per Hari" akan **otomatis terisi** dengan harga yang sesuai.

Contoh:
- Pilih "ED" → Tarif Kamar = Rp 350.000
- Pilih "OD" → Tarif Kamar = Rp 750.000
- Pilih "ICCU" → Tarif Kamar = Rp 950.000
- dst...

### Step 4: Hitung Total
Klik "Hitung Total" - selesai!

---

## 🔧 Perubahan Teknis

### Files yang Dimodifikasi

1. **templates/input_pbo.html**
   - ❌ Hapus: Dropdown "Tipe Kamar"
   - ✏️ Ubah: Field "Tarif Kamar" menjadi readonly lagi
   - ✏️ Update: JavaScript untuk mapping kelas ke harga

### Removed Features
- ❌ Dropdown "Tipe Kamar" (tidak lagi ada)
- ❌ Event listener untuk room_type_select
- ❌ API fetch untuk room types

### Added Features
- ✅ JavaScript mapping: `kelasToRoomPrice`
- ✅ Auto-fill tarif kamar saat kelas dipilih

---

## 💡 Mapping Detail

```javascript
const kelasToRoomPrice = {
    'ED': 350000,      // Basic
    'OD': 750000,      // Standard
    'ICCU': 950000,    // Deluxe
    'PICU': 1900000,   // VIP
    'HDU': 2000000,    // VVIP
    'ICU': 5000000,    // Suite
    'OR': 7500000      // Presidential Suite
};
```

---

## ✨ Contoh Penggunaan

**Skenario:** Membuat PBO untuk pasien dengan operasi di ruang ICU

1. Buka "Input PBO"
2. Isi data pasien & operasi
3. Pilih "Kelas" = **ICU**
4. Field "Tarif Kamar" otomatis berisi **Rp 5.000.000**
5. Klik "Hitung Total" → selesai!

---

## 🧪 Testing

✅ Mapping sudah diverifikasi:
```
✅ MATCH - Semua harga sesuai!
- ED: Rp 350,000
- OD: Rp 750,000
- ICCU: Rp 950,000
- PICU: Rp 1,900,000
- HDU: Rp 2,000,000
- ICU: Rp 5,000,000
- OR: Rp 7,500,000
```

---

**Status:** ✅ SELESAI  
**Last Update:** 2025-12-30
