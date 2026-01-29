"""
Recreate all tables using Flask-SQLAlchemy models
"""

from app import app, db

print("=" * 70)
print("🔧 RECREATING DATABASE TABLES")
print("=" * 70)

with app.app_context():
    print("\n📋 Creating all tables from models...")
    
    try:
        db.create_all()
        print("✅ All tables created successfully!")
        
        # Verify tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("\n📋 Current tables in database:")
        for table in sorted(tables):
            print(f"   ✅ {table}")
        
        print(f"\n✅ Total: {len(tables)} tables")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
