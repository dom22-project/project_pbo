# PBO Versioning System - Implementation Guide

## 📋 Overview

Sistem versioning untuk data PBO sudah diimplementasikan di level backend (database & models). Dokumen ini menjelaskan apa yang sudah selesai dan bagaimana melanjutkan implementasi.

---

## ✅ Yang Sudah Diimplementasikan

### 1. Database Schema (models.py)

**Kolom Baru di Tabel `database`:**
```sql
- version_number INTEGER DEFAULT 1      -- Nomor versi (1, 2, 3, ...)
- parent_id INTEGER                     -- ID versi pertama (root)
- is_latest INTEGER DEFAULT 1           -- Flag versi terbaru (1/0)
- edited_by TEXT                        -- Username yang mengedit
- edited_at TIMESTAMP                   -- Waktu edit
```

**Auto Migration:**
- Kolom otomatis ditambahkan saat aplikasi dijalankan
- Data existing otomatis di-set sebagai version 1

### 2. Fungsi Versioning (models.py)

#### `create_pbo_version(parent_id, data, username)`
Membuat versi baru dari PBO yang di-edit.
```python
# Contoh penggunaan:
new_version_id = db.create_pbo_version(
    parent_id=pbo_id,
    data=form_data_tuple,
    username=session['username']
)
```

**Fitur:**
- Set versi lama menjadi `is_latest = 0`
- Create versi baru dengan `version_number` increment
- Auto cleanup jika versi > 10
- Track user yang mengedit

#### `get_pbo_versions(pbo_id)`
Ambil semua versi dari satu PBO.
```python
# Contoh penggunaan:
versions = db.get_pbo_versions(pbo_id)
# Returns: list of dict dengan info versi
```

**Return Data:**
```python
[
    {
        'id': 123,
        'version_number': 3,
        'is_latest': 1,
        'edited_by': 'user123',
        'edited_at': '2024-01-15 10:30:00',
        'nama_pasien': 'John Doe',
        'total': 5000000,
        ...
    },
    ...
]
```

#### `restore_pbo_version(version_id, username)`
Restore versi lama sebagai versi terbaru.
```python
# Contoh penggunaan:
restored_id = db.restore_pbo_version(
    version_id=old_version_id,
    username=session['username']
)
```

**Fitur:**
- Copy data dari versi lama
- Create sebagai versi baru (increment version_number)
- Set sebagai latest version

#### `compare_pbo_versions(version1_id, version2_id)`
Bandingkan 2 versi dan tampilkan perbedaan.
```python
# Contoh penggunaan:
comparison = db.compare_pbo_versions(v1_id, v2_id)
```

**Return Data:**
```python
{
    'version1': {...},  # Data versi 1
    'version2': {...},  # Data versi 2
    'differences': [
        {
            'field': 'total',
            'version1_value': 5000000,
            'version2_value': 5500000
        },
        ...
    ],
    'has_differences': True
}
```

#### `get_all_latest_pbo(limit, offset)`
Ambil hanya versi terbaru dari semua PBO.

#### `search_latest_pbo(field, value)`
Search hanya di versi terbaru.

#### `count_latest_pbo()`
Hitung total PBO (versi terbaru saja).

### 3. Routes yang Sudah Diupdate (app.py)

```python
# Dashboard - gunakan latest version
@app.route('/')
def index():
    total_pbo = db.count_latest_pbo()
    recent_pbo = db.get_all_latest_pbo(limit=5)
    ...

# Search - gunakan latest version
@app.route('/search')
def search_pbo():
    results = db.search_latest_pbo(field, value)
    ...
```

---

## 🔧 Yang Perlu Dilanjutkan

### 1. Update Route Edit (app.py)

**File:** `app.py`
**Route:** `/edit/<int:pbo_id>`

**Perubahan yang diperlukan:**

```python
@app.route('/edit/<int:pbo_id>', methods=['GET', 'POST'])
@login_required
def edit_pbo(pbo_id):
    if request.method == 'POST':
        try:
            # ... (kode form data sama seperti sekarang)
            
            # GANTI INI:
            # db.update_pbo(pbo_id, data)
            
            # DENGAN INI:
            new_version_id = db.create_pbo_version(
                parent_id=pbo_id,
                data=data,
                username=session['username']
            )
            
            flash(f'Data PBO berhasil diupdate (Versi baru: {new_version_id})', 'success')
            return redirect(url_for('detail_pbo', pbo_id=new_version_id))
            
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('edit_pbo', pbo_id=pbo_id))
    
    # GET request tetap sama
    ...
```

