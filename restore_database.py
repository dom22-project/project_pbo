#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restore Database MySQL PBO
Import data dari file SQL backup
"""

import mysql.connector
from mysql.connector import Error
import os
import sys

def restore_database(backup_file):
    """Restore database dari file SQL"""
    
    host = 'localhost'
    user = 'root'
    password = ''
    database = 'pbo_db'
    
    print("\n" + "="*70)
    print("♻️  PBO Database Restore Tool")
    print("="*70)
    
    # Check if file exists
    if not os.path.exists(backup_file):
        print(f"\n❌ File not found: {backup_file}")
        return False
    
    print(f"\n📂 Backup file: {backup_file}")
    file_size = os.path.getsize(backup_file)
    print(f"   Size: {file_size / 1024:.2f} KB")
    
    print(f"\n⚠️  Warning: Ini akan DROP semua tabel existing!")
    response = input("   Lanjutkan restore? (yes/no): ").strip().lower()
    if response != 'yes':
        print("   ❌ Cancelled")
        return False
    
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
    
    try:
        print(f"\n📖 Reading backup file...")
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        
        print(f"✅ File loaded")
        
        # Split statements by ; (careful with strings)
        print(f"\n⚙️  Parsing SQL statements...")
        statements = []
        current_stmt = ""
        in_string = False
        escape_next = False
        
        for char in backup_content:
            if escape_next:
                current_stmt += char
                escape_next = False
                continue
            
            if char == '\\':
                escape_next = True
                current_stmt += char
                continue
            
            if char == "'":
                in_string = not in_string
                current_stmt += char
                continue
            
            if char == ';' and not in_string:
                stmt = current_stmt.strip()
                if stmt and not stmt.startswith('--'):
                    statements.append(stmt)
                current_stmt = ""
                continue
            
            current_stmt += char
        
        # Add last statement if any
        if current_stmt.strip():
            statements.append(current_stmt.strip())
        
        print(f"✅ {len(statements)} statements parsed")
        
        # Execute statements
        print(f"\n🔄 Executing statements...")
        success_count = 0
        error_count = 0
        
        for i, stmt in enumerate(statements, 1):
            try:
                if stmt.startswith('--'):
                    continue
                
                cursor.execute(stmt)
                success_count += 1
                
                # Show progress
                if i % 10 == 0:
                    print(f"   ✅ {success_count}/{len(statements)} statements executed")
                    
            except Error as e:
                error_count += 1
                print(f"   ⚠️  Statement {i}: {str(e)[:80]}")
        
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n✅ Restore completed!")
        print(f"   Success: {success_count}")
        print(f"   Errors: {error_count}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Restore failed: {e}")
        return False

if __name__ == '__main__':
    print("\n🚀 PBO Database Restore\n")
    
    # Get backup file from argument or ask user
    if len(sys.argv) > 1:
        backup_file = sys.argv[1]
    else:
        # List available backup files
        backup_files = [f for f in os.listdir('.') if f.startswith('backup_pbo_') and f.endswith('.sql')]
        
        if not backup_files:
            print("❌ No backup files found!")
            print("\nUsage: python restore_database.py <backup_file>")
            print("   or")
            print("   python restore_database.py backup_pbo_20260129_120000.sql")
            sys.exit(1)
        
        print("📋 Available backup files:")
        for i, f in enumerate(backup_files, 1):
            size = os.path.getsize(f) / 1024
            print(f"   {i}. {f} ({size:.2f} KB)")
        
        try:
            choice = int(input("\nSelect file (number): ")) - 1
            if choice < 0 or choice >= len(backup_files):
                print("❌ Invalid choice")
                sys.exit(1)
            backup_file = backup_files[choice]
        except ValueError:
            print("❌ Invalid input")
            sys.exit(1)
    
    if restore_database(backup_file):
        print("\n" + "="*70)
        print("✅ SUCCESS!")
        print("="*70)
        print("\nVerify data dengan:")
        print("   python verify_database.py")
        print("\nJalankan aplikasi:")
        print("   python app.py")
        print("="*70 + "\n")
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("❌ RESTORE FAILED")
        print("="*70 + "\n")
        sys.exit(1)
