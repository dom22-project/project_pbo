#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backup Database MySQL PBO
Export semua tabel + data ke file SQL
"""

import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import sys

def backup_database():
    """Backup semua tabel dan data"""
    
    host = 'localhost'
    user = 'root'
    password = ''
    database = 'pbo_db'
    
    print("\n" + "="*70)
    print("💾 PBO Database Backup Tool")
    print("="*70)
    
    print(f"\n📡 Connecting to {database}...")
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        print("✅ Connected")
    except Error as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Create backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_pbo_{timestamp}.sql"
    backup_path = os.path.join(os.getcwd(), backup_file)
    
    print(f"\n📝 Backing up to: {backup_file}")
    
    try:
        with open(backup_path, 'w', encoding='utf-8') as f:
            # Header
            f.write("-- PBO Database Backup\n")
            f.write(f"-- Backup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-- Database: pbo_db\n")
            f.write("-- Charset: utf8mb4\n")
            f.write("\n")
            
            # Get all tables
            cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{database}'")
            tables = cursor.fetchall()
            
            print(f"\n📊 Tables found: {len(tables)}")
            
            total_rows = 0
            
            for (table_name,) in tables:
                print(f"\n   📋 Backing up: {table_name}")
                
                # Get CREATE TABLE statement
                cursor.execute(f"SHOW CREATE TABLE {table_name}")
                create_table = cursor.fetchone()[1]
                
                f.write(f"\n-- Table: {table_name}\n")
                f.write(f"DROP TABLE IF EXISTS {table_name};\n")
                f.write(f"{create_table};\n\n")
                
                # Get data
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                if rows:
                    # Get column names
                    cursor.execute(f"DESCRIBE {table_name}")
                    columns = [col[0] for col in cursor.fetchall()]
                    
                    row_count = len(rows)
                    total_rows += row_count
                    print(f"      ✅ {row_count} records")
                    
                    # Write INSERT statements
                    f.write(f"-- Inserting {row_count} records into {table_name}\n")
                    for row in rows:
                        # Prepare values
                        values = []
                        for val in row:
                            if val is None:
                                values.append("NULL")
                            elif isinstance(val, str):
                                # Escape single quotes
                                escaped_val = val.replace("'", "''")
                                values.append(f"'{escaped_val}'")
                            elif isinstance(val, (int, float)):
                                values.append(str(val))
                            else:
                                # For datetime, etc
                                values.append(f"'{str(val)}'")
                        
                        columns_str = ", ".join(columns)
                        values_str = ", ".join(values)
                        f.write(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});\n")
                    
                    f.write("\n")
                else:
                    print(f"      ℹ️  No records")
            
            # Footer
            f.write("\n-- Backup completed\n")
            f.write(f"-- Total records: {total_rows}\n")
        
        cursor.close()
        conn.close()
        
        file_size = os.path.getsize(backup_path)
        file_size_kb = file_size / 1024
        
        print(f"\n✅ Backup completed!")
        print(f"   File: {backup_file}")
        print(f"   Size: {file_size_kb:.2f} KB")
        print(f"   Total records: {total_rows}")
        
        return True
        
    except Error as e:
        print(f"❌ Backup failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("\n🚀 PBO Database Backup\n")
    if backup_database():
        print("\n" + "="*70)
        print("✅ SUCCESS!")
        print("="*70)
        print("\nFile backup sudah siap untuk di-restore atau dipindahkan.")
        print("="*70 + "\n")
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("❌ BACKUP FAILED")
        print("="*70 + "\n")
        sys.exit(1)
