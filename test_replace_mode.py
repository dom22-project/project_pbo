"""
Test script untuk mode replace
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db_helper, import_excel_to_database
import openpyxl
from tempfile import NamedTemporaryFile

def create_test_excel():
    """Create a test Excel file"""
    wb = openpyxl.Workbook()
    
    # Sheet 1: db table operasi
    ws1 = wb.active
    ws1.title = 'db table operasi'
    ws1['A1'] = 'No'
    ws1['B1'] = 'Nama Tindakan'
    ws1['C1'] = 'Kelas'
    ws1['D1'] = 'Biaya Dokter'
    ws1['E1'] = 'Biaya RS'
    
    ws1['A2'] = 10
    ws1['B2'] = 'NEW Tindakan 1'
    ws1['C2'] = 'Z'
    ws1['D2'] = 999000
    ws1['E2'] = 500000
    
    ws1['A3'] = 11
    ws1['B3'] = 'NEW Tindakan 2'
    ws1['C3'] = 'Y'
    ws1['D3'] = 888000
    ws1['E3'] = 400000
    
    # Sheet 2: db nama dokter
    ws2 = wb.create_sheet('db nama dokter')
    ws2['A1'] = 'No'
    ws2['B1'] = 'Nama Dokter'
    ws2['A2'] = 1
    ws2['B2'] = 'NEW Dr. Andi'
    ws2['A3'] = 2
    ws2['B3'] = 'NEW Dr. Citra'
    
    # Save
    temp_file = NamedTemporaryFile(suffix='.xlsx', delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    wb.save(temp_path)
    return temp_path

def test_with_replace():
    """Test dengan replace mode"""
    print("="*60)
    print("TEST: Replace Mode")
    print("="*60)
    
    test_file = create_test_excel()
    
    try:
        with app.app_context():
            print("\n[BEFORE] Database status:")
            ops_before = db_helper.get_all_operations()
            docs_before = db_helper.get_all_doctors()
            print(f"  Operations: {len(ops_before)}")
            print(f"  Doctors: {len(docs_before)}")
            
            # Delete all
            print("\n[ACTION] Deleting all data...")
            db_helper.delete_all_operations()
            db_helper.delete_all_doctors()
            db_helper.delete_all_tindakan_items()
            
            print("\n[AFTER DELETE] Database status:")
            ops_after_delete = db_helper.get_all_operations()
            docs_after_delete = db_helper.get_all_doctors()
            print(f"  Operations: {len(ops_after_delete)}")
            print(f"  Doctors: {len(docs_after_delete)}")
            
            # Import new data
            print("\n[IMPORT] Importing new data...")
            stats = import_excel_to_database(test_file, db_helper)
            
            print("\n[AFTER IMPORT] Database status:")
            ops_after_import = db_helper.get_all_operations()
            docs_after_import = db_helper.get_all_doctors()
            print(f"  Operations: {len(ops_after_import)}")
            print(f"  Doctors: {len(docs_after_import)}")
            
            print("\n[IMPORT STATS]:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
            
            if len(ops_after_import) > 0 and len(docs_after_import) > 0:
                print("\n✅ REPLACE MODE TEST PASSED!")
            else:
                print("\n❌ REPLACE MODE TEST FAILED - No data imported")
                
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == '__main__':
    test_with_replace()
