# Panduan Autentikasi Sistem PBO

## Overview
Sistem PBO sekarang dilengkapi dengan fitur autentikasi untuk mengontrol akses pengguna.

## Level User

### 1. Admin
- **Username**: `admin`
- **Password**: `admin123`
- **Hak Akses**:
  - ✅ View/Lihat data PBO
  - ✅ Input data PBO baru
  - ✅ Edit data PBO
  - ✅ **Hapus data PBO** (Khusus Admin)
  - ✅ Print/Cetak form PBO
  - ✅ Upload database
  - ✅ Manage data tindakan (view, add, edit, delete)

### 2. User Biasa
- **Username**: `user`
- **Password**: `user123`
- **Hak Akses**:
  - ✅ View/Lihat data PBO
  - ✅ Input data PBO baru
  - ✅ Edit data PBO
  - ❌ **TIDAK bisa hapus data PBO**
  - ✅ Print/Cetak form PBO
  - ✅ Upload database
  - ✅ Manage data tindakan (view, add, edit)
  - ❌ **TIDAK bisa hapus data tindakan**

## Cara Menggunakan

### Login
1. Akses aplikasi di `http://localhost:5000`
2. Anda akan diarahkan ke halaman login
3. Masukkan username dan password
4. Klik tombol "Login"

### Logout
1. Klik dropdown user di pojok kanan atas navbar
2. Klik "Logout"

## Fitur Keamanan

### Protected Routes
Semua halaman kecuali halaman login memerlukan autentikasi:
- Dashboard (/)
- Input PBO (/input)
- Search PBO (/search)
- Detail PBO (/detail/<id>)
- Edit PBO (/edit/<id>)
- Print PBO (/print/<id>)
- View Tindakan (/view-tindakan)
- Upload Database (/upload-database)

### Admin-Only Routes
Route berikut hanya bisa diakses oleh admin:
- Delete PBO (/delete/<id>)
- Delete Tindakan (/tindakan/delete/<id>)

### Session Management
- Session disimpan di server
- Otomatis redirect ke login jika belum login
- Otomatis redirect ke dashboard jika sudah login dan mengakses halaman login

## UI Changes

### Navbar
- Menampilkan username dan role (Admin/User) di pojok kanan
- Badge warna kuning untuk Admin
- Badge warna biru untuk User biasa
- Dropdown menu untuk logout

### Detail PBO Page
- Tombol "Hapus Data" hanya muncul untuk Admin
- User biasa tidak melihat tombol hapus

## Database Schema

### Tabel Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Default Users
Saat pertama kali aplikasi dijalankan, 2 user default akan dibuat otomatis:
1. admin / admin123 (role: admin)
2. user / user123 (role: user)

## Catatan Keamanan

⚠️ **PENTING**: 
- Password disimpan dalam plain text (tidak di-hash)
- Untuk production, sebaiknya gunakan password hashing (bcrypt/werkzeug.security)
- Ganti password default setelah deployment
- Gunakan HTTPS untuk production

## Troubleshooting

### Tidak bisa login
- Pastikan username dan password benar
- Cek apakah database sudah ter-initialize dengan benar
- Restart aplikasi jika perlu

### Tombol delete tidak muncul
- Pastikan login sebagai admin
- Cek badge di navbar, harus tertulis "Admin"

### Redirect loop
- Clear browser cookies/session
- Restart aplikasi Flask
