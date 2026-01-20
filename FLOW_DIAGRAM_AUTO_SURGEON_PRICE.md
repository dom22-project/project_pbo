# Auto-Surgeon Price Feature - Flow Diagram

## User Flow

```
┌─────────────────────────────────────────────────────────────┐
│ USER MEMBUKA FORM INPUT PBO                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ FORM DIMUAT                                                  │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Operasi Table Kosong                                   │  │
│ │ ┌─ No. ─┬──── Tindakan Operasi ────┬─ Persentase ─┬─ ┐ │
│ │ │  1    │ [Pilih Tindakan...] ▼     │  100%  ▼     │ X │ │
│ │ └────────┴──────────────────────────┴──────────────┴─ ┘ │
│ │                                                          │
│ │ Rincian Biaya                                           │
│ │ Surgeon: [0]                          ← WILL BE AUTO    │
│ │ Anesthesi: [0]                                          │
│ │ OT Room Charge: [0]                                     │
│ └────────────────────────────────────────────────────────┘
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ USER KLIK DROPDOWN "TINDAKAN OPERASI"                       │
│                                                              │
│ [Pilih Tindakan...] ▼                                        │
│ ┌─ 📋 Tabel Operasi Standard ──────────────────────────┐   │
│ │ > 4199999994 - DOCTORS PROCEDURE TABLE 3             │   │
│ │ > 4199999995 - DOCTORS PROCEDURE TABLE 1             │   │
│ │ > 4199999996 - DOCTORS PROCEDURE TABLE 2             │   │
│ ├─ 🏥 Data Tindakan Terbaru ───────────────────────────┤   │
│ │ > TINDAKAN-5 - Nama Tindakan A                       │   │
│ │ > TINDAKAN-6 - Nama Tindakan B                       │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                              │
│ USER MEMILIH: "4199999994 - DOCTORS PROCEDURE TABLE 3"      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼ CHANGE EVENT TRIGGERED
┌─────────────────────────────────────────────────────────────┐
│ JAVASCRIPT EVENT LISTENER AKTIF                             │
│                                                              │
│ $(document).on('change', '.operation-select', function() {  │
│   selectedValue = "4199999994 - DOCTORS PROCEDURE TABLE 3"  │
│   kode = "4199999994"                                        │
│   ...                                                        │
│ })                                                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼ AJAX REQUEST
┌─────────────────────────────────────────────────────────────┐
│ REQUEST DIKIRIM KE BACKEND                                   │
│                                                              │
│ POST /api/get-operation-price                               │
│ Content-Type: application/json                              │
│ {                                                            │
│   "kode": "4199999994"                                       │
│ }                                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ BACKEND PROCESSING (app.py)                                 │
│                                                              │
│ @app.route('/api/get-operation-price', methods=['POST'])    │
│ def api_get_operation_price():                              │
│   kode = "4199999994"                                       │
│   kode = kode.split(' - ')[0].strip()  # "4199999994"      │
│                                                              │
│   operation = db_helper.get_operation_by_code(kode)         │
│   │                                                          │
│   └─▶ SQL: SELECT * FROM operation_tables                  │
│       WHERE kode = '4199999994'                             │
│                                                              │
│   Found: OperationTable(                                    │
│       kode='4199999994',                                    │
│       nama_tindakan='DOCTORS PROCEDURE TABLE 3',            │
│       biaya_dokter=4934000,                                 │
│       biaya_rs=0                                            │
│   )                                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ RESPONSE DIKIRIM KE FRONTEND                                │
│                                                              │
│ HTTP 200 OK                                                  │
│ Content-Type: application/json                              │
│ {                                                            │
│   "success": true,                                           │
│   "type": "operation",                                       │
│   "price": 4934000,                                          │
│   "biaya_dokter": 4934000,                                   │
│   "biaya_rs": 0,                                             │
│   "nama_tindakan": "DOCTORS PROCEDURE TABLE 3"              │
│ }                                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ JAVASCRIPT SUCCESS CALLBACK                                  │
│                                                              │
│ success: function(response) {                               │
│   price = 4934000                                            │
│   percentage = 100% (default)                               │
│   finalPrice = 4934000 * 1.0 = 4934000                      │
│   $('#surgeon').val(formatNumber(4934000))                  │
│   calculateTotal()                                           │
│ }                                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ SURGEON FIELD AUTO-POPULATED                                │
│                                                              │
│ Rincian Biaya                                               │
│ Surgeon: [Rp 4.934.000] ◄─── UPDATED!                       │
│ Anesthesi: [0]                                              │
│ OT Room Charge: [0]                                         │
│                                                              │
│ TOTAL BIAYA: [Rp 4.934.000] ◄─── RECALCULATED!            │
└─────────────────────────────────────────────────────────────┘
```

## Percentage Application Flow

