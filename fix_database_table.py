"""
Fix the database schema by removing the old 'database' table and ensuring 'pbo_data' is correct
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'pbo_db')

def fix_database_schema():
    """Remove old 'database' table and verify schema"""
    
    print("=" * 70)
    print("🔧 DATABASE SCHEMA FIX")
    print("=" * 70)
    
    try:
        if MYSQL_PASSWORD:
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE
            )
        else:
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                database=MYSQL_DATABASE
            )
        
        cursor = conn.cursor()
        
        print("\n📋 Current tables:")
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        for table in tables:
            print(f"   - {table}")
        
        # Check if old 'database' table exists
        if 'database' in tables:
            print("\n⚠️  Old 'database' table found! Dropping dependent tables first...")
            
            # Tables that reference 'database' table
            dependent_tables = ['paket_tindakan', 'tindakan_items']
            
            for table in dependent_tables:
                if table in tables:
                    print(f"   Dropping {table}...")
                    cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
            
            print("   Dropping old 'database' table...")
            cursor.execute("DROP TABLE IF EXISTS `database`")
            conn.commit()
            print("✅ Dropped old 'database' table and dependents")
        else:
            print("\n✅ No old 'database' table found")
        
        # Check if pbo_data table exists
        if 'pbo_data' not in tables:
            print("\n❌ 'pbo_data' table not found!")
            print("   Run create_db_schema.py to create the correct schema")
        else:
            print("✅ 'pbo_data' table exists")
        
        # Final table list
        print("\n📋 Tables after fix:")
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        for table in tables:
            print(f"   ✅ {table}")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Schema fix complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    fix_database_schema()
