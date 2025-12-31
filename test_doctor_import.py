#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test import doctors function directly
"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment
os.environ['FLASK_ENV'] = 'development'

from app import app, db_helper, import_excel_to_database

def test_doctor_import():
    """Test doctor import from Excel"""
    print("\n=== Testing Doctor Import ===\n")
    
    # Path to test file
    test_file = Path('test_doctors.xlsx')
    
    if not test_file.exists():
        print("[ERROR] Test file not found. Running debug_doctor_upload.py first...")
        import subprocess
        subprocess.run(['python', 'debug_doctor_upload.py'])
    
    # Clear existing doctors
    print("[TEST] Clearing existing doctors...")
    with app.app_context():
        db_helper.delete_all_doctors()
        print(f"[TEST] Current doctors count: {db_helper.count_doctors()}")
        
        # Import from test file
        print(f"\n[TEST] Starting import from: {test_file}")
        try:
            stats = import_excel_to_database(str(test_file), db_helper)
            
            print("\n[TEST] Import Statistics:")
            print(f"  - Doctors imported: {stats.get('doctors_imported', 0)}")
            print(f"  - Doctors duplicates: {stats.get('doctors_duplicates', 0)}")
            print(f"  - Doctors skipped: {stats.get('doctors_skipped', 0)}")
            
            # Verify doctors in database
            print(f"\n[TEST] Verifying doctors in database...")
            all_doctors = db_helper.get_all_doctors()
            print(f"[TEST] Total doctors in DB: {len(all_doctors)}")
            
            if all_doctors:
                print("\n[TEST] Doctors in database:")
                for doctor in all_doctors:
                    print(f"  - {doctor['nama_dokter']} (ID: {doctor['id']})")
            else:
                print("[ERROR] No doctors found in database after import!")
            
            return stats
            
        except Exception as e:
            print(f"[ERROR] Import failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

if __name__ == '__main__':
    result = test_doctor_import()
    if result:
        print("\n✓ Test completed successfully")
    else:
        print("\n✗ Test failed")
