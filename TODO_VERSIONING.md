# TODO - PBO Versioning System Implementation

## Progress Tracking

### ✅ Completed
- [x] Update database schema dengan kolom versioning
- [x] Tambah fungsi `create_pbo_version()` di models.py
- [x] Tambah fungsi `get_pbo_versions()` di models.py
- [x] Tambah fungsi `restore_pbo_version()` di models.py
- [x] Tambah fungsi `compare_pbo_versions()` di models.py
- [x] Tambah fungsi `_cleanup_old_versions()` (max 10 versions)
- [x] Tambah fungsi `get_all_latest_pbo()` di models.py
- [x] Tambah fungsi `search_latest_pbo()` di models.py
- [x] Tambah fungsi `count_latest_pbo()` di models.py
- [x] Update route `/` (index) untuk gunakan `count_latest_pbo()`
- [x] Update route `/search` untuk gunakan `search_latest_pbo()`

### 🔄 In Progress
- [ ] Update route `/edit/<int:pbo_id>` untuk create version (NEXT)
- [ ] Tambah route baru untuk versioning

### ⏳ Pending
- [ ] Update route `/edit/<int:pbo_id>` untuk create version instead of update
- [ ] Tambah route `/history/<int:pbo_id>` untuk view history
- [ ] Tambah route `/compare/<int:v1>/<int:v2>` untuk compare
- [ ] Tambah route `/restore/<int:version_id>` untuk restore
- [ ] Update template `detail_pbo.html` - tambah version badge & history link
- [ ] Buat template `pbo_history.html` - tampilkan all versions
- [ ] Buat template `pbo_compare.html` - compare 2 versions
- [ ] Update template `edit_pbo.html` - info create new version
- [ ] Testing semua fitur versioning

## Implementation Details

### Database Schema Changes
- `version_number`: INTEGER - nomor versi (1, 2, 3, ...)
- `parent_id`: INTEGER - ID dari versi pertama (root)
- `is_latest`: INTEGER - flag versi terbaru (1 = latest, 0 = old)
- `edited_by`: TEXT - username yang mengedit
- `edited_at`: TIMESTAMP - waktu edit

### Key Features
1. **Auto Versioning**: Setiap edit create versi baru
2. **Version History**: Lihat semua versi dengan detail
3. **Compare Versions**: Bandingkan 2 versi side-by-side
4. **Restore Version**: Kembalikan ke versi sebelumnya
5. **Auto Cleanup**: Simpan max 10 versi terakhir
6. **User Tracking**: Track siapa yang edit

### Next Steps
1. Update app.py untuk gunakan fungsi versioning
2. Buat templates untuk UI versioning
3. Testing end-to-end
4. Update dokumentasi

---
Last Updated: 2024
