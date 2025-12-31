"""
Test script untuk debugging upload database
Jalankan: python test_upload_debug.py
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db_helper, import_excel_to_database
import openpyxl
from openpyxl.styles import Font
from tempfile import NamedTemporaryFile

def create_test_excel():
    """Create a test Excel file with various data issues"""
    wb = openpyxl.Workbook()
    
    # Sheet 1: db table operasi
    ws1 = wb.active
    ws1.title = 'db table operasi'
    ws1['A1'] = 'No'
    ws1['B1'] = 'Nama Tindakan'
    ws1['C1'] = 'Kelas'
    ws1['D1'] = 'Biaya Dokter'
    ws1['E1'] = 'Biaya RS'
    
    # Test data: normal, missing value, text value
    ws1['A2'] = 1
    ws1['B2'] = 'Tindakan 1'
    ws1['C2'] = 'A'
    ws1['D2'] = 100000
    ws1['E2'] = 50000
    
    ws1['A3'] = 2
    ws1['B3'] = 'Tindakan 2'
    ws1['C3'] = 'B'
    ws1['D3'] = 'tidak_ada'  # Invalid - akan dicoba convert
    ws1['E3'] = 75000
    
    ws1['A4'] = 3
    ws1['B4'] = 'Tindakan 3'
    ws1['C4'] = 'C'
    ws1['D4'] = None  # Empty value
    ws1['E4'] = None
    
    # Sheet 2: db nama dokter
    ws2 = wb.create_sheet('db nama dokter')
    ws2['A1'] = 'No'
    ws2['B1'] = 'Nama Dokter'
    ws2['A2'] = 1
    ws2['B2'] = 'Dr. Ahmad'
    ws2['A3'] = 2
    ws2['B3'] = 'Dr. Budi'
    
    # Sheet 3: db nama tindakan (optional)
    ws3 = wb.create_sheet('db nama tindakan')
    ws3['A1'] = 'No'
    ws3['B1'] = 'Nama Tindakan'
    ws3['C1'] = 'Kelas'
    ws3['D1'] = 'Kategory'
    ws3['E1'] = 'Type'
    ws3['F1'] = 'Amount'
    
    ws3['A2'] = 1
    ws3['B2'] = 'Tindakan A'
    ws3['C2'] = 'Kelas 1'
    ws3['D2'] = 'Cat 1'
    ws3['E2'] = 'Type 1'
    ws3['F2'] = 100000
    
    # Save to temp file
    temp_file = NamedTemporaryFile(suffix='.xlsx', delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    wb.save(temp_path)
    return temp_path

def test_import():
    """Test the import function"""
    print("="*60)
    print("Testing Database Upload Import Function")
    print("="*60)
    
    # Create test Excel file
    print("\n[TEST] Creating test Excel file...")
    test_file = create_test_excel()
    print(f"[TEST] Test file created: {test_file}")
    
    try:
        print("\n[TEST] Starting import test...")
        with app.app_context():
            stats = import_excel_to_database(test_file, db_helper)
        
        print("\n" + "="*60)
        print("IMPORT RESULTS:")
        print("="*60)
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\n[TEST] OK Import test completed successfully!")
        
    except Exception as e:
        print(f"\n[TEST] ✗ Import test failed with error:")
        print(f"  {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"\n[TEST] Cleaned up test file")

def test_conversion():
    """Test type conversion safety"""
    print("\n" + "="*60)
    print("Testing Type Conversion Safety")
    print("="*60)
    
    test_values = [
        100000,
        "100000",
        "not_a_number",
        None,
        "",
        0,
    ]
    
    for val in test_values:
        try:
            result = float(val) if val else 0
            print(f"[OK] Value '{val}' -> {result}")
        except (ValueError, TypeError) as e:
            result = 0
            print(f"[OK] Value '{val}' -> {result} (error handled)")

if __name__ == '__main__':
    test_conversion()
    test_import()
    print("\n[TEST] All tests completed!")
