# Quick Start Guide - Web Application

Panduan cepat untuk menjalankan aplikasi web PBO.

## 🚀 Langkah Cepat (5 Menit)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi

```bash
python app.py
```

### 3. Buka Browser

Akses: **http://localhost:5000**

## ✅ Selesai!

Aplikasi web sudah berjalan dan siap digunakan.

---

## 📝 Langkah Detail

### Persiapan

1. **Pastikan Python terinstall**
   ```bash
   python --version
   # Harus Python 3.7 atau lebih tinggi
   ```

2. **Clone atau download project**
   ```bash
   cd "c:/Users/agung.daniel/Project PBO/app pbo"
   ```

3. **Install dependencies**
   ```bash
   pip install Flask Werkzeug Jinja2 WeasyPrint
   ```
   
   Atau gunakan requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

### Menjalankan Aplikasi

**Development Mode:**
```bash
python app.py
```

Aplikasi akan berjalan di:
- URL: http://localhost:5000
- Host: 0.0.0.0 (accessible dari network)
- Debug: True (auto-reload on code changes)

**Production Mode (dengan Gunicorn):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Mengakses Aplikasi

1. **Dari komputer yang sama:**
   - http://localhost:5000
   - http://127.0.0.1:5000

2. **Dari komputer lain di network yang sama:**
   - http://[IP-ADDRESS]:5000
   - Contoh: http://192.168.1.100:5000

3. **Cek IP Address:**
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

## 🎯 Fitur Utama

### 1. Dashboard
- Statistik total data PBO
- Data terbaru
- Quick actions

### 2. Input Data PBO
- Form lengkap dengan validasi
- Auto-calculation biaya
- Real-time total calculation

### 3. Cari Data
- Search by multiple criteria
- View, Edit, Delete, Print

### 4. Detail & Edit
- View full details
- Edit existing data
- Print form

## 🔧 Troubleshooting

### Port sudah digunakan?

Edit `app.py`, ubah port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module tidak ditemukan?

Install ulang dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### Database error?

Pastikan folder `data/` ada:
```bash
mkdir data
```

### Browser tidak bisa akses?

1. Cek firewall
2. Pastikan aplikasi running
3. Coba http://127.0.0.1:5000

## 📱 Akses dari Mobile

1. Pastikan mobile dan komputer di network yang sama
2. Cek IP address komputer (ipconfig/ifconfig)
3. Buka browser di mobile
4. Akses: http://[IP-KOMPUTER]:5000

## 🛑 Menghentikan Aplikasi

Tekan `Ctrl + C` di terminal

## 📊 Struktur URL

| URL | Fungsi |
|-----|--------|
| `/` | Dashboard |
| `/input` | Input data PBO |
| `/search` | Cari data |
| `/detail/<id>` | Detail PBO |
| `/edit/<id>` | Edit PBO |
| `/print/<id>` | Cetak form |

## 💡 Tips

1. **Auto-reload**: Dalam development mode, perubahan code akan otomatis reload
2. **Debug mode**: Error akan ditampilkan detail di browser
3. **Database**: File database ada di `data/pbo_database.db`
4. **Backup**: Backup database secara berkala

## 🔐 Keamanan

Untuk production:
1. Set `debug=False` di app.py
2. Gunakan secret key yang kuat di config.py
3. Gunakan HTTPS
4. Setup firewall
5. Gunakan gunicorn atau uwsgi

## 📞 Bantuan

Jika ada masalah:
1. Cek console/terminal untuk error messages
2. Cek browser console (F12)
3. Lihat WEB_README.md untuk dokumentasi lengkap
4. Hubungi IT Support RS Siloam TB Simatupang

---

**Happy Coding! 🎉**
