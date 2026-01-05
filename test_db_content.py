"""Test hasil import ke database"""
import sys
sys.path.insert(0, r"c:\Users\agung.daniel\Project PBO\app pbo")

from app import app
from models import Database

db_helper = Database()

with app.app_context():
    print("Checking database content...")
    print()

    # Check operations
    try:
        ops = db_helper.get_all_operations()
        print(f"Total Operations: {len(ops) if ops else 0}")
        if ops and len(ops) > 0:
            for i, op in enumerate(ops[:5]):
                print(f"  {i+1}. {op}")
        print()
    except Exception as e:
        print(f"Error checking operations: {e}")
        print()

    # Check doctors  
    try:
        doc_count = db_helper.count_doctors()
        print(f"Total Doctors: {doc_count}")
        print()
    except Exception as e:
        print(f"Error checking doctors: {e}")
        print()

    # Check tindakan
    try:
        tind_count = db_helper.count_tindakan_items()
        print(f"Total Tindakan Items: {tind_count}")
        print()
    except Exception as e:
        print(f"Error checking tindakan: {e}")
        print()
