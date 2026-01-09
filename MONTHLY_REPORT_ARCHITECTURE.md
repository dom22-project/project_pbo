# 📊 MONTHLY REPORT - FLOWCHART & ARCHITECTURE

## SISTEM FLOWCHART

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER ACCESS                                │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
            │ Navbar Menu  │ │  Dashboard   │ │  Direct URL  │
            │  "Laporan    │ │ "Laporan     │ │ /monthly-    │
            │   Bulanan"   │ │  Bulanan"    │ │  report      │
            └──────────────┘ └──────────────┘ └──────────────┘
                    │             │             │
                    └─────────────┼─────────────┘
                                  ▼
                    ┌─────────────────────────────┐
                    │  /monthly-report endpoint   │
                    │  (Flask route handler)      │
                    └─────────────────────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                ▼                 ▼                 ▼
        ┌───────────────┐ ┌──────────────┐ ┌──────────────┐
        │ Get Available │ │  Get Monthly │ │ Calculate    │
        │   Months      │ │   Report     │ │ Statistics   │
        │               │ │   Data       │ │              │
        │(Database)     │ │(Database)    │ │              │
        └───────────────┘ └──────────────┘ └──────────────┘
                │             │                  │
                └─────────────┼──────────────────┘
                              ▼
                    ┌─────────────────────────┐
                    │  Render HTML Template   │
                    │ (monthly_report.html)   │
                    └─────────────────────────┘
                              │
                ┌─────────────┬─────────────┐
                ▼             ▼             ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │  Statistics  │ │ Month Picker │ │  Data Table  │
        │   Cards      │ │              │ │              │
        └──────────────┘ └──────────────┘ └──────────────┘
                │             │             │
                └─────────────┴─────────────┘
                              ▼
                    ┌─────────────────────────┐
                    │   Display to Browser    │
                    │   (Rendered HTML)       │
                    └─────────────────────────┘
                              │
                ┌─────────────┬─────────────┬──────────────┐
                ▼             ▼             ▼              ▼
            ┌────────┐  ┌────────┐  ┌─────────┐  ┌──────────────┐
            │ View   │  │ Export │  │ Export  │  │ Print/PDF    │
            │ Detail │  │ CSV    │  │ Custom  │  │              │
            │        │  │        │  │ Filter  │  │              │
            └────────┘  └────────┘  └─────────┘  └──────────────┘
```

## DATABASE QUERY FLOW

```
┌─────────────────────────────────────────────────────────────┐
│               get_available_months()                        │
├─────────────────────────────────────────────────────────────┤
│ SELECT YEAR(tanggal), MONTH(tanggal), COUNT(DISTINCT id)   │
│ FROM database                                              │
│ WHERE tanggal IS NOT NULL AND is_latest = 1               │
│ GROUP BY YEAR, MONTH                                       │
│ ORDER BY YEAR DESC, MONTH DESC                             │
├─────────────────────────────────────────────────────────────┤
│ ✓ Result: List of (year, month, count) tuples             │
│ ✓ Used for: Populate dropdown selector                     │
│ ✓ Contoh: [(2026, 1, 15), (2025, 12, 23), ...]            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│            get_monthly_report(year, month)                 │
├─────────────────────────────────────────────────────────────┤
│ SELECT id, tanggal, nama_operasi, nama_dokter,             │
│        perusahaan_asuransi, nama_pasien, kelas, total      │
│ FROM database                                              │
│ WHERE YEAR(tanggal) = @year                               │
│   AND MONTH(tanggal) = @month                             │
│   AND is_latest = 1                                        │
│ ORDER BY tanggal DESC                                      │
├─────────────────────────────────────────────────────────────┤
│ ✓ Result: List of dicts dengan info operasi               │
│ ✓ Used for: Display di table, calculate stats              │
│ ✓ Example: {id: 1, tanggal: Date, nama_operasi: '...'}   │
└─────────────────────────────────────────────────────────────┘
```

## COMPONENT ARCHITECTURE

```
┌──────────────────────────────────────────────────────────────┐
│                  MONTHLY REPORT SYSTEM                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          PRESENTATION LAYER (Frontend)                │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ • monthly_report.html (Template)                      │ │
│  │ • Bootstrap 5 styling                                  │ │
│  │ • Chart JS (untuk visualisasi)                         │ │
│  │ • Export JS (CSV/PDF handling)                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                         │                                    │
│                         ▼                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         APPLICATION LAYER (Backend)                   │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ • app.py (Flask route handler)                         │ │
│  │   - @app.route('/monthly-report')                      │ │
│  │   - Request handling                                   │ │
│  │   - Template rendering                                │ │
│  └────────────────────────────────────────────────────────┘ │
│                         │                                    │
│                         ▼                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         BUSINESS LOGIC LAYER (Models)                 │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ • models.py (Database operations)                      │ │
│  │   - get_available_months()                             │ │
│  │   - get_monthly_report(year, month)                    │ │
│  │   - Data processing & formatting                       │ │
│  └────────────────────────────────────────────────────────┘ │
│                         │                                    │
│                         ▼                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         DATA LAYER (Database)                         │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ • SQLAlchemy ORM                                       │ │
│  │ • models_sqlalchemy.py (PBOData model)                 │ │
│  │ • SQL queries dengan filter                            │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## DATA PROCESSING FLOW

