#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Backup Manager untuk PBO System
Backup + Restore dalam satu script
"""

import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import sys

class BackupManager:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'pbo_db'
    
    def backup(self):
        """Backup database ke file SQL"""
        print("\n" + "="*70)
        print("💾 BACKUP DATABASE")
        print("="*70)
        
        print(f"\n📡 Connecting to {self.database}...")
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = conn.cursor()
            print("✅ Connected")
        except Error as e:
            print(f"❌ Connection failed: {e}")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_pbo_{timestamp}.sql"
        
        print(f"\n📝 Creating backup: {backup_file}")
        
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                # Header
                f.write("-- PBO Database Backup\n")
                f.write(f"-- Backup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-- Database: pbo_db\n")
                f.write("-- Charset: utf8mb4\n")
                f.write("\n")
                
                # Get all tables
                cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.database}'")
                tables = cursor.fetchall()
                
                print(f"\n📊 Tables: {len(tables)}")
                total_rows = 0
                
                for (table_name,) in tables:
                    print(f"   📋 {table_name}...", end=" ")
                    
                    # CREATE TABLE
                    cursor.execute(f"SHOW CREATE TABLE {table_name}")
                    create_table = cursor.fetchone()[1]
                    
                    f.write(f"\n-- Table: {table_name}\n")
                    f.write(f"DROP TABLE IF EXISTS {table_name};\n")
                    f.write(f"{create_table};\n\n")
                    
                    # DATA
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    
                    if rows:
                        cursor.execute(f"DESCRIBE {table_name}")
                        columns = [col[0] for col in cursor.fetchall()]
                        
                        total_rows += len(rows)
                        print(f"✅ ({len(rows)} records)")
                        
                        f.write(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES\n")
                        
                        for idx, row in enumerate(rows):
                            values = []
                            for val in row:
                                if val is None:
                                    values.append("NULL")
                                elif isinstance(val, str):
                                    escaped_val = val.replace("'", "''")
                                    values.append(f"'{escaped_val}'")
                                elif isinstance(val, (int, float)):
                                    values.append(str(val))
                                else:
                                    values.append(f"'{str(val)}'")
                            
                            values_str = f"({', '.join(values)})"
                            if idx == len(rows) - 1:
                                f.write(f"{values_str};\n\n")
                            else:
                                f.write(f"{values_str},\n")
                    else:
                        print(f"✅ (no records)")
                
                f.write("\n-- Backup completed\n")
                f.write(f"-- Total records: {total_rows}\n")
            
            cursor.close()
            conn.close()
            
            file_size = os.path.getsize(backup_file) / 1024
            
            print(f"\n✅ Backup SUCCESS!")
            print(f"   File: {backup_file}")
            print(f"   Size: {file_size:.2f} KB")
            print(f"   Records: {total_rows}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False
    
    def restore(self, backup_file):
        """Restore database dari file SQL"""
        print("\n" + "="*70)
        print("♻️  RESTORE DATABASE")
        print("="*70)
        
        if not os.path.exists(backup_file):
            print(f"\n❌ File not found: {backup_file}")
            return False
        
        print(f"\n📂 File: {backup_file}")
        print(f"   Size: {os.path.getsize(backup_file) / 1024:.2f} KB")
        
        print(f"\n⚠️  Ini akan DROP semua tabel existing!")
        response = input("   Lanjutkan? (yes/no): ").strip().lower()
        if response != 'yes':
            print("   ❌ Cancelled")
            return False
        
        print(f"\n📡 Connecting...")
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = conn.cursor()
            print("✅ Connected")
        except Error as e:
            print(f"❌ Connection failed: {e}")
            return False
        
        try:
            print(f"\n📖 Reading file...")
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            print("✅ File loaded")
            
            # Parse SQL statements
            print(f"⚙️  Parsing statements...")
            statements = []
            current_stmt = ""
            in_string = False
            
            for char in backup_content:
                if char == "'":
                    in_string = not in_string
                
                if char == ';' and not in_string:
                    stmt = current_stmt.strip()
                    if stmt and not stmt.startswith('--'):
                        statements.append(stmt)
                    current_stmt = ""
                    continue
                
                current_stmt += char
            
            print(f"✅ {len(statements)} statements parsed")
            
            # Execute
            print(f"\n🔄 Executing...")
            success = 0
            for i, stmt in enumerate(statements, 1):
                try:
                    cursor.execute(stmt)
                    success += 1
                    if i % 10 == 0:
                        print(f"   ✅ {success}/{len(statements)}")
                except Error as e:
                    print(f"   ⚠️  #{i}: {str(e)[:60]}")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"\n✅ Restore SUCCESS!")
            print(f"   Executed: {success}/{len(statements)}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False

def main():
    """Main menu"""
    manager = BackupManager()
    
    print("\n" + "="*70)
    print("🗄️  PBO Database Backup Manager")
    print("="*70)
    print("\n1. BACKUP - Simpan database ke file")
    print("2. RESTORE - Pulihkan database dari file")
    print("3. EXIT")
    
    choice = input("\nPilih (1/2/3): ").strip()
    
    if choice == '1':
        if manager.backup():
            print("\n✅ Done!\n")
            return 0
        else:
            print("\n❌ Failed!\n")
            return 1
    
    elif choice == '2':
        # List backup files
        backup_files = sorted([f for f in os.listdir('.') 
                             if f.startswith('backup_pbo_') and f.endswith('.sql')], 
                            reverse=True)
        
        if not backup_files:
            print("\n❌ No backup files found!")
            return 1
        
        print("\n📋 Available backups (newest first):")
        for i, f in enumerate(backup_files[:10], 1):
            size = os.path.getsize(f) / 1024
            mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M')
            print(f"   {i}. {f}")
            print(f"      Size: {size:.2f} KB | Modified: {mtime}")
        
        try:
            sel = int(input("\nSelect (number): ")) - 1
            if sel < 0 or sel >= len(backup_files):
                print("❌ Invalid choice")
                return 1
            
            if manager.restore(backup_files[sel]):
                print("\n✅ Done!\n")
                return 0
            else:
                print("\n❌ Failed!\n")
                return 1
        except ValueError:
            print("❌ Invalid input")
            return 1
    
    else:
        print("\n❌ Invalid choice")
        return 1

if __name__ == '__main__':
    exit(main())
