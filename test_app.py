"""
Quick test to verify Flask app starts and connects to database
"""

from app import app, db

print("=" * 70)
print("✅ FLASK APPLICATION TEST")
print("=" * 70)

# Test app context
with app.app_context():
    print("\n✅ Flask app initialized successfully")
    print(f"   Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    # Test query
    from models_sqlalchemy import User
    user_count = User.query.count()
    print(f"\n✅ Database connection working!")
    print(f"   Total users: {user_count}")
    
    # List users
    users = User.query.all()
    print("\n📋 Available users:")
    for user in users:
        print(f"   - {user.id} ({user.username})")

print("\n✅ APPLICATION READY TO USE!")
print("\nTo start the Flask web server:")
print("   python app.py")
print("\nThen open your browser to:")
print("   http://localhost:5000")
