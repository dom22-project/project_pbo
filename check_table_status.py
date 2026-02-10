#!/usr/bin/env python3
"""
Check operation_tables status and fix auto_increment
"""

from app import app
from models_sqlalchemy import db

def check_and_fix_table():
    """Check and fix operation_tables"""
    
    print("[CHECK] Checking operation_tables status...\n")
    
    try:
        # Check current data
        print("[CHECK] Step 1: Checking current data in table")
        result = db.session.execute(db.text("SELECT COUNT(*) as cnt FROM operation_tables"))
        count = result.fetchone()[0]
        print(f"  Total rows: {count}")
        
        # Check for id=0 rows
        result = db.session.execute(db.text("SELECT id, kode FROM operation_tables WHERE id = 0 OR id < 0 LIMIT 5"))
        bad_rows = list(result)
        if bad_rows:
            print(f"  WARNING: Found {len(bad_rows)} rows with invalid id:")
            for row in bad_rows:
                print(f"    - id={row[0]}, kode={row[1]}")
        else:
            print(f"  ✓ No invalid IDs found")
        
        # Check auto_increment status
        print("\n[CHECK] Step 2: Checking AUTO_INCREMENT status")
        result = db.session.execute(db.text("""
            SELECT AUTO_INCREMENT FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'operation_tables'
        """))
        auto_inc = result.fetchone()[0]
        print(f"  Current AUTO_INCREMENT: {auto_inc}")
        
        # Check max id
        result = db.session.execute(db.text("SELECT MAX(id) FROM operation_tables"))
        max_id = result.fetchone()[0]
        print(f"  Max ID in table: {max_id}")
        
        # If table is empty, truncate and reset
        if count == 0:
            print("\n[CHECK] Step 3: Table is empty - truncating and resetting AUTO_INCREMENT")
            db.session.execute(db.text("TRUNCATE TABLE operation_tables"))
            db.session.commit()
            print(f"  ✓ Table truncated and AUTO_INCREMENT reset to 1")
        
        print()
        return True
        
    except Exception as e:
        print(f"[CHECK] ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("[CHECK] Operation Tables Status Check\n")
    
    with app.app_context():
        check_and_fix_table()
