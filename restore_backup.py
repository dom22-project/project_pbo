"""
Restore database from backup file
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

def restore_from_backup(backup_file):
    """Restore database from SQL backup file"""
    
    print("=" * 70)
    print(f"📥 RESTORING DATABASE FROM: {backup_file}")
    print("=" * 70)
    
    if not os.path.exists(backup_file):
        print(f"\n❌ Backup file not found: {backup_file}")
        return False
    
    try:
        # Read backup file
        with open(backup_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        print(f"\n📖 Read {len(sql_script)} bytes from backup file")
        
        # Connect to MySQL
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
        
        # Split and execute SQL statements
        statements = sql_script.split(';\n')
        success_count = 0
        
        print("\n⏳ Executing SQL statements...")
        for i, statement in enumerate(statements):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    success_count += 1
                except Exception as e:
                    print(f"   ⚠️  Statement {i+1} failed: {e}")
        
        conn.commit()
        
        print(f"\n✅ Successfully executed {success_count} statements")
        
        # Verify data
        print("\n📋 Verifying restored data:")
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"   ✅ users: {user_count} records")
        
        cursor.execute("SELECT COUNT(*) FROM operation_tables")
        op_count = cursor.fetchone()[0]
        print(f"   ✅ operation_tables: {op_count} records")
        
        cursor.execute("SELECT COUNT(*) FROM room_types")
        room_count = cursor.fetchone()[0]
        print(f"   ✅ room_types: {room_count} records")
        
        cursor.execute("SELECT COUNT(*) FROM pbo_data")
        pbo_count = cursor.fetchone()[0]
        print(f"   ✅ pbo_data: {pbo_count} records")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database restore complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during restore: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Use the latest backup file
    backup_file = "backup_pbo_20260129_112905.sql"
    restore_from_backup(backup_file)
