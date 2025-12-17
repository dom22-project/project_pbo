# Quick Start Guide - Sistem PBO RS Siloam TB Simatupang

## Cara Cepat Menjalankan Aplikasi

### 1. Buka Terminal/Command Prompt
Navigasi ke folder project:
```bash
cd "c:/Users/agung.daniel/Project PBO/app pbo"
```

### 2. Jalankan Aplikasi
```bash
python .vscode/main.py
```

## Penggunaan Dasar

### Input Data Baru
1. Isi **Nama Pasien** (wajib)
2. Pilih **Kelas** → Tarif kamar otomatis terisi
3. Pilih **Sifat Operasi** (Elektif/CITO/Penyulit)
4. Pilih **Tabel Operasi 1-4** dari dropdown
5. Pilih **Persentase** untuk setiap operasi
6. Biaya Surgeon, Anesthesi, dan OT Room Charge akan **otomatis terhitung**
7. Isi biaya tambahan lainnya jika ada
8. Klik **"Hitung Total"**
9. Klik **"Simpan Data"**

### Cari Data
1. Pindah ke tab **"Cari Data PBO"**
2. Pilih kriteria pencarian
3. Masukkan kata kunci
4. Klik **"Cari"**
5. **Double-click** pada baris untuk edit

### Cetak
- **Cetak Form**: Cetak form yang sedang diisi
- **Cetak Data Terpilih**: Cetak data dari hasil pencarian

## Tips

✅ **Perhitungan Otomatis**: Surgeon, Anesthesi, dan OT Room Charge dihitung otomatis
✅ **Surcharge**: CITO +25%, Penyulit +30%
✅ **Tarif Kamar**: Otomatis berdasarkan kelas
✅ **Validasi**: Nama Pasien wajib diisi sebelum simpan

## Keyboard Shortcuts

- **Tab**: Pindah antar field
- **Enter**: Konfirmasi pilihan dropdown
- **Ctrl+P**: Print (saat dialog print terbuka)

## Troubleshooting Cepat

**Aplikasi tidak muncul?**
→ Pastikan PyQt5 terinstall: `pip install PyQt5`

**Data tidak tersimpan?**
→ Pastikan Nama Pasien terisi

**Error saat buka?**
→ Lihat error di terminal, biasanya missing dependency

---

Untuk dokumentasi lengkap, lihat **README.md**
