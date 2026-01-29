#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Foreign Key Relationships
Drop and recreate paket_tindakan with proper FK
"""

import mysql.connector
from mysql.connector import Error
import sys

def fix_foreignkeys():
    """Fix FK constraints"""
    host = 'localhost'
    user = 'root'
    password = ''
    
    print("\n" + "="*70)
    print("🔧 Fixing Foreign Key Relationships")
    print("="*70)
    
    print(f"\n📡 Connecting...")
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database='pbo_db'
        )
        print("✅ Connected")
    except Error as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    cursor = conn.cursor()
    
    # SQL Statements
    statements = [
        # Drop existing paket_tindakan table
        "DROP TABLE IF EXISTS paket_tindakan",
        
        # Recreate paket_tindakan with proper FK
        """CREATE TABLE paket_tindakan (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pbo_id INT NOT NULL,
            tindakan_id INT,
            nama_tindakan VARCHAR(255),
            kategory VARCHAR(100),
            harga DECIMAL(15, 2) DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_pbo_id (pbo_id),
            INDEX idx_tindakan_id (tindakan_id),
            CONSTRAINT fk_paket_pbo FOREIGN KEY (pbo_id) REFERENCES pbo_data(id) ON DELETE CASCADE,
            CONSTRAINT fk_paket_tindakan FOREIGN KEY (tindakan_id) REFERENCES tindakan_items(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
    ]
    
    print("\n📄 Executing fixes...")
    
    for stmt in statements:
        try:
            cursor.execute(stmt)
            if 'DROP' in stmt.upper():
                print(f"   ✅ Dropped old paket_tindakan table")
            elif 'CREATE' in stmt.upper():
                print(f"   ✅ Created paket_tindakan with FK constraints")
        except Error as e:
            print(f"   ⚠️  Error: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n✅ Foreign key relationships fixed!")
    return True

if __name__ == '__main__':
    print("\n🚀 Foreign Key Fixer\n")
    if fix_foreignkeys():
        print("\n" + "="*70)
        print("✅ SUCCESS!")
        print("="*70)
        print("\nNow try running the app:")
        print("  python app.py")
        print("="*70 + "\n")
        sys.exit(0)
    else:
        sys.exit(1)