```
┌─────────────────────────────────────────────────────────────┐
│ USER MENGUBAH PERSENTASE                                    │
│                                                              │
│ [Persentase] ▼                                               │
│ ┌─ 20% ──────────────────────────────────────────────────┐  │
│ │ > 20%                                                  │  │
│ │ > 30%                                                  │  │
│ │ > 35%                                                  │  │
│ │ > 50%                                                  │  │
│ │ > 75%                                                  │  │
│ │ > 100% (dipilih sebelumnya)                           │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                              │
│ USER MEMILIH: 50%                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼ CHANGE EVENT TRIGGERED
┌─────────────────────────────────────────────────────────────┐
│ JAVASCRIPT UPDATES SURGEON PRICE                            │
│                                                              │
│ pricePercentage = 50                                         │
│ percentage = 50 > 1 ? 50/100 : 50 = 0.5                    │
│ finalPrice = 4934000 * 0.5 = 2.467.000                     │
│ $('#surgeon').val(formatNumber(2467000))                   │
│ calculateTotal()                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ SURGEON FIELD UPDATED                                        │
│                                                              │
│ Rincian Biaya                                               │
│ Surgeon: [Rp 2.467.000] ◄─── PERCENTAGE APPLIED!           │
│ Anesthesi: [0]                                              │
│ OT Room Charge: [0]                                         │
│                                                              │
│ TOTAL BIAYA: [Rp 2.467.000] ◄─── RECALCULATED!           │
└─────────────────────────────────────────────────────────────┘
```

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────┐
│ USER MEMILIH OPERASI YANG TIDAK VALID                       │
│ (Contoh: operasi dihapus dari database)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ BACKEND TIDAK MENEMUKAN OPERASI                             │
│                                                              │
│ operation = db_helper.get_operation_by_code("INVALID")     │
│ │ (returns None)                                            │
│                                                              │
│ HTTP 404 NOT FOUND                                          │
│ {                                                            │
│   "success": false,                                          │
│   "error": "Operation with code INVALID not found"          │
│ }                                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ JAVASCRIPT ERROR CALLBACK                                    │
│                                                              │
│ error: function(xhr, status, error) {                       │
│   console.error('Error fetching operation price:', error)   │
│   // Surgeon field tidak berubah                            │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
```

## Database Schema

```
┌──────────────────────────────────────┐
│ operation_tables                      │
├──────────────────────────────────────┤
│ id: INTEGER (PK)                     │
│ kode: STRING (UNIQUE)                │
│ nama_tindakan: STRING                │
│ kelas: STRING                        │
│ biaya_dokter: FLOAT      ◄─ USED     │
│ biaya_rs: FLOAT                      │
│ total_biaya: FLOAT                   │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ tindakan_items                        │
├──────────────────────────────────────┤
│ id: INTEGER (PK)                     │
│ nama_tindakan: STRING                │
│ kelas: STRING                        │
│ kategory: STRING                     │
│ sales_item_type: STRING              │
│ amount: FLOAT           ◄─ USED      │
│ created_at: DATETIME                 │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ database (PBOData)                    │
├──────────────────────────────────────┤
│ id: INTEGER (PK)                     │
│ nama_pasien: STRING                  │
│ diagnosa: STRING                     │
│ nama_operasi: STRING                 │
│ surgeon: FLOAT       ◄─ UPDATED HERE │
│ anesthesi: FLOAT                     │
│ ot_room_charge: FLOAT                │
│ total: FLOAT                         │
│ ...                                  │
└──────────────────────────────────────┘
```

## API Integration Points

```
FRONTEND (input_pbo.html)
         │
         │ POST /api/get-operation-price
         │ { "kode": "4199999994" }
         ▼
BACKEND (app.py)
         │
         ├─▶ db_helper.get_operation_by_code(kode)
         │   └─▶ DATABASE: operation_tables
         │
         ├─▶ db_helper.get_tindakan_by_id(id)
         │   └─▶ DATABASE: tindakan_items
         │
         └─▶ return { success, type, price, ... }
                    │
                    ▼
              FRONTEND
              Update #surgeon field
              Calculate total
```

## Component Interaction

```
┌────────────────────────────────────────────────────────┐
│                    FRONTEND (Browser)                   │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ HTML: Operasi Dropdown                           │  │
│  │ <select class="operation-select">                │  │
│  │   <option value="4199999994 - NAME">...</option> │  │
│  │ </select>                                        │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                     │
│                   ▼ user selects                        │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ JavaScript: Event Listener                       │  │
│  │ $(document).on('change', '.operation-select')    │  │
│  │ - Extract kode                                   │  │
│  │ - Fetch from API                                │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                     │
│                   ▼ Ajax POST                           │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ API: /api/get-operation-price                    │  │
│  │ Returns: { price, type, nama_tindakan, ... }    │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                     │
│                   ▼                                     │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ HTML: Surgeon Field                              │  │
│  │ <input id="surgeon" value="Rp 4.934.000">       │  │
│  │                                                   │  │
│  │ HTML: Total Field                                │  │
│  │ <input id="total" value="Rp 4.934.000">         │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└────────────────────────────────────────────────────────┘
                    │
                    │ network boundary
                    ▼
┌────────────────────────────────────────────────────────┐
│                    BACKEND (Server)                     │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Flask Route: /api/get-operation-price            │  │
│  │ - Parse JSON                                     │  │
│  │ - Validate input                                │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                     │
│                   ▼                                     │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Database Helper: get_operation_by_code()         │  │
│  │ - Query database                                │  │
│  │ - Return operation data                         │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                     │
│                   ▼                                     │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Database: operation_tables / tindakan_items      │  │
│  │ - Fetch price data                              │  │
│  │ - Return to helper                              │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                     │
│                   ▼                                     │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ JSON Response: { success, type, price, ... }    │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                     │
└────────────────────────────────────────────────────────┘
                    │
                    │ JSON response
                    ▼
              Update DOM & Display
```

---

**Visual Documentation Created: 20 Januari 2026**
