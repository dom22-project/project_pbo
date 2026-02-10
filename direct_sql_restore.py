#!/usr/bin/env python3
"""
Direct SQL restore of operation_tables
"""

import csv
from datetime import datetime
from app import app
from models_sqlalchemy import db

def direct_sql_restore():
    """Restore operation_tables using direct SQL"""
    
    csv_file = 'data/operation_tables_export_20260210_161040.csv'
    
    print(f"[RESTORE] === DIRECT SQL RESTORE ===")
    print(f"[RESTORE] Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Step 1: Truncate table using raw SQL
        print(f"[RESTORE] Step 1: Truncating table...")
        db.session.execute(db.text("TRUNCATE TABLE operation_tables"))
        db.session.commit()
        print(f"[RESTORE] ✓ Table truncated\n")
        
        # Step 2: Read CSV and collect unique operations
        print(f"[RESTORE] Step 2: Reading CSV and deduplicating...")
        operations = {}  # kode -> operation data
        
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                kode = str(row.get('kode', '')).strip()
                if kode and kode not in operations:  # First occurrence wins
                    operations[kode] = row
        
        print(f"[RESTORE] ✓ Found {len(operations)} unique operations\n")
        
        if len(operations) == 0:
            print("[RESTORE] ✗ No valid data")
            return False
        
        # Step 3: Show preview
        print(f"[RESTORE] Step 3: Preview (First 5 operations)")
        for idx, (kode, op) in enumerate(list(operations.items())[:5], 1):
            print(f"  {idx}. kode={kode}, nama={op.get('nama_tindakan')[:40]}")
        print()
        
        # Step 4: Build insert SQL
        print(f"[RESTORE] Step 4: Preparing batch insert...")
        
        insert_sql = """
        INSERT INTO operation_tables (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya)
        VALUES (:kode, :nama, :kelas, :dokter, :rs, :total)
        """
        
        # Prepare data for batch insert
        batch_data = []
        for kode, op in operations.items():
            try:
                # Try to convert to float, handling both comma and dot notation
                dokter_str = str(op.get('biaya_dokter', 0) or 0).replace(',', '.')
                rs_str = str(op.get('biaya_rs', 0) or 0).replace(',', '.')
                
                dokter = float(dokter_str) if dokter_str else 0
                rs = float(rs_str) if rs_str else 0
                
                batch_data.append({
                    'kode': kode,
                    'nama': str(op.get('nama_tindakan', '')).strip(),
                    'kelas': str(op.get('kelas', '')).strip(),
                    'dokter': dokter,
                    'rs': rs,
                    'total': dokter + rs
                })
            except (ValueError, TypeError) as e:
                # Skip rows with bad data
                print(f"[RESTORE] Skipped kode={kode} - invalid price: {str(e)[:50]}")
                continue
        
        print(f"[RESTORE] ✓ Prepared {len(batch_data)} rows for insert\n")
        
        # Step 5: Execute batch insert
        print(f"[RESTORE] Step 5: Executing batch insert...")
        
        try:
            for idx, data in enumerate(batch_data, 1):
                db.session.execute(db.text(insert_sql), data)
                
                if idx % 500 == 0:
                    db.session.commit()
                    print(f"  Inserted {idx}/{len(batch_data)} rows...")
            
            # Final commit
            db.session.commit()
            print(f"  Final commit done\n")
            
        except Exception as e:
            print(f"  ERROR during insert: {str(e)}")
            db.session.rollback()
            return False
        
        # Step 6: Verify
        print(f"[RESTORE] Step 6: Verification...")
        result = db.session.execute(db.text("SELECT COUNT(*) as cnt FROM operation_tables"))
        count = result.fetchone()[0]
        print(f"  Total operations in DB: {count}")
        
        # Show first few
        result = db.session.execute(db.text("SELECT kode, nama_tindakan, kelas, total_biaya FROM operation_tables LIMIT 3"))
        print(f"\n  Sample operations:")
        for row in result:
            print(f"    - kode={row[0]}, nama={row[1][:40]}, kelas={row[2]}, total={row[3]}")
        
        print(f"\n{'='*60}")
        print(f"[RESTORE] === RESTORE COMPLETE ===")
        print(f"[RESTORE] Total restored: {count}")
        print(f"[RESTORE] Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        return count > 0
        
    except Exception as e:
        print(f"[RESTORE] ✗ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return False

if __name__ == '__main__':
    print("[RESTORE] Direct SQL Restore Tool for Operation Tables\n")
    
    with app.app_context():
        success = direct_sql_restore()
        exit(0 if success else 1)
