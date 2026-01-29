#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL Connection Diagnostics Script
Untuk diagnose masalah koneksi ke MySQL
"""

import mysql.connector
from mysql.connector import Error
import socket
import sys

def check_port(host, port):
    """Check apakah port terbuka"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error checking port: {e}")
        return False

def test_mysql_connection(host, user, password):
    """Test koneksi ke MySQL dengan detail error"""
    print("\n" + "="*60)
    print("🔍 MySQL Connection Diagnostic")
    print("="*60)
    
    # Step 1: Check port
    print(f"\n1️⃣  Checking if MySQL port {3306} is open on {host}...")
    if check_port(host, 3306):
        print(f"   ✅ Port 3306 is open")
    else:
        print(f"   ❌ Port 3306 is NOT open or MySQL is not running")
        print(f"\n   💡 SOLUTION:")
        print(f"      1. Open XAMPP Control Panel: C:\\xampp\\xampp-control.exe")
        print(f"      2. Click START for MySQL")
        print(f"      3. Wait for it to turn green")
        return False
    
    # Step 2: Try connection
    print(f"\n2️⃣  Attempting connection to MySQL...")
    print(f"   Host: {host}")
    print(f"   User: {user}")
    print(f"   Password: {'<empty>' if not password else '***'}")
    
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            print(f"   ✅ Connected successfully!")
            
            # Get version
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            print(f"   ℹ️  MySQL Version: {version}")
            cursor.close()
            
            # Check if database exists
            print(f"\n3️⃣  Checking if database 'pbo_db' exists...")
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES LIKE 'pbo_db'")
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                print(f"   ✅ Database 'pbo_db' EXISTS")
            else:
                print(f"   ℹ️  Database 'pbo_db' does not exist yet (will be created)")
            
            connection.close()
            return True
            
    except mysql.connector.errors.ProgrammingError as e:
        print(f"   ❌ Connection failed: {e}")
        error_msg = str(e)
        
        if "Access denied" in error_msg:
            print(f"\n   💡 SOLUTION (Access Denied):")
            print(f"      The password might be wrong!")
            print(f"      In XAMPP, default MySQL password is EMPTY (kosong)")
            print(f"      Try with empty password")
            
            # Try again with empty password
            if password != "":
                print(f"\n      Trying again with empty password...")
                try:
                    conn = mysql.connector.connect(
                        host=host,
                        user=user,
                        password=""
                    )
                    if conn.is_connected():
                        print(f"      ✅ Connected with empty password!")
                        conn.close()
                        return True
                except:
                    pass
        
        elif "Unknown MySQL server host" in error_msg:
            print(f"\n   💡 SOLUTION (Unknown Host):")
            print(f"      Host '{host}' not found")
            print(f"      Use 'localhost' or '127.0.0.1'")
        
        elif "Connection refused" in error_msg:
            print(f"\n   💡 SOLUTION (Connection Refused):")
            print(f"      MySQL is not running on port 3306")
            print(f"      1. Open XAMPP Control Panel")
            print(f"      2. Start MySQL service")
            print(f"      3. Wait until it shows green/running")
        
        return False
        
    except Exception as e:
        print(f"   ❌ Unexpected error: {type(e).__name__}: {e}")
        print(f"\n   💡 SOLUTION:")
        print(f"      1. Ensure mysql-connector-python is installed:")
        print(f"         pip install mysql-connector-python")
        print(f"      2. Ensure XAMPP MySQL is running")
        print(f"      3. Try again")
        return False

def main():
    print("\n🚀 MySQL Connection Troubleshooting\n")
    
    # Get user input
    host = input("MySQL Host (default: localhost): ").strip() or "localhost"
    user = input("MySQL User (default: root): ").strip() or "root"
    password = input("MySQL Password (default: empty): ").strip() or ""
    
    # Test connection
    success = test_mysql_connection(host, user, password)
    
    # Results
    print("\n" + "="*60)
    if success:
        print("✅ CONNECTION SUCCESSFUL!")
        print("\nYou can now run: python setup_mysql.py")
    else:
        print("❌ CONNECTION FAILED!")
        print("\nPlease follow the solutions above and try again.")
    print("="*60)
    
    return 0 if success else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(1)
