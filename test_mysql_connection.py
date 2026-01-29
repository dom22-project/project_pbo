#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL Connection Test - Non-interactive
Testing connection dengan default values
"""

import mysql.connector
from mysql.connector import Error
import socket

def test_connection():
    host = "localhost"
    user = "root"
    password = ""
    
    print("\n" + "="*60)
    print("🔍 Testing MySQL Connection")
    print("="*60)
    print(f"\nConfiguration:")
    print(f"  Host: {host}")
    print(f"  User: {user}")
    print(f"  Password: <empty>")
    
    # Check port
    print(f"\n1️⃣  Checking if MySQL is running on port 3306...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, 3306))
        sock.close()
        
        if result == 0:
            print(f"   ✅ Port 3306 is OPEN (MySQL is running)")
        else:
            print(f"   ❌ Port 3306 is CLOSED")
            print(f"\n   FIX:")
            print(f"   1. Open: C:\\xampp\\xampp-control.exe")
            print(f"   2. Click START next to MySQL")
            print(f"   3. Wait for green status")
            return False
    except Exception as e:
        print(f"   Error checking port: {e}")
        return False
    
    # Test MySQL connection
    print(f"\n2️⃣  Testing MySQL connection...")
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            print(f"   ✅ Connected to MySQL successfully!")
            
            # Get version
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            print(f"   MySQL Version: {version}")
            
            # Check database
            cursor.execute("SHOW DATABASES LIKE 'pbo_db'")
            db_exists = cursor.fetchone() is not None
            cursor.close()
            
            if db_exists:
                print(f"\n3️⃣  Database 'pbo_db':")
                print(f"   ✅ Already exists")
            else:
                print(f"\n3️⃣  Database 'pbo_db':")
                print(f"   ℹ️  Does not exist yet (will be created by setup_mysql.py)")
            
            connection.close()
            return True
            
    except mysql.connector.errors.ProgrammingError as e:
        error_msg = str(e)
        print(f"   ❌ Connection Error: {error_msg}")
        
        if "Access denied" in error_msg:
            print(f"\n   🔴 PROBLEM: Password incorrect or user not found")
            print(f"\n   SOLUTIONS:")
            print(f"   1. Check if password is really empty in XAMPP")
            print(f"   2. Try setting password:")
            print(f"      - Open XAMPP Control Panel")
            print(f"      - Click 'Admin' button for MySQL")
            print(f"      - In phpMyAdmin, check user settings")
            print(f"   3. Or reset MySQL:")
            print(f"      - Backup any important data")
            print(f"      - Reinstall XAMPP")
        
        elif "Connection refused" in error_msg:
            print(f"\n   🔴 PROBLEM: MySQL is not running")
            print(f"\n   SOLUTION:")
            print(f"   1. Open: C:\\xampp\\xampp-control.exe")
            print(f"   2. Click START next to MySQL")
            print(f"   3. Wait until it shows running (green)")
        
        return False
        
    except Exception as e:
        print(f"   ❌ Error: {type(e).__name__}: {e}")
        print(f"\n   💡 Check if mysql-connector-python is installed:")
        print(f"      pip install mysql-connector-python")
        return False

if __name__ == '__main__':
    success = test_connection()
    
    print("\n" + "="*60)
    if success:
        print("✅ SUCCESS!")
        print("\nYou can now run:")
        print("  python setup_mysql.py")
    else:
        print("❌ FAILED!")
        print("\nFix the issues above and try again")
    print("="*60 + "\n")
