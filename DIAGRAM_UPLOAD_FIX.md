# Diagram: Upload Dokter Fix

## BEFORE (Masalah)
```
┌─────────────────────────────────────────────────────────┐
│ User Upload File Excel                                  │
│ Sheet: "DB NAMA DOKTER" (UPPERCASE)                    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │ Validation Check    │
        │ 'db nama dokter'    │
        │ in sheetnames? ❌   │  ← Case-sensitive check FAILS
        └────────┬────────────┘
                 │
                 ▼ (TIDAK KETEMU)
        ┌──────────────────────────────────────┐
        │ Doctor Import Section SKIPPED         │
        │ (Silent - tidak kasih tahu user)      │
        └──────────┬───────────────────────────┘
                   │
                   ▼
        ⚠️ RESULT: Dokter tidak terupload
           Status: 0 imported, 0 skipped
           User: "Kok gak terupload?"
```

## AFTER (Diperbaiki)
```
┌─────────────────────────────────────────────────────────┐
│ User Upload File Excel                                  │
│ Sheet: "DB NAMA DOKTER" atau "db nama dokter" atau     │
│        "Db Nama Dokter" (case apapun OK)               │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────┐
        │ find_sheet() Function           │
        │ (Case-Insensitive Search) ✅    │
        │ Matches: DB NAMA DOKTER         │
        └────────┬────────────────────────┘
                 │
                 ▼ (KETEMU!)
        ┌──────────────────────────────────────┐
        │ Doctor Import Process                 │
        │ ✓ Dr. Budi Santoso                   │
        │ ✓ Dr. Siti Nurhaliza                 │
        │ ✓ Dr. Andi Prasetyo                  │
        │ [Total: 3 imported]                  │
        └──────────┬───────────────────────────┘
                   │
                   ▼
        ┌────────────────────────────────────┐
        │ Success Page with Statistics       │
        │ ✅ 3 Doctors Imported              │
        │ ✅ 0 Duplicates                    │
        │ ✅ 0 Skipped                       │
        │ ℹ️  No Warnings                     │
        └────────────────────────────────────┘
```

## Error Handling Example

### BEFORE
```
❌ ERROR: Sheet 'db table operasi' tidak ditemukan
(User confused: "Tapi file saya punya sheet kok...")
```

### AFTER
```
❌ ERROR: File Excel tidak memiliki sheet yang diperlukan:
- db table operasi

Sheet yang ditemukan dalam file Anda:
- DB NAMA DOKTER
- SHEET_LAIN
- SHEET_LAGI

(User bisa lihat: "Oh, sheet operasi-nya nama beda, atau mungkin belum di-create")
```

## Code Comparison

### BEFORE
```python
# ❌ Exact case-sensitive match
if 'db nama dokter' in wb.sheetnames:
    ws = wb['db nama dokter']  # KeyError jika case beda!
    # Process...
```

### AFTER
```python
# ✅ Case-insensitive match
def find_sheet(workbook, sheet_name_pattern):
    pattern_lower = sheet_name_pattern.lower()
    for sheet_name in workbook.sheetnames:
        if sheet_name.lower() == pattern_lower:
            return sheet_name
    return None

# Usage
dokter_sheet = find_sheet(wb, 'db nama dokter')
if dokter_sheet:
    ws = wb[dokter_sheet]  # ✅ Works regardless of case
    # Process...
else:
    stats['warnings'].append("Sheet 'db nama dokter' tidak ditemukan")
```

## Import Flow

```
STEP 1: USER UPLOAD FILE
   ↓
STEP 2: VALIDATE SHEETS (case-insensitive) ✅
   ├─ Find "db table operasi" → OK
   ├─ Find "db nama dokter" → OK
   └─ All required sheets found
   ↓
STEP 3: BACKUP DATABASE
   ├─ Save backup
   └─ Show backup path
   ↓
STEP 4: CHECK REPLACE MODE
   ├─ If MERGE: Keep existing data
   └─ If REPLACE: Clear all existing data
   ↓
STEP 5: IMPORT SHEETS
   ├─ Import operasi → [2 imported, 0 skipped]
   ├─ Import dokter → [3 imported, 0 duplicates]
   └─ Import tindakan → [0 imported, 0 skipped]
   ↓
STEP 6: DISPLAY SUCCESS
   ├─ Show statistics ✅
   ├─ Show warnings ⚠️ (if any)
   ├─ Show total in DB 
   └─ Show backup location
```

## Key Points

✅ **Case-Insensitive Matching**
- Sheet names bisa dalam case apapun
- "db nama dokter", "DB NAMA DOKTER", "Db Nama Dokter" semua OK

✅ **Detailed Error Messages**
- User tahu sheet mana yang missing
- User bisa lihat sheet apa saja yang ada

✅ **Warnings Tracking**
- Semua issues ditampilkan
- User bisa debug dengan jelas

✅ **Better Logging**
- Setiap dokter yang diimport di-log
- Easy untuk troubleshooting

✅ **Column Flexibility**
- Bisa read dari column B atau A
- Handles different Excel templates
