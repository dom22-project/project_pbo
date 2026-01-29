#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL Database Setup Script untuk PBO Management System
Script ini akan membuat database dan tables di MySQL XAMPP
"""

import mysql.connector
from mysql.connector import Error
import sys
from pathlib import Path

def create_connection(host, user, password):
    """Buat koneksi ke MySQL tanpa database"""
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

def setup_mysql_database(host='localhost', user='root', password=''):
    """Setup MySQL database dengan semua tables"""
    print("\n" + "="*60)
    print("🔧 MySQL Database Setup untuk PBO System")
    print("="*60)
    
    # Test koneksi
    print(f"\n📡 Connecting to MySQL at {host}...")
    connection = create_connection(host, user, password)
    
    if not connection:
        print("\n❌ Tidak bisa koneksi ke MySQL!")
        print("\n💡 Pastikan:")
        print("   1. XAMPP sudah dijalankan")
        print("   2. MySQL Service aktif")
        print("   3. Username dan password benar")
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
        print("\n🎯 Next Steps:")
        print("   1. Jalankan aplikasi: python app.py")
        print("   2. Akses di browser: http://localhost:5000")
        print("   3. Login dengan:")
        print("      - Username: admin")
        print("      - Password: admin123")
        print("\n" + "="*60)
        connection.close()
        return True
    else:
        print("\n❌ Gagal setup database!")
        connection.close()
        return False

if __name__ == '__main__':
    print("\n🚀 Memulai setup MySQL Database...\n")
    
    # Get credentials from user or use defaults
    host = input("🔹 MySQL Host (default: localhost): ").strip() or 'localhost'
    user = input("🔹 MySQL User (default: root): ").strip() or 'root'
    password = input("🔹 MySQL Password (default: kosong): ").strip() or ''
    
    # Setup database
    if setup_mysql_database(host, user, password):
        sys.exit(0)
    else:
        sys.exit(1)
