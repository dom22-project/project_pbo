#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL Database Setup Script - Auto Mode
Non-interactive setup dengan default values
"""

import mysql.connector
from mysql.connector import Error
import sys
from pathlib import Path

def create_connection(host, user, password):
    """Buat koneksi ke MySQL"""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Error saat koneksi ke MySQL: {e}")
        return None

def execute_sql_file(connection, sql_file):
    """Execute SQL file"""
    try:
        cursor = connection.cursor()
        
        # Baca file SQL
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Split statements by semicolon
        statements = sql_script.split(';')
        
        success_count = 0
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    if cursor.rowcount > 0 or 'CREATE' in statement or 'INSERT' in statement:
                        success_count += 1
                except Error as e:
                    # Skip errors untuk duplicate entries
                    if 'Duplicate entry' not in str(e) and 'already exists' not in str(e):
                        print(f"⚠️  Warning: {e}")
        
        connection.commit()
        cursor.close()
        print(f"✅ SQL file executed successfully ({success_count} statements)")
        return True
        
    except Error as e:
        print(f"❌ Error saat execute SQL: {e}")
        return False

def setup_mysql_auto():
    """Setup MySQL dengan default values"""
    host = 'localhost'
    user = 'root'
    password = ''
    
    print("\n" + "="*60)
    print("🔧 MySQL Database Setup - AUTO MODE")
    print("="*60)
    print(f"\nUsing default configuration:")
    print(f"  Host: {host}")
    print(f"  User: {user}")
    print(f"  Password: <empty>")
    
    # Test koneksi
    print(f"\n📡 Connecting to MySQL...")
    connection = create_connection(host, user, password)
    
    if not connection:
        print("\n❌ Tidak bisa koneksi ke MySQL!")
        print("\n💡 Pastikan:")
        print("   1. XAMPP sudah dijalankan")
        print("   2. MySQL Service aktif")
        print("   3. Jalankan: python test_mysql_connection.py untuk diagnose")
        return False
    
    print("✅ Koneksi ke MySQL berhasil!")
    
    # Find SQL file
    sql_file = Path(__file__).parent / 'create_database.sql'
    
    if not sql_file.exists():
        print(f"\n❌ File SQL tidak ditemukan: {sql_file}")
        connection.close()
        return False
    
    print(f"\n📄 Reading SQL file: {sql_file}")
    
    # Execute SQL file
    if execute_sql_file(connection, sql_file):
        print("\n" + "="*60)
        print("✅ DATABASE SETUP BERHASIL!")
        print("="*60)
        print("\n📊 Database Info:")
        print(f"   Host: {host}")
        print(f"   Database: pbo_db")
        print(f"   User: {user}")
        print("\n✨ Tables created:")
        print("   • users (2 default users)")
        print("   • database (PBO data)")
        print("   • operation_tables (3 sample operations)")
        print("   • doctors")
        print("   • tindakan_items")
        print("   • room_types (7 room types)")
        print("   • paket_tindakan")
        print("\n🎯 Next Steps:")
        print("   1. Verify: python verify_database.py")
        print("   2. Run app: python app.py")
        print("   3. Access: http://localhost:5000")
        print("   4. Login: admin / admin123")
        print("\n" + "="*60)
        connection.close()
        return True
    else:
        print("\n❌ Gagal setup database!")
        connection.close()
        return False

if __name__ == '__main__':
    print("\n🚀 Memulai setup MySQL Database (AUTO)...\n")
    
    if setup_mysql_auto():
        sys.exit(0)
    else:
        sys.exit(1)
