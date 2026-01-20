# Feature: Auto-Populate Surgeon Price

## Deskripsi
Fitur ini memungkinkan harga operasi (surgeon) otomatis muncul di kolom "Surgeon" ketika user memilih tabel operasi dari form input PBO.

## Cara Kerja

### 1. User memilih Operasi
Ketika user memilih operasi dari dropdown di tabel operasi:
```
[Pilih Tindakan Operasi dropdown] ← User memilih di sini
```

### 2. Event Listener Triggered
JavaScript event listener menangkap perubahan:
```javascript
$(document).on('change', '.operation-select', function() {
    // Fetch harga operasi dari API
});
```

### 3. API Call ke Backend
Mengirim request ke endpoint `/api/get-operation-price`:
```json
POST /api/get-operation-price
{
  "kode": "4199999994"  // atau "TINDAKAN-5"
}
```

### 4. Backend Returns Price
API mengembalikan harga operasi:
```json
{
  "success": true,
  "type": "operation",  // atau "tindakan"
  "price": 4934000,
  "nama_tindakan": "DOCTORS PROCEDURE TABLE 3"
}
```

### 5. Auto-Populate Surgeon Field
Harga otomatis diisi ke kolom "Surgeon":
```
Surgeon: Rp 4.934.000
```

### 6. Apply Percentage
Jika user memilih persentase (20%, 50%, 100%), harga akan disesuaikan:
```
If 50% selected:
Surgeon: Rp 2.467.000
```

### 7. Calculate Total
Total biaya otomatis diperbarui.

## Supported Operation Types

### 1. Operation Table (OperationTable)
- Format: `"4199999994 - DOCTORS PROCEDURE TABLE 3"`
- Price field: `biaya_dokter`

### 2. Tindakan Items (TindakanItem)
- Format: `"TINDAKAN-5 - Nama Tindakan"`
- Price field: `amount`

## API Endpoint

### GET `/api/get-operation-price`
**Request:**
```json
{
  "kode": "4199999994"
}
```

**Response (Operation Table):**
```json
{
  "success": true,
  "type": "operation",
  "price": 4934000,
  "biaya_dokter": 4934000,
  "biaya_rs": 0,
  "nama_tindakan": "DOCTORS PROCEDURE TABLE 3"
}
```

**Response (Tindakan Item):**
```json
{
  "success": true,
  "type": "tindakan",
  "price": 50000,
  "amount": 50000,
  "nama_tindakan": "Nama Tindakan"
}
```

## Implementation Details

### Frontend (input_pbo.html)
```javascript
// Listen for operation selection
$(document).on('change', '.operation-select', function() {
    const rowId = $(this).closest('.operation-row').data('row-id');
    const selectedValue = $(this).val();
    
    if (selectedValue && selectedValue.trim()) {
        const kode = selectedValue.split(' - ')[0].trim();
        
        // Fetch price
        $.ajax({
            url: '/api/get-operation-price',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ kode: kode }),
            success: function(response) {
                if (response.success) {
                    const price = response.price;
                    const percentage = parseFloat($(`#operation_persentase_${rowId}`).val() || 100);
                    const finalPrice = price * (percentage > 1 ? percentage / 100 : percentage);
                    
                    $('#surgeon').val(formatNumber(finalPrice));
                    calculateTotal();
                }
            }
        });
    }
});
```

### Backend (app.py)
```python
@app.route('/api/get-operation-price', methods=['POST'])
def api_get_operation_price():
    """API endpoint to get operation price by operation code"""
    data = request.get_json()
    kode = data.get('kode', '').strip()
    
    # Extract operation code (remove description if present)
    kode = kode.split(' - ')[0].strip()
    
    # Try OperationTable first
    operation = db_helper.get_operation_by_code(kode)
    if operation:
        return jsonify({
            'success': True,
            'type': 'operation',
            'price': operation['biaya_dokter'],
            ...
        })
    
    # Try TindakanItem
    if kode.startswith('TINDAKAN-'):
        tindakan_id = int(kode.replace('TINDAKAN-', '').strip())
        tindakan = db_helper.get_tindakan_by_id(tindakan_id)
        if tindakan:
            return jsonify({
                'success': True,
                'type': 'tindakan',
                'price': tindakan['amount'],
                ...
            })
    
    return jsonify({'success': False, 'error': 'Not found'}), 404
```

## Testing

### Manual Test
1. Buka form input PBO
2. Pilih Kelas (misal: BASIC)
3. Pilih Tindakan Operasi dari dropdown
4. Lihat harga otomatis muncul di kolom "Surgeon"
5. Ubah persentase, harga akan disesuaikan

### Expected Behavior
- Surgeon field auto-populated dengan harga operasi
- Harga berubah saat persentase diubah
- Total biaya otomatis dihitung

## Notes
- Fitur ini berjalan setelah operasi dipilih (real-time)
- Tidak mengganggu fungsi "Hitung Biaya Operasi" button yang sudah ada
- Kompatibel dengan percentage selection
- Works untuk both OperationTable dan TindakanItem
