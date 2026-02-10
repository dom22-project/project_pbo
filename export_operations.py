#!/usr/bin/env python3
"""
Export operation_tables from db_baru.db to CSV file
"""

import sqlite3
import csv
from datetime import datetime
import os

def export_operations_to_csv():
    """Export operation_tables from db_baru.db to CSV"""
    
    db_baru_path = 'data/db_baru.db'
    output_file = f'data/operation_tables_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    print(f"[EXPORT] Starting export from {db_baru_path}")
    print(f"[EXPORT] Output file: {output_file}\n")
    
    try:
        # Connect to source database
        conn = sqlite3.connect(db_baru_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query all rows from operation_tables
        cursor.execute("SELECT * FROM operation_tables")
        rows = cursor.fetchall()
        
        print(f"[EXPORT] Found {len(rows)} rows in operation_tables\n")
        
        if len(rows) == 0:
            print("[EXPORT] No data to export")
            conn.close()
            return False
        
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        print(f"[EXPORT] Columns: {column_names}\n")
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_names)
            writer.writeheader()
            
            for row_idx, row in enumerate(rows, 1):
                row_dict = dict(row)
                writer.writerow(row_dict)
                
                if row_idx % 50 == 0:
                    print(f"[EXPORT] Exported {row_idx} rows...")
        
        conn.close()
        
        # Get file size
        file_size = os.path.getsize(output_file)
        file_size_kb = file_size / 1024
        
        print(f"\n{'='*80}")
        print(f"[EXPORT] SUCCESS")
        print(f"{'='*80}")
        print(f"  Total rows exported: {len(rows)}")
        print(f"  Output file: {output_file}")
        print(f"  File size: {file_size_kb:.2f} KB ({file_size} bytes)")
        print(f"  Export completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        # Show preview
        print(f"[EXPORT] === PREVIEW (First 5 rows) ===")
        for idx in range(min(5, len(rows))):
            row_dict = dict(rows[idx])
            print(f"[EXPORT] Row {idx+1}: {row_dict}")
        print(f"[EXPORT] === END PREVIEW ===\n")
        
        print(f"[EXPORT] File ready for download at: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"[EXPORT ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("[EXPORT] PBO Operation Tables Export Tool")
    print(f"[EXPORT] Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    success = export_operations_to_csv()
    exit(0 if success else 1)