### 2. Tambah Route History (app.py)

```python
@app.route('/history/<int:pbo_id>')
@login_required
def pbo_history(pbo_id):
    """View version history of PBO"""
    # Get all versions
    versions = db.get_pbo_versions(pbo_id)
    
    if not versions:
        flash('Data PBO tidak ditemukan', 'danger')
        return redirect(url_for('search_pbo'))
    
    # Get current PBO data for context
    current_pbo = db.get_pbo_by_id(pbo_id)
    
    return render_template('pbo_history.html', 
                         versions=versions,
                         current_pbo=current_pbo)
```

### 3. Tambah Route Compare (app.py)

```python
@app.route('/compare/<int:version1_id>/<int:version2_id>')
@login_required
def compare_versions(version1_id, version2_id):
    """Compare two versions of PBO"""
    comparison = db.compare_pbo_versions(version1_id, version2_id)
    
    if not comparison:
        flash('Versi tidak ditemukan', 'danger')
        return redirect(url_for('search_pbo'))
    
    return render_template('pbo_compare.html', 
                         comparison=comparison)
```

### 4. Tambah Route Restore (app.py)

```python
@app.route('/restore/<int:version_id>', methods=['POST'])
@login_required
def restore_version(version_id):
    """Restore a previous version"""
    try:
        restored_id = db.restore_pbo_version(
            version_id=version_id,
            username=session['username']
        )
        
        if restored_id:
            flash(f'Versi berhasil di-restore sebagai versi terbaru (ID: {restored_id})', 'success')
            return redirect(url_for('detail_pbo', pbo_id=restored_id))
        else:
            flash('Gagal restore versi', 'danger')
            return redirect(url_for('search_pbo'))
            
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
        return redirect(url_for('search_pbo'))
```

### 5. Update Template detail_pbo.html

**Tambahkan di bagian header:**

```html
<!-- Version Badge -->
{% if pbo.version_number %}
<div class="alert alert-info">
    <strong>Versi:</strong> {{ pbo.version_number }}
    {% if pbo.edited_by %}
    | <strong>Diedit oleh:</strong> {{ pbo.edited_by }}
    | <strong>Waktu:</strong> {{ pbo.edited_at }}
    {% endif %}
    
    <!-- Link to History -->
    <a href="{{ url_for('pbo_history', pbo_id=pbo.id) }}" class="btn btn-sm btn-primary float-right">
        <i class="fas fa-history"></i> Lihat History
    </a>
</div>
{% endif %}
```

### 6. Buat Template pbo_history.html

```html
{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <h2>History Versi - {{ current_pbo.nama_pasien }}</h2>
    
    <div class="card">
        <div class="card-body">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Versi</th>
                        <th>Tanggal</th>
                        <th>Diedit Oleh</th>
                        <th>Total</th>
                        <th>Status</th>
                        <th>Aksi</th>
                    </tr>
                </thead>
                <tbody>
                    {% for version in versions %}
                    <tr>
                        <td>{{ version.version_number }}</td>
                        <td>{{ version.edited_at or version.created_at }}</td>
                        <td>{{ version.edited_by or '-' }}</td>
                        <td>{{ version.total|currency }}</td>
                        <td>
                            {% if version.is_latest %}
                            <span class="badge badge-success">Latest</span>
                            {% else %}
                            <span class="badge badge-secondary">Old</span>
                            {% endif %}
                        </td>
                        <td>
                            <a href="{{ url_for('detail_pbo', pbo_id=version.id) }}" 
                               class="btn btn-sm btn-info">View</a>
                            
                            {% if not version.is_latest %}
                            <form method="POST" action="{{ url_for('restore_version', version_id=version.id) }}" 
                                  style="display:inline;">
                                <button type="submit" class="btn btn-sm btn-warning"
                                        onclick="return confirm('Restore versi ini?')">
                                    Restore
                                </button>
                            </form>
                            {% endif %}
                            
                            {% if loop.index < versions|length %}
                            <a href="{{ url_for('compare_versions', 
                                      version1_id=version.id, 
                                      version2_id=versions[loop.index].id) }}" 
                               class="btn btn-sm btn-secondary">Compare</a>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```

### 7. Buat Template pbo_compare.html