```
REQUEST: /monthly-report?year=2026&month=1
   │
   ▼
EXTRACT PARAMETERS
   │
   ├─ selected_year = 2026
   ├─ selected_month = 1
   │
   ▼
CALL DATABASE FUNCTIONS
   │
   ├─ available_months = db_helper.get_available_months()
   │  └─ Returns: [(2026, 1, 15), (2025, 12, 23), ...]
   │
   ├─ report_data = db_helper.get_monthly_report(2026, 1)
   │  └─ Returns: [{id: 1, tanggal: ..., nama_operasi: ..., ...}, ...]
   │
   ▼
CALCULATE STATISTICS
   │
   ├─ total_operations = len(report_data)
   │  └─ Count: 15 operasi
   │
   ├─ total_revenue = sum([item['total'] for item in report_data])
   │  └─ Sum: Rp 2.500.000
   │
   ├─ unique_doctors = len(set([item['nama_dokter'] for item in report_data]))
   │  └─ Count: 8 dokter unik
   │
   ├─ unique_insurances = len(set([item['perusahaan_asuransi'] for ...]))
   │  └─ Count: 5 asuransi unik
   │
   ▼
PREPARE TEMPLATE CONTEXT
   │
   ├─ report_data
   ├─ available_months
   ├─ selected_year
   ├─ selected_month
   ├─ month_name ("Januari")
   ├─ total_operations
   ├─ total_revenue
   ├─ unique_doctors
   └─ unique_insurances
   │
   ▼
RENDER TEMPLATE
   │
   └─ render_template('monthly_report.html', context)
   │
   ▼
HTML RESPONSE TO BROWSER
```

## FILE STRUCTURE

```
app_pbo/
├── models.py
│   ├── Database class
│   ├── ├─ get_monthly_report()    [NEW]
│   ├─ └─ get_available_months()   [NEW]
│   └── Existing functions
│
├── app.py
│   ├── @app.route('/monthly-report')  [NEW]
│   └── monthly_report() function      [NEW]
│
├── templates/
│   ├── base.html
│   │   └─ Updated: +1 nav item    [MODIFIED]
│   │
│   ├── index.html
│   │   └─ Updated: +1 quick action button  [MODIFIED]
│   │
│   └── monthly_report.html               [NEW]
│       ├── Header section
│       ├── Statistics cards
│       ├── Month selector
│       ├── Data table
│       ├── Export buttons
│       └── JavaScript handlers
│
├── Documentation/
│   ├── MONTHLY_REPORT_GUIDE.md              [NEW]
│   ├── MONTHLY_REPORT_QUICKSTART.md         [NEW]
│   ├── MONTHLY_REPORT_IMPLEMENTATION.md     [NEW]
│   └── MONTHLY_REPORT_SUMMARY.txt           [NEW]
│
└── Testing/
    └── test_monthly_report.py               [NEW]
```

## INTERACTION DIAGRAM

```
┌──────────────┐
│ User/Browser │
└──────────────┘
       │
       │ GET /monthly-report?year=2026&month=1
       ▼
┌──────────────────────────┐
│    Flask App (app.py)    │
│  monthly_report()        │
└──────────────────────────┘
       │
       ├─→ db_helper.get_available_months()
       │        │
       │        ▼
       │   ┌──────────────────┐
       │   │  Database Query  │
       │   │  (SQLAlchemy)    │
       │   └──────────────────┘
       │        │
       │        └─→ Returns: Months list
       │
       ├─→ db_helper.get_monthly_report(2026, 1)
       │        │
       │        ▼
       │   ┌──────────────────┐
       │   │  Database Query  │
       │   │  (SQLAlchemy)    │
       │   └──────────────────┘
       │        │
       │        └─→ Returns: Report data
       │
       ├─→ Calculate statistics
       │
       └─→ render_template('monthly_report.html', ...)
              │
              ▼
         ┌──────────────────────────┐
         │    HTML Template         │
         │ (Jinja2 rendering)       │
         └──────────────────────────┘
              │
              ▼
         ┌──────────────────────────┐
         │   HTTP Response (HTML)   │
         └──────────────────────────┘
              │
              ▼
         ┌──────────────┐
         │   Browser    │
         │  (Displayed) │
         └──────────────┘
```

## EXPORT FUNCTIONALITY

```
USER CLICKS EXPORT
       │
       ├─ Export CSV
       │    │
       │    ▼
       │  JavaScript function exportToCSV()
       │    │
       │    ├─ Collect table data
       │    ├─ Convert to CSV format
       │    ├─ Create Blob object
       │    └─ Trigger download
       │         │
       │         ▼
       │    laporan_Januari_2026.csv
       │
       └─ Export PDF (Print)
            │
            ▼
          Ctrl+P atau klik "Cetak"
            │
            ├─ Browser print dialog
            ├─ Select printer: "Save as PDF"
            └─ Save as PDF file
```

## DATABASE MODEL RELATIONSHIP

```
┌─────────────────────────────────────────┐
│           PBOData Table                 │
├─────────────────────────────────────────┤
│ PK: id                                  │
│ ├─ diagnosa                             │
│ ├─ nama_operasi        ← USED           │
│ ├─ sifat_operasi                        │
│ ├─ nama_dokter         ← USED           │
│ ├─ perusahaan_asuransi ← USED           │
│ ├─ tanggal             ← USED (FILTER)  │
│ ├─ kelas                                │
│ ├─ total               ← USED (SUM)     │
│ ├─ is_latest           ← USED (FILTER)  │
│ ├─ created_at                           │
│ ├─ version_number                       │
│ ├─ parent_id                            │
│ └─ ... (other fields)                   │
│                                         │
└─────────────────────────────────────────┘
   │
   │ Query dengan WHERE:
   │ - YEAR(tanggal) = 2026
   │ - MONTH(tanggal) = 1
   │ - is_latest = 1
   │ ORDER BY tanggal DESC
   │
   ▼
Report Data untuk dashboard
```

---

**Diagram ini menggambarkan alur lengkap dari user request hingga data ditampilkan di browser.**

