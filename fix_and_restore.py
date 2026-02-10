#!/usr/bin/env python3
"""
Fix auto_increment and restore
"""

import csv
import mysql.connector
from datetime import datetime

def fix_and_restore():
    """Fix AUTO_INCREMENT and restore data"""
    
    csv_file = 'data/operation_tables_export_20260210_161040.csv'
    
    print("[RESTORE] === Fix AUTO_INCREMENT & Restore ===")
    print(f"[RESTORE] Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Connect to MySQL directly
        print("[RESTORE] Step 1: Connecting to MySQL...")
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='pbo_db'
        )
        cursor = conn.cursor()
        print("[RESTORE] ✓ Connected\n")
        
        # Truncate and fix auto_increment
        print("[RESTORE] Step 2: Truncating and fixing AUTO_INCREMENT...")
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute("DELETE FROM operation_tables")  # Delete instead of truncate
        cursor.execute("ALTER TABLE operation_tables AUTO_INCREMENT = 1")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        conn.commit()
        print("[RESTORE] ✓ Table cleaned and AUTO_INCREMENT reset to 1\n")
        
        # Verify auto_increment
        cursor.execute("SHOW TABLE STATUS WHERE Name='operation_tables'")
        table_status = cursor.fetchone()
        print(f"[RESTORE] AUTO_INCREMENT value now: {table_status[10]}\n")
        
        # Read and deduplicate CSV
        print("[RESTORE] Step 3: Reading CSV...")
        operations = {}
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                kode = str(row.get('kode', '')).strip()
                if kode and kode not in operations:
                    operations[kode] = row
        
        print(f"[RESTORE] ✓ Found {len(operations)} unique operations\n")
        
        # Show preview
        print("[RESTORE] Step 4: Preview (First 5 rows)")
        for idx, (kode, op) in enumerate(list(operations.items())[:5], 1):
            print(f"  {idx}. {kode}: {op.get('nama_tindakan')[:40]}")
        print()
        
        # Insert data
        print("[RESTORE] Step 5: Inserting data...")
        insert_sql = """
        INSERT INTO operation_tables (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        inserted = 0
        skipped = 0
        
        for idx, (kode, op) in enumerate(operations.items(), 1):
            try:
                # Parse prices
                try:
                    dokter = float(str(op.get('biaya_dokter', 0) or 0).replace(',', '.'))
                except (ValueError, TypeError):
                    dokter = 0
                
                try:
                    rs = float(str(op.get('biaya_rs', 0) or 0).replace(',', '.'))
                except (ValueError, TypeError):
                    rs = 0
                
                total = dokter + rs
                
                cursor.execute(insert_sql, (
                    kode,
                    str(op.get('nama_tindakan', '')).strip(),
                    str(op.get('kelas', '')).strip(),
                    dokter,
                    rs,
                    total
                ))
                inserted += 1
                
                if idx % 1000 == 0:
                    conn.commit()
                    print(f"  Inserted {idx}... ({inserted} success, {skipped} skipped)")
                    
            except mysql.connector.Error as e:
                skipped += 1
                if skipped <= 5:
                    print(f"  ERROR at kode '{kode}': {str(e)[:60]}")
                continue
        
        # Final commit
        conn.commit()
        print(f"  Final commit done\n")
        
        # Verify
        print("[RESTORE] Step 6: Verification...")
        cursor.execute("SELECT COUNT(*) FROM operation_tables")
        count = cursor.fetchone()[0]
        print(f"  Total operations in DB: {count}")
        
        cursor.execute("SELECT kode, nama_tindakan, kelas, total_biaya FROM operation_tables ORDER BY id LIMIT 3")
        print(f"\n  Sample operations:")
        for row in cursor.fetchall():
            print(f"    - {row[0]}: {row[1][:40]}, {row[2]}, Total: {row[3]}")
        
        print(f"\n{'='*60}")
        print(f"[RESTORE] === RESTORE COMPLETE ===")
        print(f"[RESTORE] Total imported: {inserted}")
        print(f"[RESTORE] Total skipped: {skipped}")
        print(f"[RESTORE] Final count: {count}")
        print(f"[RESTORE] Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        cursor.close()
        conn.close()
        
        return count > 0
        
    except Exception as e:
        print(f"[RESTORE] ✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("[RESTORE] Fix AUTO_INCREMENT & Restore Tool\n")
    success = fix_and_restore()
    exit(0 if success else 1)