```html
{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <h2>Perbandingan Versi</h2>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    Versi {{ comparison.version1.version_number }}
                </div>
                <div class="card-body">
                    <p><strong>Total:</strong> {{ comparison.version1.total|currency }}</p>
                    <p><strong>Tanggal:</strong> {{ comparison.version1.tanggal }}</p>
                    <!-- Tambahkan field lain yang penting -->
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-success text-white">
                    Versi {{ comparison.version2.version_number }}
                </div>
                <div class="card-body">
                    <p><strong>Total:</strong> {{ comparison.version2.total|currency }}</p>
                    <p><strong>Tanggal:</strong> {{ comparison.version2.tanggal }}</p>
                    <!-- Tambahkan field lain yang penting -->
                </div>
            </div>
        </div>
    </div>
    
    {% if comparison.has_differences %}
    <div class="card mt-4">
        <div class="card-header">
            <h4>Perbedaan</h4>
        </div>
        <div class="card-body">
            <table class="table">
                <thead>
                    <tr>
                        <th>Field</th>
                        <th>Versi {{ comparison.version1.version_number }}</th>
                        <th>Versi {{ comparison.version2.version_number }}</th>
                    </tr>
                </thead>
                <tbody>
                    {% for diff in comparison.differences %}
                    <tr>
                        <td><strong>{{ diff.field }}</strong></td>
                        <td>{{ diff.version1_value }}</td>
                        <td class="bg-warning">{{ diff.version2_value }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    {% else %}
    <div class="alert alert-info mt-4">
        Tidak ada perbedaan antara kedua versi.
    </div>
    {% endif %}
</div>
{% endblock %}
```

### 8. Update Template edit_pbo.html

**Tambahkan info di bagian atas form:**

```html
<div class="alert alert-warning">
    <i class="fas fa-info-circle"></i>
    <strong>Perhatian:</strong> Saat Anda menyimpan perubahan, sistem akan membuat versi baru dari data PBO ini. 
    Data versi sebelumnya akan tetap tersimpan dan dapat dilihat di history.
</div>
```

---

## 🧪 Testing Checklist

### Test 1: Create PBO Baru
- [ ] Buat PBO baru
- [ ] Cek version_number = 1
- [ ] Cek is_latest = 1
- [ ] Cek parent_id = NULL

### Test 2: Edit PBO (Create Version)
- [ ] Edit PBO existing
- [ ] Cek versi baru dibuat
- [ ] Cek version_number increment
- [ ] Cek versi lama is_latest = 0
- [ ] Cek versi baru is_latest = 1
- [ ] Cek edited_by terisi username
- [ ] Cek edited_at terisi timestamp

### Test 3: View History
- [ ] Akses halaman history
- [ ] Cek semua versi tampil
- [ ] Cek urutan versi (terbaru di atas)
- [ ] Cek badge "Latest" tampil di versi terbaru

### Test 4: Compare Versions
- [ ] Pilih 2 versi untuk compare
- [ ] Cek perbedaan tampil dengan benar
- [ ] Cek field yang berbeda di-highlight

### Test 5: Restore Version
- [ ] Restore versi lama
- [ ] Cek versi baru dibuat (bukan overwrite)
- [ ] Cek data sama dengan versi yang di-restore
- [ ] Cek version_number increment

### Test 6: Cleanup Old Versions
- [ ] Buat lebih dari 10 versi
- [ ] Cek hanya 10 versi terakhir yang tersimpan
- [ ] Cek versi terlama otomatis terhapus

### Test 7: Search & Dashboard
- [ ] Cek search hanya tampilkan latest version
- [ ] Cek dashboard count hanya latest version
- [ ] Cek recent PBO hanya latest version

---

## 📝 Notes

1. **Backward Compatibility:** Data existing otomatis di-set sebagai version 1
2. **Performance:** Index pada kolom `is_latest` untuk query cepat
3. **Storage:** Max 10 versi per PBO untuk hemat storage
4. **User Tracking:** Semua perubahan ter-track dengan username & timestamp

---

## 🆘 Troubleshooting

### Error: Column not found
**Solusi:** Restart aplikasi untuk trigger auto migration

### Versi tidak muncul di history
**Solusi:** Cek `parent_id` dan `is_latest` di database

### Cleanup tidak jalan
**Solusi:** Cek fungsi `_cleanup_old_versions()` dipanggil di `create_pbo_version()`

---

**Last Updated:** 2024
**Status:** Backend Complete, Frontend Pending
