#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic Tool - MySQL Connection Troubleshooter
"""

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

print("\n" + "="*70)
print("🔍 MYSQL CONNECTION DIAGNOSTIC TOOL")
print("="*70)

# Get config from .env
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'pbo_db')

print("\n📋 Configuration from .env:")
print(f"   Host: {MYSQL_HOST}")
print(f"   Port: {MYSQL_PORT}")
print(f"   User: {MYSQL_USER}")
print(f"   Password: {'(empty)' if not MYSQL_PASSWORD else '***'}")
print(f"   Database: {MYSQL_DATABASE}")

# Step 1: Test connection to MySQL server (without database)
print("\n" + "-"*70)
print("Step 1️⃣ : Testing MySQL Server Connection...")
print("-"*70)

try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        auth_plugin='mysql_native_password'
    )
    
    if conn.is_connected():
        print("✅ Connected to MySQL Server!")
        
        # Get MySQL info
        db_info = conn.get_server_info()
        print(f"   MySQL Version: {db_info}")
        
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE()")
        result = cursor.fetchone()
        print(f"   Current Database: {result[0] or 'None'}")
        cursor.close()
    else:
        print("❌ Connection failed")
        
except Error as e:
    print(f"❌ ERROR: {e}")
    print(f"\n💡 Possible causes:")
    print(f"   1. XAMPP MySQL not running")
    print(f"   2. Wrong host/port in .env")
    print(f"   3. Wrong username/password")
    conn = None

# Step 2: List all databases
if conn:
    print("\n" + "-"*70)
    print("Step 2️⃣ : Listing Available Databases...")
    print("-"*70)
    
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        
        print(f"✅ Found {len(databases)} database(s):")
        for db in databases:
            db_name = db[0]
            marker = "📍" if db_name == MYSQL_DATABASE else "  "
            print(f"   {marker} {db_name}")
        
        cursor.close()
        
        # Check if pbo_db exists
        db_names = [db[0] for db in databases]
        if MYSQL_DATABASE in db_names:
            print(f"\n✅ Database '{MYSQL_DATABASE}' EXISTS!")
        else:
            print(f"\n❌ Database '{MYSQL_DATABASE}' NOT FOUND!")
            print(f"   Available: {', '.join(db_names)}")
            
    except Error as e:
        print(f"❌ ERROR: {e}")

# Step 3: Connect to specific database
if conn:
    print("\n" + "-"*70)
    print(f"Step 3️⃣ : Connecting to Database '{MYSQL_DATABASE}'...")
    print("-"*70)
    
    try:
        conn.database = MYSQL_DATABASE
        print(f"✅ Connected to '{MYSQL_DATABASE}'!")
        
        # List tables
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"\n✅ Found {len(tables)} table(s):")
            for table in tables:
                table_name = table[0]
                
                # Count rows
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                print(f"   📋 {table_name:25} ({row_count} rows)")
        else:
            print(f"\n⚠️  Database exists but has NO tables")
            
        cursor.close()
        
    except Error as e:
        print(f"❌ ERROR: {e}")
        print(f"\n💡 If error is 'Unknown database', need to create it:")
        print(f"   - Use phpMyAdmin to create database '{MYSQL_DATABASE}'")
        print(f"   - Or run: CREATE DATABASE {MYSQL_DATABASE};")

# Step 4: Test Flask SQLAlchemy connection
if conn:
    print("\n" + "-"*70)
    print("Step 4️⃣ : Testing Flask-SQLAlchemy Connection...")
    print("-"*70)
    
    try:
        from app import app, db
        from sqlalchemy import text
        
        with app.app_context():
            # Try to execute a simple query
            result = db.session.execute(text("SELECT 1"))
            print("✅ Flask-SQLAlchemy Connection: SUCCESS!")
            
            # Show models
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"\n   Tables accessible via SQLAlchemy: {len(tables)}")
            for table in tables:
                print(f"   📋 {table}")
                
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"\n💡 Flask connection failed. Check:")
        print(f"   - Is XAMPP MySQL running?")
        print(f"   - Is database '{MYSQL_DATABASE}' created?")
        print(f"   - Is .env configuration correct?")

# Close connection
if conn and conn.is_connected():
    conn.close()
    print("\n✅ Connection closed")

print("\n" + "="*70)
print("🔍 DIAGNOSTIC COMPLETE")
print("="*70 + "\n")
