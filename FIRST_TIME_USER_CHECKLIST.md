# ✅ MONTHLY REPORT - FIRST TIME USER CHECKLIST

## 📋 BEFORE YOU START

Pastikan hal-hal berikut sudah siap:

### Prerequisites
- [x] Aplikasi PBO sudah running (http://localhost:5000)
- [x] Anda sudah login dengan akun valid
- [x] Browser yang support (Chrome, Firefox, Safari, Edge)
- [x] Data operasi sudah ada di sistem (minimal untuk 1 bulan)

---

## 🎯 FIRST TIME SETUP

### Step 1: Akses Fitur Laporan Bulanan
- [ ] Klik **"Laporan Bulanan"** di menu navbar
  
  *Atau alternatif:*
  - [ ] Dari Dashboard → Klik tombol **"Laporan Bulanan"** di Quick Actions
  - [ ] Akses langsung URL: http://localhost:5000/monthly-report

### Step 2: Halaman Laporan Membuka
- [ ] Halaman berhasil load tanpa error
- [ ] Lihat header berwarna ungu dengan judul "Laporan Bulanan"
- [ ] Lihat dropdown "Pilih Bulan & Tahun" (Month Selector)
- [ ] Lihat 4 statistik cards (Total Operasi, Pendapatan, Dokter, Asuransi)

### Step 3: Pilih Bulan (Optional - akan default ke bulan sekarang)
- [ ] Klik dropdown "Pilih Bulan & Tahun"
- [ ] Lihat list bulan yang ada data
- [ ] Pilih bulan yang ingin dilihat
- [ ] Klik tombol **"Tampilkan Data"**
  
  *Atau biarkan default ke bulan sekarang*

### Step 4: Lihat Tabel Data
- [ ] Tabel muncul di bawah statistik
- [ ] Tabel menampilkan kolom: Tanggal, Operasi, Dokter, Asuransi, Kelas, Total
- [ ] Setiap baris adalah 1 operasi
- [ ] Total operasi = jumlah baris di tabel
- [ ] Total pendapatan = sum dari kolom "Total Biaya"

---

## 🔍 UNDERSTAND THE DATA

### Memahami Statistik Cards
```
┌──────────────────────┐
│ Total Operasi: 15    │ = Ada 15 operasi dalam bulan ini
└──────────────────────┘

┌──────────────────────┐
│ Total Pendapatan     │ = Jumlah semua biaya operasi
│ Rp. 2.500.000        │ = Rp 2 juta 500 ribu
└──────────────────────┘

┌──────────────────────┐
│ Dokter Unik: 8       │ = Ada 8 dokter berbeda yang
│                      │   melakukan operasi bulan ini
└──────────────────────┘

┌──────────────────────┐
│ Asuransi Unik: 5     │ = Ada 5 asuransi/perusahaan
│                      │   berbeda yang menanggung biaya
└──────────────────────┘
```

### Memahami Tabel Detail

Setiap kolom menampilkan:
- **No.** = Nomor urut (1, 2, 3, ...)
- **Tanggal** = Tanggal operasi dilakukan (format: DD/MM/YYYY)
- **Nama Operasi** = Jenis prosedur medis (misal: Operasi Hernia, etc)
- **Nama Dokter** = Dokter yang melakukan operasi (dalam badge biru)
- **Perusahaan/Asuransi** = Pihak penanggung (dalam badge kuning)
- **Kelas** = Klasifikasi operasi (VIP, 1, 2, 3, dll)
- **Total Biaya** = Total biaya operasi (format Rp.)
- **Aksi** = Tombol untuk lihat detail (ikon mata)

---

## 🎬 FIRST ACTIONS

### Action 1: Lihat Detail Operasi
- [ ] Di tabel, cari baris yang ingin dilihat
- [ ] Klik **ikon mata** di kolom "Aksi"
- [ ] Akan membuka halaman detail operasi lengkap
- [ ] Klik **"Kembali"** untuk balik ke laporan

### Action 2: Export Data ke CSV (Untuk Excel)
- [ ] Scroll ke bawah halaman
- [ ] Lihat section "Opsi Ekspor"
- [ ] Klik tombol **"Export CSV"**
- [ ] File `laporan_[BULAN]_[TAHUN].csv` akan otomatis diunduh
- [ ] Buka file di Excel untuk analisis lebih lanjut

### Action 3: Export ke PDF (Untuk Print)
- [ ] Klik tombol **"Cetak"** di header (atau Ctrl+P)
- [ ] Dialog print akan muncul
- [ ] Pilih printer: **"Save as PDF"**
- [ ] Klik **"Save"**
- [ ] PDF akan tersimpan di folder Downloads

### Action 4: Ganti Bulan
- [ ] Klik dropdown "Pilih Bulan & Tahun" lagi
- [ ] Pilih bulan berbeda
- [ ] Klik "Tampilkan Data"
- [ ] Tabel akan berubah menampilkan data bulan baru

---

## 🚫 TROUBLESHOOTING

### Problem: "Tidak Ada Data" muncul
**Penyebab**: Tidak ada operasi di bulan yang dipilih

**Solusi**:
- [ ] Pilih bulan lain dari dropdown
- [ ] Input beberapa operasi terlebih dahulu
- [ ] Pastikan operasi punya tanggal yang valid

### Problem: Statistik terlihat 0 (nol)
**Penyebab**: Data mungkin tidak terbaca dengan benar

**Solusi**:
- [ ] Refresh page (tekan F5)
- [ ] Logout → Login lagi
- [ ] Clear browser cache (Ctrl+Shift+Delete)

### Problem: Export CSV tidak berfungsi
**Penyebab**: Browser mungkin block download atau ada error

**Solusi**:
- [ ] Coba browser lain (Chrome, Firefox)
- [ ] Check folder Downloads untuk file
- [ ] Disable adblocker di browser
- [ ] Coba fitur Print ke PDF sebagai alternatif

### Problem: Tabel tidak muncul
**Penyebab**: Halaman mungkin belum fully load

**Solusi**:
- [ ] Tunggu beberapa detik
- [ ] Refresh page (F5)
- [ ] Klik tombol "Tampilkan Data" lagi

---

## 💡 TIPS & TRICKS

### Tip 1: Filter Dokter Produktif
Setelah lihat laporan:
1. Export ke CSV
2. Buka di Excel
3. Sort kolom "Nama Dokter"
4. Lihat dokter mana yang paling banyak operasi
→ Helps tracking dokter productivity!

### Tip 2: Track Asuransi Klien
Setelah lihat laporan:
1. Lihat statistik "Asuransi Unik"
2. Lihat kolom "Perusahaan/Asuransi"
3. Hitung jumlah operasi per asuransi
→ Helps understanding klien yang paling besar!

### Tip 3: Monthly Revenue Tracking
Setiap bulan:
1. Buka laporan bulanan
2. Lihat "Total Pendapatan"
3. Catat nilai tersebut
4. Bandingkan dengan bulan lalu
→ Easy way to track revenue trend!

### Tip 4: Archive Laporan
Setiap akhir bulan:
1. Buka laporan bulan tersebut
2. Export ke CSV
3. Rename file: `Laporan_Operasi_Januari_2026.csv`
4. Simpan di folder khusus untuk archieve
→ Good documentation practice!

---

## 🔐 REMEMBER

- ✅ Only latest operation data is shown (version control active)
- ✅ Only you (as logged in user) can access this report
- ✅ Data is secure and validated
- ✅ Export files are safe to share
- ✅ You can always come back and check old months

---

## 📞 NEED HELP?

1. **Quick Answer?** → Check FAQ section in MONTHLY_REPORT_GUIDE.md
2. **Want More Details?** → Read MONTHLY_REPORT_GUIDE.md
3. **Having Error?** → Check TROUBLESHOOTING in MONTHLY_REPORT_GUIDE.md
4. **Technical Issue?** → Contact IT Support

---

## 🎓 NEXT STEPS

After you've completed this checklist:

1. **Get Comfortable**
   - [ ] Use feature for 1-2 days
   - [ ] Try all export options
   - [ ] Explore different months

2. **Learn Advanced Usage**
   - [ ] Read MONTHLY_REPORT_GUIDE.md for more details
   - [ ] Try all available features
   - [ ] Understand all statistics

3. **Use for Work**
   - [ ] Make monthly reports
   - [ ] Track dokter productivity
   - [ ] Monitor revenue
   - [ ] Share with management

4. **Share with Colleagues**
   - [ ] Show them this feature
   - [ ] Share QUICKSTART guide
   - [ ] Help them get started

---

## ✨ COMMON USE CASES

### Use Case 1: Daily Monitoring
```
Waktu: 4 PM setiap hari
Tujuan: Check progress operasi hari ini/bulan ini
Langkah:
1. Login → Laporan Bulanan
2. Lihat statistik
3. Scroll tabel untuk cek operasi terbaru
5. Logout
```

### Use Case 2: Monthly Report Generation
```
Waktu: Akhir bulan
Tujuan: Buat laporan bulanan
Langkah:
1. Buka Laporan Bulanan
2. Pastikan bulan benar
3. Export CSV
4. Buka di Excel
5. Format & add chart/analysis
6. Send ke manager
```

### Use Case 3: Dokter Productivity Check
```
Waktu: Setiap minggu/bulan
Tujuan: Check produktivitas dokter
Langkah:
1. Laporan Bulanan
2. Export CSV
3. Pivot table di Excel: Count by Nama Dokter
4. Sort descending
5. Analyze hasil
```

### Use Case 4: Asuransi Revenue Tracking
```
Waktu: Monthly/Quarterly
Tujuan: Track asuransi klien
Langkah:
1. Laporan Bulanan
2. Export CSV
3. Pivot table: Sum(Total) by Asuransi
4. Analyze trend
```

---

## 🎯 SUCCESS CRITERIA

You'll know you've successfully used the feature when:

- [ ] ✅ Page loads without error
- [ ] ✅ Can see statistics correctly
- [ ] ✅ Can see table data
- [ ] ✅ Can export CSV
- [ ] ✅ Can print/export PDF
- [ ] ✅ Can view detail operasi
- [ ] ✅ Can change month and see different data
- [ ] ✅ Understand what all columns mean
- [ ] ✅ Can use for your work

---

## 📋 QUICK REFERENCE CARD

Save this for quick access:

```
MONTHLY REPORT QUICK ACTIONS:

1. ACCESS:
   Menu → Laporan Bulanan

2. PICK MONTH:
   Dropdown → Select Month → Tampilkan Data

3. VIEW DATA:
   Lihat Statistik & Tabel

4. EXPORT CSV:
   Opsi Ekspor → Export CSV

5. EXPORT PDF:
   Cetak → Save as PDF

6. VIEW DETAIL:
   Klik ikon mata di tabel
```

---

**Congratulations! You're ready to use Monthly Report! 🎉**

Remember: If you have any issues, check the troubleshooting section or
contact IT Support.

**Happy reporting! 📊**

---

Last Updated: January 9, 2026
Version: 1.0
Status: Ready ✅

