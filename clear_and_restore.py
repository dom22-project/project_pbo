#!/usr/bin/env python3
"""
Clear operation_tables and restore from CSV
"""

import csv
from datetime import datetime
from app import app
from models_sqlalchemy import db, OperationTable

def clear_and_restore_operations():
    """Clear and restore operation_tables from CSV export"""
    
    csv_file = 'data/operation_tables_export_20260210_161040.csv'
    
    print(f"[RESTORE] === CLEAR & RESTORE operation_tables ===")
    print(f"[RESTORE] Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Step 1: Clear existing data
        print(f"[RESTORE] Step 1: Clearing existing data...")
        db.session.query(OperationTable).delete()
        db.session.commit()
        print(f"[RESTORE] ✓ Table cleared\n")
        
        # Step 2: Read CSV file
        print(f"[RESTORE] Step 2: Reading CSV file...")
        rows_data = []
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                # Only process rows with non-empty kode (skip empty rows)
                if row.get('kode', '').strip():
                    rows_data.append(row)
        
        print(f"[RESTORE] ✓ Found {len(rows_data)} valid rows in CSV\n")
        
        if len(rows_data) == 0:
            print("[RESTORE] ✗ No valid data to restore")
            return False
        
        # Step 3: Show preview
        print(f"[RESTORE] Step 3: Data preview (First 5 rows)")
        for idx, row in enumerate(rows_data[:5], 1):
            print(f"  Row {idx}: kode={row.get('kode')}, nama={row.get('nama_tindakan')[:40]}, kelas={row.get('kelas')}")
        print()
        
        # Step 4: Import data (with deduplication by kode)
        print(f"[RESTORE] Step 4: Importing data (deduplicating by kode)...")
        imported = 0
        failed = 0
        seen_kodes = set()
        
        for row_idx, row in enumerate(rows_data, 1):
            try:
                kode = str(row.get('kode', '')).strip()
                
                # Skip if we've already seen this kode
                if kode in seen_kodes:
                    continue
                
                seen_kodes.add(kode)
                
                # Build operation
                op = OperationTable(
                    kode=kode,
                    nama_tindakan=str(row.get('nama_tindakan', '')).strip(),
                    kelas=str(row.get('kelas', '')).strip(),
                    biaya_dokter=float(row.get('biaya_dokter', 0) or 0),
                    biaya_rs=float(row.get('biaya_rs', 0) or 0)
                )
                
                # Calculate total biaya
                op.total_biaya = op.biaya_dokter + op.biaya_rs
                
                # Add to session
                db.session.add(op)
                imported += 1
                
                # Batch commit every 100 rows
                if imported % 100 == 0:
                    try:
                        db.session.commit()
                        print(f"  Imported {imported} unique operations...")
                    except Exception as e:
                        print(f"  ERROR at batch commit: {str(e)[:60]}")
                        db.session.rollback()
                        
            except Exception as e:
                db.session.rollback()
                failed += 1
                if failed <= 5:
                    print(f"  Row {row_idx}: {str(e)[:60]}")
                continue
        
        # Final commit
        try:
            db.session.commit()
            print(f"  Final commit done\n")
        except Exception as e:
            print(f"  ERROR on final commit: {str(e)}")
            db.session.rollback()
            return False
        
        # Step 5: Summary
        print(f"{'='*60}")
        print(f"[RESTORE] === RESTORE SUMMARY ===")
        print(f"{'='*60}")
        print(f"  Total rows processed: {len(rows_data)}")
        print(f"  Successfully imported: {imported}")
        print(f"  Failed/Skipped: {failed}")
        print(f"  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Step 6: Verify
        print(f"[RESTORE] Step 5: Verification...")
        all_ops = db.session.query(OperationTable).all()
        print(f"  Total operations in DB: {len(all_ops)}")
        
        if len(all_ops) > 0:
            print(f"\n  Sample operations:")
            for op in all_ops[:3]:
                print(f"    - kode={op.kode}, nama={op.nama_tindakan[:40]}, kelas={op.kelas}, total={op.total_biaya}")
        
        print()
        return imported > 0
        
    except Exception as e:
        print(f"[RESTORE] ✗ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("[RESTORE] PBO Operation Tables - Clear & Restore Tool\n")
    
    with app.app_context():
        success = clear_and_restore_operations()
        exit(0 if success else 1)
