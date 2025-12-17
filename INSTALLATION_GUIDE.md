# Installation Guide - Sistem Manajemen PBO

## Panduan Instalasi Lengkap untuk Aplikasi PBO RS Sumber Hidup

---

## Prerequisites

### 1. Python
- **Versi Required:** Python 3.8 atau lebih tinggi
- **Check Version:**
  ```bash
  python --version
  ```
  atau
  ```bash
  python3 --version
  ```

### 2. pip (Python Package Manager)
- Biasanya sudah terinstall dengan Python
- **Check Version:**
  ```bash
  pip --version
  ```

### 3. Git (Optional)
- Untuk clone repository
- Download dari: https://git-scm.com/

---

## Step-by-Step Installation

### Step 1: Clone atau Download Project

#### Option A: Clone dengan Git
```bash
git clone <repository-url>
cd "app pbo"
```

#### Option B: Download ZIP
1. Download project sebagai ZIP
2. Extract ke folder pilihan Anda
3. Buka terminal/command prompt di folder tersebut

---

### Step 2: Create Virtual Environment (Recommended)

Virtual environment membantu mengisolasi dependencies project.

#### Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### Linux/Mac:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**Note:** Setelah aktivasi, Anda akan melihat `(venv)` di awal command prompt.

---

### Step 3: Install Python Dependencies

Install semua package yang diperlukan dari requirements.txt:

```bash
pip install -r requirements.txt
```

**Proses ini akan menginstall:**
- Flask 3.0.0 (Web Framework)
- WeasyPrint 60.1 (PDF Generation)
- openpyxl 3.1.2 (Excel Processing)
- Dan semua dependencies lainnya

**Estimasi waktu:** 2-5 menit (tergantung koneksi internet)

---

### Step 4: Download Frontend Dependencies

Frontend dependencies (Select2, Bootstrap, dll) sudah tersedia sebagai local files.

Jika belum ada, jalankan script helper:

```bash
python download_dependencies.py
```

**Script ini akan download:**
- Select2 CSS & JS
- Select2 Bootstrap 5 Theme

**Lokasi:** `static/vendor/select2/`

---

### Step 5: Initialize Database

Database SQLite akan otomatis dibuat saat pertama kali aplikasi dijalankan.

**Lokasi database:** `data/pbo_database.db`

Jika ingin membuat database secara manual:

```bash
python -c "from models import Database; db = Database(); print('Database initialized!')"
```

---

### Step 6: Run Application

Jalankan aplikasi Flask:

```bash
python app.py
```

**Output yang diharapkan:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://10.83.48.90:5000
Press CTRL+C to quit
```

---

### Step 7: Access Application

Buka browser dan akses:
- **Local:** http://127.0.0.1:5000
- **Network:** http://10.83.48.90:5000 (dari device lain di network yang sama)

---

## Verification Checklist

Setelah instalasi, verifikasi hal-hal berikut:

### ✅ Python Dependencies
```bash
pip list
```
Pastikan semua package dari requirements.txt terinstall.

### ✅ Frontend Dependencies
```bash
# Windows
dir static\vendor\select2 /s

# Linux/Mac
ls -R static/vendor/select2
```
Pastikan ada 3 files:
- select2.min.css
- select2-bootstrap-5-theme.min.css
- select2.min.js

### ✅ Database
```bash
# Windows
dir data

# Linux/Mac
ls -la data
```
Pastikan ada file `pbo_database.db`

### ✅ Application Running
- Buka http://127.0.0.1:5000
- Pastikan halaman home muncul tanpa error
- Check browser console (F12) untuk error JavaScript

---

## Troubleshooting

### Problem 1: pip command not found
**Solution:**
```bash
# Windows
python -m pip install -r requirements.txt

# Linux/Mac
python3 -m pip install -r requirements.txt
```

### Problem 2: Permission denied (Linux/Mac)
**Solution:**
```bash
# Add --user flag
pip install --user -r requirements.txt

# Or use sudo (not recommended)
sudo pip install -r requirements.txt
```

### Problem 3: WeasyPrint installation error
**Solution:**

**Windows:**
- Install GTK3 runtime: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
- Atau gunakan pre-built wheels

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-dev python3-pip python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

**Mac:**
```bash
brew install python3 cairo pango gdk-pixbuf libffi
```

### Problem 4: Port 5000 already in use
**Solution:**
Edit `app.py` dan ubah port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Ganti 5000 ke 5001
```

### Problem 5: Database locked error
**Solution:**
- Tutup semua instance aplikasi yang sedang berjalan
- Delete file `pbo_database.db` dan restart aplikasi
- Database akan dibuat ulang otomatis

### Problem 6: Select2 not working
**Solution:**
1. Check browser console untuk error
2. Pastikan file Select2 ada di `static/vendor/select2/`
3. Jalankan: `python download_dependencies.py`
4. Clear browser cache (Ctrl+F5)

---

## Update Dependencies

Untuk update semua dependencies ke versi terbaru:

```bash
# Backup requirements.txt lama
cp requirements.txt requirements.txt.backup

# Update all packages
pip install --upgrade -r requirements.txt

# Generate new requirements.txt
pip freeze > requirements.txt
```

**Warning:** Update dependencies bisa menyebabkan breaking changes. Test aplikasi setelah update.

---

## Uninstall

### Remove Virtual Environment
```bash
# Deactivate first
deactivate

# Remove venv folder
# Windows
rmdir /s venv

# Linux/Mac
rm -rf venv
```

### Remove All Dependencies
```bash
pip uninstall -r requirements.txt -y
```

---

## Production Deployment

### Using Gunicorn (Linux/Mac)

1. **Install Gunicorn** (sudah ada di requirements.txt)

2. **Run with Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

**Options:**
- `-w 4`: 4 worker processes
- `-b 0.0.0.0:8000`: Bind to all interfaces on port 8000
- `app:app`: module:application

3. **Run as Background Service:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app --daemon
```

### Using Nginx (Reverse Proxy)

1. **Install Nginx:**
```bash
sudo apt-get install nginx
```

2. **Configure Nginx:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/app/static;
    }
}
```

3. **Restart Nginx:**
```bash
sudo systemctl restart nginx
```

---

## Environment Variables

Create `.env` file untuk konfigurasi:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Database
DATABASE_PATH=data/pbo_database.db

# Server
HOST=0.0.0.0
PORT=5000
```

Load dengan python-dotenv (sudah terinstall):
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## System Requirements

### Minimum:
- **CPU:** 1 Core
- **RAM:** 512 MB
- **Storage:** 100 MB
- **OS:** Windows 7+, Linux, macOS 10.12+

### Recommended:
- **CPU:** 2+ Cores
- **RAM:** 2 GB
- **Storage:** 500 MB
- **OS:** Windows 10+, Ubuntu 20.04+, macOS 11+

---

## Support

Jika mengalami masalah saat instalasi:

1. Check dokumentasi di folder project:
   - `README.md`
   - `QUICK_START.md`
   - `CHANGELOG.md`

2. Check log error di terminal

3. Contact developer atau IT support

---

## Version Information

- **Application Version:** 1.0.0
- **Python Version:** 3.8+
- **Flask Version:** 3.0.0
- **Last Updated:** 2024-11-20

---

## License

© 2024 RS Sumber Hidup. All rights reserved.
