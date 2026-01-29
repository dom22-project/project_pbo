#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL Database Setup - Improved Parser
Better handling of SQL statements
"""

import mysql.connector
from mysql.connector import Error
import sys
from pathlib import Path
import re

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
        print(f"❌ Error: {e}")
        return None

def parse_sql_statements(sql_content):
    """Parse SQL statements with better handling"""
    statements = []
    current_statement = ""
    in_string = False
    string_char = None
    
    for i, char in enumerate(sql_content):
        # Handle string literals
        if char in ["'", '"'] and (i == 0 or sql_content[i-1] != '\\'):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None
        
        # Handle statement separator only if not in string
        if char == ';' and not in_string:
            current_statement += char
            statements.append(current_statement.strip())
            current_statement = ""
        else:
            current_statement += char
    
    # Add last statement if it exists
    if current_statement.strip():
        statements.append(current_statement.strip())
    
    return statements

def execute_sql_file(connection, sql_file):
    """Execute SQL file with improved parsing"""
    try:
        cursor = connection.cursor()
        
        # Baca file SQL
        print(f"   Reading: {sql_file}")
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Parse statements
        statements = parse_sql_statements(sql_content)
        print(f"   Parsed {len(statements)} SQL statements")
        
        executed = 0
        skipped = 0
        
        for i, statement in enumerate(statements, 1):
            # Skip comments and empty statements
            if not statement or statement.startswith('--'):
                continue
            
            # Remove comments from statement
            statement = re.sub(r'--.*$', '', statement, flags=re.MULTILINE).strip()
            
            if not statement:
                continue
            
            try:
                # Debug: show what we're executing
                if 'CREATE' in statement.upper() or 'USE' in statement.upper() or 'INSERT' in statement.upper():
                    pass  # Silent for now
                
                cursor.execute(statement)
                executed += 1
                
                # Print progress for important statements
                if 'CREATE TABLE' in statement.upper():
                    table_name = re.search(r'CREATE TABLE.*?(\w+)\s*\(', statement, re.IGNORECASE)
                    if table_name:
                        print(f"   ✅ Table created: {table_name.group(1)}")
                elif 'INSERT' in statement.upper():
                    pass  # Silent
                elif 'CREATE DATABASE' in statement.upper():
                    print(f"   ✅ Database created/exists")
                elif 'USE' in statement.upper():
                    print(f"   ✅ Database selected")
                
            except Error as e:
                error_msg = str(e).lower()
                # Skip duplicate/existing errors
                if 'duplicate' in error_msg or 'already exists' in error_msg:
                    skipped += 1
                else:
                    print(f"   ⚠️  Error: {e}")
        
        connection.commit()
        cursor.close()
        
        print(f"\n✅ SQL execution completed")
        print(f"   Executed: {executed} statements")
        print(f"   Skipped: {skipped} statements")
        return True
        
    except Error as e:
        print(f"❌ Error: {e}")
        return False

def setup():
    """Main setup"""
    host = 'localhost'
    user = 'root'
    password = ''
    
    print("\n" + "="*70)
    print("🔧 MySQL Setup - Improved")
    print("="*70)
    
    print(f"\n📡 Connecting to MySQL...")
    print(f"   Host: {host}, User: {user}")
    
    connection = create_connection(host, user, password)
    if not connection:
        return False
    
    print(f"   ✅ Connected")
    
    # Find SQL file
    sql_file = Path(__file__).parent / 'create_database_simple.sql'
    if not sql_file.exists():
        print(f"\n❌ SQL file not found: {sql_file}")
        connection.close()
        return False
    
    print(f"\n📄 Executing SQL file...")
    if execute_sql_file(connection, sql_file):
        print("\n" + "="*70)
        print("✅ DATABASE SETUP SUCCESSFUL!")
        print("="*70)
        print("\n🎯 Next Steps:")
        print("   python verify_database.py")
        print("   python app.py")
        print("\n" + "="*70)
        connection.close()
        return True
    
    connection.close()
    return False

if __name__ == '__main__':
    print("\n🚀 Starting MySQL Setup...\n")
    success = setup()
    sys.exit(0 if success else 1)
