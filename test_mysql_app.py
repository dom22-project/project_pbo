#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MySQL Connection in Flask App
"""

from app import app, db
from models_sqlalchemy import User, PBOData

def test_mysql_connection():
    print("\n" + "="*70)
    print("🔍 TESTING MYSQL CONNECTION IN FLASK APP")
    print("="*70)
    
    with app.app_context():
        try:
            # Get database URI
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            print(f"\n📊 Database Configuration:")
            print(f"   URI: {db_uri}")
            
            # Test connection by querying
            user_count = User.query.count()
            pbo_count = PBOData.query.count()
            
            print(f"\n✅ MySQL Connection: SUCCESS!")
            print(f"\n📈 Data in Database:")
            print(f"   Users: {user_count} records")
            print(f"   PBO Data: {pbo_count} records")
            
            # Get all tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n📋 Tables in pbo_db ({len(tables)} total):")
            for table in tables:
                print(f"   ✅ {table}")
            
            print(f"\n" + "="*70)
            print("✅ APPLICATION IS USING MYSQL SUCCESSFULLY!")
            print("="*70 + "\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print(f"\n⚠️  Could not connect to MySQL")
            print(f"   Check if XAMPP MySQL is running")
            return False

if __name__ == '__main__':
    test_mysql_connection()
