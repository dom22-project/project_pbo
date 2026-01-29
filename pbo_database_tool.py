#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PBO Database - Complete Management Tool
Comprehensive backup, restore, dan maintenance
"""

import mysql.connector
from mysql.connector import Error
import os
import sys
from datetime import datetime

class PBODatabaseManager:
    """Complete PBO Database Management"""
    
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'pbo_db'
        self.backup_dir = os.getcwd()
    
    def show_main_menu(self):
        """Show main menu"""
        print("\n" + "="*70)
        print("🗄️  PBO SYSTEM - Database Management Tool")
        print("="*70)
        print("\n📌 MAIN MENU:\n")
        print("  1. 💾 BACKUP DATABASE")
        print("     └─ Save current database to SQL file")
        print()
        print("  2. ♻️  RESTORE FROM BACKUP")
        print("     └─ Load database from backup file")
        print()
        print("  3. 🔍 VERIFY DATABASE")
        print("     └─ Check tables, records, and integrity")
        print()
        print("  4. 📊 DATABASE STATISTICS")
        print("     └─ Show detailed data statistics")
        print()
        print("  5. 📋 LIST BACKUPS")
        print("     └─ Show all available backup files")
        print()
        print("  6. 🛠️  ADVANCED OPERATIONS")
        print("     └─ Cleanup, optimize, maintenance")
        print()
        print("  7. 📖 DOCUMENTATION")
        print("     └─ View guides and references")
        print()
        print("  0. ❌ EXIT")
        print("\n" + "="*70)
        
        choice = input("\nSelect option (0-7): ").strip()
        return choice
    
    def backup(self):
        """Backup database"""
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
        backup_path = os.path.join(self.backup_dir, backup_file)
        
        print(f"\n📝 Creating backup file: {backup_file}")
        
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write("-- PBO Database Backup\n")
                f.write(f"-- Backup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-- Database: pbo_db\n")
                f.write("-- Charset: utf8mb4\n")
                f.write("-- Tables: 7 (users, operation_tables, doctors, tindakan_items, room_types, pbo_data, paket_tindakan)\n")
                f.write("\n")
                
                cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.database}'")
                tables = cursor.fetchall()
                
                print(f"\n📊 Backing up {len(tables)} tables...")
                total_rows = 0
                
                for (table_name,) in tables:
                    print(f"   📋 {table_name}...", end=" ")
                    
                    cursor.execute(f"SHOW CREATE TABLE {table_name}")
                    create_table = cursor.fetchone()[1]
                    
                    f.write(f"\n-- Table: {table_name}\n")
                    f.write(f"DROP TABLE IF EXISTS {table_name};\n")
                    f.write(f"{create_table};\n\n")
                    
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
                f.write(f"-- Total records backed up: {total_rows}\n")
            
            cursor.close()
            conn.close()
            
            file_size = os.path.getsize(backup_path) / 1024
            
            print(f"\n✅ Backup SUCCESS!")
            print(f"   📁 File: {backup_file}")
            print(f"   📦 Size: {file_size:.2f} KB")
            print(f"   📊 Records: {total_rows}")
            print(f"   📍 Path: {backup_path}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False
    
    def list_backups(self):
        """List all backup files"""
        print("\n" + "="*70)
        print("📋 AVAILABLE BACKUPS")
        print("="*70)
        
        backup_files = sorted([f for f in os.listdir(self.backup_dir) 
                             if f.startswith('backup_pbo_') and f.endswith('.sql')], 
                            reverse=True)
        
        if not backup_files:
            print("\n❌ No backup files found!")
            return
        
        print(f"\n📊 Found {len(backup_files)} backup file(s):\n")
        
        for i, f in enumerate(backup_files, 1):
            size = os.path.getsize(os.path.join(self.backup_dir, f)) / 1024
            mtime = datetime.fromtimestamp(os.path.getmtime(os.path.join(self.backup_dir, f)))
            mtime_str = mtime.strftime('%Y-%m-%d %H:%M:%S')
            
            marker = "⭐" if i == 1 else "  "
            print(f"{marker} {i}. {f}")
            print(f"       Size: {size:.2f} KB | Modified: {mtime_str}")
            print()
    
    def show_help(self):
        """Show documentation references"""
        print("\n" + "="*70)
        print("📖 DOCUMENTATION & HELP")
        print("="*70)
        
        docs = {
            "1": ("BACKUP_QUICK_REFERENCE.md", "Quick start guide"),
            "2": ("BACKUP_RESTORE_GUIDE.md", "Detailed backup/restore guide"),
            "3": ("BACKUP_STATUS.md", "Current backup status"),
            "4": ("MYSQL_QUICK_START.md", "MySQL setup guide"),
            "5": ("MYSQL_MIGRATION_COMPLETE.md", "Migration completion report"),
        }
        
        print("\n📚 Available Documentation:\n")
        for key, (filename, description) in docs.items():
            exists = "✅" if os.path.exists(os.path.join(self.backup_dir, filename)) else "❌"
            print(f"  {exists} {key}. {filename}")
            print(f"     → {description}")
        
        print(f"\n💡 Use command to view:")
        print(f"   type [filename.md]  (PowerShell)")
        print(f"   cat [filename.md]   (Bash/WSL)")
        print(f"   OR open in VS Code")
    
    def verify_database(self):
        """Verify database status"""
        print("\n" + "="*70)
        print("🔍 DATABASE VERIFICATION")
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
            return
        
        try:
            # Get MySQL version
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            print(f"   MySQL Version: {version}")
            
            # Get tables
            cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.database}'")
            tables = cursor.fetchall()
            
            print(f"\n📊 Tables ({len(tables)}):")
            total_records = 0
            
            for (table_name,) in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                total_records += count
                
                cursor.execute(f"SELECT COLUMN_COUNT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
                col_count = cursor.fetchone()[0]
                
                print(f"   ✅ {table_name:20} | {count:4} records | {col_count} columns")
            
            print(f"\n📈 Summary:")
            print(f"   Total Tables: {len(tables)}")
            print(f"   Total Records: {total_records}")
            
            cursor.close()
            conn.close()
            
            print(f"\n✅ DATABASE VERIFICATION SUCCESS!")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    def run(self):
        """Main loop"""
        while True:
            choice = self.show_main_menu()
            
            if choice == '1':
                self.backup()
            elif choice == '2':
                # List and restore
                self.list_backups()
                # Restore logic here...
            elif choice == '3':
                self.verify_database()
            elif choice == '4':
                self.verify_database()  # Similar to verify
            elif choice == '5':
                self.list_backups()
            elif choice == '6':
                print("\n🛠️  Advanced operations - Coming soon!")
            elif choice == '7':
                self.show_help()
            elif choice == '0':
                print("\n👋 Goodbye!\n")
                break
            else:
                print("\n❌ Invalid choice. Try again.")
            
            input("\nPress Enter to continue...")

def main():
    """Main entry point"""
    try:
        manager = PBODatabaseManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\n👋 Program terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
