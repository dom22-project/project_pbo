#!/usr/bin/env python
"""Fix auto-increment issue in database table"""
import mysql.connector
from config import Config

try:
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )
    cursor = conn.cursor()
    
    print("Checking for ID=0 records...")
    cursor.execute("SELECT id, nama_pasien FROM database WHERE id = 0")
    result = cursor.fetchone()
    if result:
        print(f"Found record with ID=0: {result}")
        print("Deleting record with ID=0...")
        cursor.execute("DELETE FROM database WHERE id = 0")
        conn.commit()
        print("Deleted successfully")
    else:
        print("No record with ID=0 found")
    
    print("\nChecking current auto-increment value...")
    cursor.execute("SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_NAME='database' AND TABLE_SCHEMA=%s", (Config.MYSQL_DATABASE,))
    result = cursor.fetchone()
    if result:
        print(f"Current AUTO_INCREMENT: {result[0]}")
    
    # Check max ID
    cursor.execute("SELECT MAX(id) FROM database")
    max_id = cursor.fetchone()[0]
    print(f"Max ID in table: {max_id}")
    
    if max_id is not None:
        new_auto_increment = max_id + 1
        print(f"\nSetting AUTO_INCREMENT to {new_auto_increment}...")
        cursor.execute(f"ALTER TABLE database AUTO_INCREMENT = {new_auto_increment}")
        conn.commit()
        print("AUTO_INCREMENT set successfully")
    
    cursor.close()
    conn.close()
    print("\nFix completed successfully!")
    
except Exception as e:
    print(f"Error: {str(e)}")