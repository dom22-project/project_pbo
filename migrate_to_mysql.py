#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Migration Script: SQLite → MySQL
Migrasi data dari database lama (SQLite) ke MySQL baru
"""

import sqlite3
import mysql.connector
from mysql.connector import Error
import os
import sys
from datetime import datetime
from pathlib import Path

class DataMigrator:
    def __init__(self, sqlite_db=None, mysql_config=None):
        self.sqlite_db = sqlite_db
        self.mysql_config = mysql_config or {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'pbo_db'
        }
        self.sqlite_conn = None
        self.mysql_conn = None
        self.stats = {
            'migrated': 0,
            'skipped': 0,
            'errors': 0,
            'tables': {}
        }
    
    def find_sqlite_db(self):
        """Cari database SQLite di folder"""
        possible_names = ['pbo_database.db', 'app.db', 'database.db', 'pbo_db.sqlite']
        
        for name in possible_names:
            path = Path(__file__).parent / name
            if path.exists():
                return str(path)
        
        return None
    
    def connect_sqlite(self):
        """Koneksi ke SQLite"""
        try:
            if not self.sqlite_db:
                self.sqlite_db = self.find_sqlite_db()
            
            if not self.sqlite_db or not os.path.exists(self.sqlite_db):
                print("❌ SQLite database tidak ditemukan")
                return False
            
            self.sqlite_conn = sqlite3.connect(self.sqlite_db)
            print(f"✅ Connected to SQLite: {self.sqlite_db}")
            return True
        except Exception as e:
            print(f"❌ Error connecting SQLite: {e}")
            return False
    
    def connect_mysql(self):
        """Koneksi ke MySQL"""
        try:
            self.mysql_conn = mysql.connector.connect(**self.mysql_config)
            print(f"✅ Connected to MySQL: {self.mysql_config['database']}")
            return True
        except Error as e:
            print(f"❌ Error connecting MySQL: {e}")
            return False
    
    def get_sqlite_tables(self):
        """Get daftar tables dari SQLite"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return tables
        except Exception as e:
            print(f"⚠️  Error getting tables: {e}")
            return []
    
    def migrate_table(self, table_name):
        """Migrate satu table dari SQLite ke MySQL"""
        try:
            # Get data dari SQLite
            sqlite_cursor = self.sqlite_conn.cursor()
            sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in sqlite_cursor.fetchall()]
            
            if not columns:
                return 0, 0
            
            sqlite_cursor.execute(f"SELECT * FROM {table_name}")
            rows = sqlite_cursor.fetchall()
            sqlite_cursor.close()
            
            if not rows:
                print(f"   ℹ️  {table_name}: No data to migrate")
                return 0, 0
            
            # Insert ke MySQL
            mysql_cursor = self.mysql_conn.cursor()
            placeholders = ', '.join(['%s'] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            migrated = 0
            skipped = 0
            
            for row in rows:
                try:
                    mysql_cursor.execute(query, row)
                    migrated += 1
                except Error as e:
                    # Skip duplicate entries
                    if 'Duplicate entry' in str(e):
                        skipped += 1
                    else:
                        print(f"   ⚠️  Error inserting row: {e}")
                        self.stats['errors'] += 1
            
            self.mysql_conn.commit()
            mysql_cursor.close()
            
            print(f"   ✅ {table_name}: {migrated} migrated, {skipped} skipped")
            self.stats['tables'][table_name] = {
                'migrated': migrated,
                'skipped': skipped
            }
            
            return migrated, skipped
            
        except Exception as e:
            print(f"   ❌ Error migrating {table_name}: {e}")
            self.stats['errors'] += 1
            return 0, 0
    
    def migrate(self):
        """Main migration function"""
        print("\n" + "="*70)
        print("📊 SQLite → MySQL Data Migration")
        print("="*70)
        
        # Connect
        print("\n🔹 Connecting to databases...")
        if not self.connect_sqlite():
            return False
        
        if not self.connect_mysql():
            return False
        
        # Get tables
        print("\n🔹 Getting table list from SQLite...")
        tables = self.get_sqlite_tables()
        
        if not tables:
            print("   ℹ️  No tables found in SQLite database")
            return True
        
        print(f"   Found {len(tables)} tables: {', '.join(tables)}")
        
        # Migrate tables
        print("\n🔹 Migrating data...")
        for table in tables:
            migrated, skipped = self.migrate_table(table)
            self.stats['migrated'] += migrated
            self.stats['skipped'] += skipped
        
        # Summary
        print("\n" + "="*70)
        print("📈 Migration Summary:")
        print(f"   Total migrated: {self.stats['migrated']} records")
        print(f"   Total skipped: {self.stats['skipped']} records")
        print(f"   Total errors: {self.stats['errors']}")
        
        if self.stats['tables']:
            print("\n   Details per table:")
            for table, counts in self.stats['tables'].items():
                print(f"      - {table}: {counts['migrated']} migrated")
        
        print("="*70)
        
        # Close connections
        if self.sqlite_conn:
            self.sqlite_conn.close()
        if self.mysql_conn:
            self.mysql_conn.close()
        
        return True

def main():
    print("\n🚀 Starting Data Migration...\n")
    
    # Ask user
    print("Apakah Anda memiliki database SQLite yang ingin dimigrasikan?")
    response = input("Enter 'yes' untuk migrate, atau 'no' untuk skip: ").strip().lower()
    
    if response != 'yes':
        print("\n✅ Skipping migration. MySQL database sudah siap digunakan.")
        return True
    
    # Get SQLite path
    migrator = DataMigrator()
    sqlite_db = migrator.find_sqlite_db()
    
    if sqlite_db:
        print(f"\n✅ Found SQLite database: {sqlite_db}")
    else:
        sqlite_db = input("Enter path ke SQLite database (atau biarkan kosong untuk skip): ").strip()
        if not sqlite_db:
            print("Skipping migration")
            return True
    
    # Get MySQL credentials
    print("\nMySQL Configuration (press Enter untuk default):")
    host = input("  Host (default: localhost): ").strip() or 'localhost'
    user = input("  User (default: root): ").strip() or 'root'
    password = input("  Password (default: kosong): ").strip() or ''
    database = input("  Database (default: pbo_db): ").strip() or 'pbo_db'
    
    # Start migration
    migrator = DataMigrator(
        sqlite_db=sqlite_db,
        mysql_config={
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
    )
    
    return migrator.migrate()

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
