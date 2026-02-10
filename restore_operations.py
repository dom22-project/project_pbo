#!/usr/bin/env python3
"""
Restore operation_tables from exported CSV file
"""

import csv
from datetime import datetime
from app import app, db_helper
from models_sqlalchemy import db

def restore_operations_from_csv():
    """Restore operation_tables from CSV export"""
    
    csv_file = 'data/operation_tables_export_20260210_161040.csv'
    
    print(f"[RESTORE] Starting restore from {csv_file}")
    print(f"[RESTORE] Restore started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Read CSV file (using semicolon delimiter)
        rows_data = []
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')  # Use semicolon as delimiter
            rows_data = list(reader)
        
        print(f"[RESTORE] Found {len(rows_data)} rows in CSV file")
        
        if len(rows_data) == 0:
            print("[RESTORE] No data to restore")
            return False
        
        # Show preview
        print(f"\n[RESTORE] === PREVIEW (First 5 rows) ===")
        for idx, row in enumerate(rows_data[:5], 1):
            print(f"[RESTORE] Row {idx}: kode={row.get('kode')}, nama={row.get('nama_tindakan')}, kelas={row.get('kelas')}")
        print(f"[RESTORE] === END PREVIEW ===\n")
        
        # Import each row
        imported = 0
        skipped = 0
        
        for row_idx, row in enumerate(rows_data, 1):
            try:
                # Build operation data - use UUID for kode to ensure uniqueness
                import uuid
                base_kode = str(row.get('kode', '')).strip()
                unique_suffix = str(uuid.uuid4())[:8].upper()
                
                op_data = {
                    'kode': f"{base_kode}_{unique_suffix}",  # Add UUID suffix for uniqueness
                    'nama_tindakan': str(row.get('nama_tindakan', '')).strip(),
                    'kelas': str(row.get('kelas', '')).strip(),
                    'biaya_dokter': float(row.get('biaya_dokter', 0)),
                    'biaya_rs': float(row.get('biaya_rs', 0))
                }
                
                # Validate required fields
                if not op_data['kode'] or not op_data['nama_tindakan'] or not op_data['kelas']:
                    print(f"[RESTORE] Row {row_idx}: SKIPPED - missing required fields")
                    skipped += 1
                    continue
                
                # Try to add operation
                db_helper.add_operation(**op_data)
                db.session.commit()
                imported += 1
                
                if row_idx % 100 == 0:
                    print(f"[RESTORE] Processed {row_idx} rows... ({imported} imported, {skipped} skipped)")
                
            except Exception as e:
                db.session.rollback()
                if row_idx <= 10:
                    print(f"[RESTORE] Row {row_idx}: ERROR - {str(e)[:80]}")
                skipped += 1
                continue
        
        # Summary
        print(f"\n{'='*80}")
        print(f"[RESTORE] RESTORE COMPLETE")
        print(f"{'='*80}")
        print(f"  Total rows processed: {len(rows_data)}")
        print(f"  Successfully imported: {imported}")
        print(f"  Skipped/Failed: {skipped}")
        print(f"  Restore completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        # Verify
        all_ops = db_helper.get_all_operations()
        print(f"[RESTORE] Verification: Total operations in DB now: {len(all_ops)}")
        
        return imported > 0
        
    except Exception as e:
        print(f"[RESTORE FATAL ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("[RESTORE] PBO Operation Tables Restore Tool")
    print(f"[RESTORE] Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    with app.app_context():
        success = restore_operations_from_csv()
        exit(0 if success else 1)
