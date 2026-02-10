#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Verification Script untuk PBO System
Verifikasi koneksi MySQL dan status database
"""

import mysql.connector
from mysql.connector import Error
import sys
from pathlib import Path

def check_mysql_connection(host, user, password, database=None):
    """Check koneksi ke MySQL"""
    try:
        config = {
            'host': host,
            'user': user,
            'password': password,
        }
        if database:
            config['database'] = database
            
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return True, connection
    except Error as e:
        return False, str(e)

def get_mysql_version(connection):
    """Get MySQL version"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()[0]
        cursor.close()
        return version
    except:
        return None

def check_database_exists(connection, database_name):
    """Check apakah database sudah ada"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{database_name}'")
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    except:
        return False

def get_table_count(connection, database_name):
    """Get jumlah tables di database"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = '{database_name}'
        """)
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    except:
        return 0

def get_tables(connection, database_name):
    """Get daftar tables"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = '{database_name}'
            ORDER BY TABLE_NAME
        """)
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables
    except:
        return []

def check_table_structure(connection, database_name, table_name):
    """Check struktur table"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"DESC {database_name}.{table_name}")
        columns = cursor.fetchall()
        cursor.close()
        return len(columns)
    except:
        return 0

def get_row_counts(connection, database_name):
    """Get jumlah rows di setiap table"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT TABLE_NAME, TABLE_ROWS
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = '{database_name}'
            ORDER BY TABLE_NAME
        """)
        result = {}
        for row in cursor.fetchall():
            result[row[0]] = row[1] if row[1] else 0
        cursor.close()
        return result
    except:
        return {}

def verify_database():
    """Main verification function"""
    print("\n" + "="*70)
    print("🔍 PBO System - Database Verification")
    print("="*70)
    
    # Configuration
    host = 'localhost'
    user = 'root'
    password = ''
    database = 'pbo_db'
    
    print(f"\n📡 Configuration:")
    print(f"   Host: {host}")
    print(f"   User: {user}")
    print(f"   Database: {database}")
    
    # Check MySQL connection
    print(f"\n🔹 Checking MySQL connection...")
    success, result = check_mysql_connection(host, user, password)
    
    if not success:
        print(f"   ❌ Failed to connect to MySQL")
        print(f"   Error: {result}")
        print(f"\n💡 Solutions:")
        print(f"   1. Pastikan MySQL service aktif di XAMPP Control Panel")
        print(f"   2. Cek port 3306 tidak terblokir")
        print(f"   3. Verify username/password MySQL")
        return False
    
    connection = result
    print(f"   ✅ Connected to MySQL")
    
    # Get MySQL version
    version = get_mysql_version(connection)
    if version:
        print(f"   ℹ️  MySQL Version: {version}")
    
    # Check database exists
    print(f"\n🔹 Checking database '{database}'...")
    if check_database_exists(connection, database):
        print(f"   ✅ Database '{database}' exists")
    else:
        print(f"   ❌ Database '{database}' not found")
        print(f"\n💡 Solution: Run 'python setup_mysql.py' to create database")
        connection.close()
        return False
    
    # Check tables
    print(f"\n🔹 Checking tables...")
    table_count = get_table_count(connection, database)
    print(f"   Total tables: {table_count}")
    
    required_tables = [
        'users',
        'operation_tables',
        'doctors',
        'tindakan_items',
        'room_types',
        'database',
        'paket_tindakan'
    ]
    
    tables = get_tables(connection, database)
    
    missing_tables = []
    for table in required_tables:
        if table in tables:
            col_count = check_table_structure(connection, database, table)
            print(f"   ✅ {table} ({col_count} columns)")
        else:
            print(f"   ❌ {table} - MISSING")
            missing_tables.append(table)
    
    # Check row counts
    print(f"\n🔹 Data Statistics:")
    row_counts = get_row_counts(connection, database)
    
    important_tables = {
        'users': 'Users',
        'database': 'PBO Records',
        'operation_tables': 'Operations',
        'doctors': 'Doctors',
        'room_types': 'Room Types'
    }
    
    for table, label in important_tables.items():
        if table in row_counts:
            count = row_counts[table]
            status = "✅" if count > 0 else "ℹ️ "
            print(f"   {status} {label}: {count} records")
    
    # Summary
    print(f"\n" + "="*70)
    
    if not missing_tables:
        print("✅ DATABASE VERIFICATION SUCCESS!")
        print("   All required tables exist and database is ready to use.")
    else:
        print("⚠️  DATABASE VERIFICATION WARNING!")
        print(f"   Missing tables: {', '.join(missing_tables)}")
        print("   Please run 'python setup_mysql.py' to create missing tables.")
    
    print("="*70)
    
    # Connection info
    print(f"\n📊 Connection String (for reference):")
    print(f"   mysql+mysqlconnector://root:@localhost/pbo_db")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Run application: python app.py")
    print(f"   2. Access: http://localhost:5000")
    print(f"   3. Login with: admin / admin123")
    
    connection.close()
    return len(missing_tables) == 0

if __name__ == '__main__':
    try:
        success = verify_database()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
