#!/usr/bin/env python3
"""
Migrate operation_tables from db_baru.db to current database
"""

import sqlite3
import sys
from datetime import datetime

# Import app context
from app import app, db_helper
from models_sqlalchemy import db

def migrate_operations():
    """Migrate operation_tables from db_baru.db"""
    
    db_baru_path = 'data/db_baru.db'
    
    print(f"[MIGRATE] Starting migration from {db_baru_path}")
    print(f"[MIGRATE] Migration started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Connect to source database
        source_conn = sqlite3.connect(db_baru_path)
        source_conn.row_factory = sqlite3.Row
        source_cursor = source_conn.cursor()
        
        print(f"[MIGRATE] Connected to source database: {db_baru_path}")
        
        # Query all rows from operation_tables
        source_cursor.execute("SELECT * FROM operation_tables")
        rows = source_cursor.fetchall()
        
        print(f"[MIGRATE] Found {len(rows)} rows in operation_tables")
        
        if len(rows) == 0:
            print("[MIGRATE] No data to migrate")
            return
        
        # Show first 5 rows as preview
        print(f"\n[MIGRATE] === PREVIEW (First 5 rows) ===")
        for idx, row in enumerate(rows[:5], 1):
            print(f"[MIGRATE] Row {idx}: {dict(row)}")
        print(f"[MIGRATE] === END PREVIEW ===\n")
        
        # Import each row
        imported = 0
        skipped = 0
        
        for row_idx, row in enumerate(rows, 1):
            try:
                row_dict = dict(row)
                
                # Build operation data
                op_data = {
                    'kode': str(row_dict.get('kode', '')),
                    'nama_tindakan': str(row_dict.get('nama_tindakan', '')),
                    'kelas': str(row_dict.get('kelas', '')),
                    'biaya_dokter': float(row_dict.get('biaya_dokter', 0)),
                    'biaya_rs': float(row_dict.get('biaya_rs', 0))
                }
                
                # Validate required fields
                if not op_data['kode'] or not op_data['nama_tindakan'] or not op_data['kelas']:
                    print(f"[MIGRATE] Row {row_idx}: SKIPPED - missing required fields")
                    skipped += 1
                    continue
                
                # Try to add operation
                db_helper.add_operation(**op_data)
                db.session.commit()
                imported += 1
                
                if row_idx % 10 == 0:
                    print(f"[MIGRATE] Processed {row_idx} rows... ({imported} imported, {skipped} skipped)")
                
            except Exception as e:
                db.session.rollback()
                print(f"[MIGRATE] Row {row_idx}: ERROR - {str(e)[:100]}")
                skipped += 1
                continue
        
        source_conn.close()
        
        # Summary
        print(f"\n{'='*80}")
        print(f"[MIGRATE] MIGRATION COMPLETE")
        print(f"{'='*80}")
        print(f"  Total rows processed: {len(rows)}")
        print(f"  Successfully imported: {imported}")
        print(f"  Skipped/Failed: {skipped}")
        print(f"  Migration completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        # Verify
        all_ops = db_helper.get_all_operations()
        print(f"[MIGRATE] Verification: Total operations in DB now: {len(all_ops)}")
        
        return True
        
    except Exception as e:
        print(f"[MIGRATE FATAL ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("[MIGRATE] PBO Operation Tables Migration Tool")
    print(f"[MIGRATE] Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    with app.app_context():
        success = migrate_operations()
        sys.exit(0 if success else 1)
