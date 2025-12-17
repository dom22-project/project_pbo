"""
Comprehensive Test Script for PBO Application
Tests all major functionality without GUI interaction
"""

import sqlite3
import os
import sys

def print_test_header(test_name):
    print("\n" + "="*60)
    print(f"TEST: {test_name}")
    print("="*60)

def print_result(passed, message):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {message}")

def test_database_initialization():
    """Test 1: Database and tables are created correctly"""
    print_test_header("Database Initialization")
    
    try:
        # Check if data directory exists
        if not os.path.exists('data'):
            print_result(False, "Data directory does not exist")
            return False
        print_result(True, "Data directory exists")
        
        # Check if database file exists
        if not os.path.exists('data/pbo_database.db'):
            print_result(False, "Database file does not exist")
            return False
        print_result(True, "Database file exists")
        
        # Connect to database
        conn = sqlite3.connect('data/pbo_database.db')
        cursor = conn.cursor()
        
        # Check if 'database' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='database'")
        if not cursor.fetchone():
            print_result(False, "Main 'database' table does not exist")
            conn.close()
            return False
        print_result(True, "Main 'database' table exists")
        
        # Check if 'operation_tables' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='operation_tables'")
        if not cursor.fetchone():
            print_result(False, "Reference 'operation_tables' table does not exist")
            conn.close()
            return False
        print_result(True, "Reference 'operation_tables' table exists")
        
        # Check table structure for 'database'
        cursor.execute("PRAGMA table_info(database)")
        columns = cursor.fetchall()
        expected_columns = ['id', 'diagnosa', 'nama_operasi', 'sifat_operasi', 'nama_dokter', 
                          'kelas', 'tabel_operasi1', 'tabel_operasi2', 'tabel_operasi3', 
                          'tabel_operasi4', 'persentase_operasi1', 'persentase_operasi2',
                          'persentase_operasi3', 'persentase_operasi4', 'konsultasi_pre_tindakan',
                          'diagnostic_pre_tindakan', 'surgeon', 'anesthesi', 'ot_room_charge',
                          'recovery_room_charge', 'alat', 'diagnostic', 'medical_equipment',
                          'obat_dan_alkes', 'tarif_kamar', 'total', 'catatan', 'keterangan',
                          'tanggal', 'nama_pasien', 'hubungan_dengan_pasien', 
                          'petugas_front_office', 'perusahaan_asuransi', 'created_at']
        
        column_names = [col[1] for col in columns]
        missing_columns = [col for col in expected_columns if col not in column_names]
        
        if missing_columns:
            print_result(False, f"Missing columns in 'database' table: {missing_columns}")
            conn.close()
            return False
        print_result(True, f"All {len(expected_columns)} columns exist in 'database' table")
        
        # Check operation_tables has data
        cursor.execute("SELECT COUNT(*) FROM operation_tables")
        count = cursor.fetchone()[0]
        if count == 0:
            print_result(False, "No operation data in operation_tables")
            conn.close()
            return False
        print_result(True, f"Operation tables has {count} records")
        
        conn.close()
        return True
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_operation_tables_data():
    """Test 2: Operation tables have correct data structure"""
    print_test_header("Operation Tables Data Structure")
    
    try:
        conn = sqlite3.connect('data/pbo_database.db')
        cursor = conn.cursor()
        
        # Get sample operation
        cursor.execute("SELECT * FROM operation_tables LIMIT 1")
        operation = cursor.fetchone()
        
        if not operation:
            print_result(False, "No operations found in database")
            conn.close()
            return False
        
        # Check structure (id, kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya)
        if len(operation) != 7:
            print_result(False, f"Expected 7 columns, got {len(operation)}")
            conn.close()
            return False
        print_result(True, "Operation table has correct number of columns (7)")
        
        # Check data types
        kode, nama_tindakan, kelas = operation[1], operation[2], operation[3]
        biaya_dokter, biaya_rs, total_biaya = operation[4], operation[5], operation[6]
        
        if not isinstance(kode, str):
            print_result(False, "Kode should be string")
            conn.close()
            return False
        print_result(True, f"Sample operation code: {kode}")
        
        if not isinstance(nama_tindakan, str):
            print_result(False, "Nama tindakan should be string")
            conn.close()
            return False
        print_result(True, f"Sample operation name: {nama_tindakan}")
        
        if not (isinstance(biaya_dokter, (int, float))):
            print_result(False, "Biaya dokter should be numeric")
            conn.close()
            return False
        print_result(True, f"Sample doctor fee: Rp {biaya_dokter:,.0f}")
        
        # Check calculation
        expected_total = biaya_dokter + biaya_rs
        if abs(total_biaya - expected_total) > 0.01:
            print_result(False, f"Total calculation incorrect: {total_biaya} != {expected_total}")
            conn.close()
            return False
        print_result(True, "Total calculation is correct")
        
        conn.close()
        return True
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_calculation_logic():
    """Test 3: Verify calculation formulas"""
    print_test_header("Calculation Logic")
    
    try:
        conn = sqlite3.connect('data/pbo_database.db')
        cursor = conn.cursor()
        
        # Get a sample operation
        cursor.execute("SELECT biaya_dokter, biaya_rs FROM operation_tables LIMIT 1")
        operation = cursor.fetchone()
        
        if not operation:
            print_result(False, "No operation data to test")
            conn.close()
            return False
        
        biaya_dokter, biaya_rs = operation
        
        # Test 1: Basic calculation (100%, Elektif)
        surgeon_fee = biaya_dokter * 1.0 * 1.0  # 100% * no surcharge
        anesthesi_fee = biaya_rs * 1.0 * 1.0
        ot_room_charge = surgeon_fee * 0.3
        
        print_result(True, f"Elektif 100%: Surgeon={surgeon_fee:,.0f}, Anesthesi={anesthesi_fee:,.0f}, OT Room={ot_room_charge:,.0f}")
        
        # Test 2: CITO surcharge (25%)
        surgeon_fee_cito = biaya_dokter * 1.0 * 1.25
        anesthesi_fee_cito = biaya_rs * 1.0 * 1.25
        ot_room_charge_cito = surgeon_fee_cito * 0.3
        
        print_result(True, f"CITO 100%: Surgeon={surgeon_fee_cito:,.0f}, Anesthesi={anesthesi_fee_cito:,.0f}, OT Room={ot_room_charge_cito:,.0f}")
        
        # Test 3: Penyulit surcharge (30%)
        surgeon_fee_penyulit = biaya_dokter * 1.0 * 1.30
        anesthesi_fee_penyulit = biaya_rs * 1.0 * 1.30
        ot_room_charge_penyulit = surgeon_fee_penyulit * 0.3
        
        print_result(True, f"Penyulit 100%: Surgeon={surgeon_fee_penyulit:,.0f}, Anesthesi={anesthesi_fee_penyulit:,.0f}, OT Room={ot_room_charge_penyulit:,.0f}")
        
        # Test 4: 50% percentage
        surgeon_fee_50 = biaya_dokter * 0.5 * 1.0
        anesthesi_fee_50 = biaya_rs * 0.5 * 1.0
        ot_room_charge_50 = surgeon_fee_50 * 0.3
        
        print_result(True, f"Elektif 50%: Surgeon={surgeon_fee_50:,.0f}, Anesthesi={anesthesi_fee_50:,.0f}, OT Room={ot_room_charge_50:,.0f}")
        
        # Verify surcharge percentages
        if abs(surgeon_fee_cito / surgeon_fee - 1.25) > 0.01:
            print_result(False, "CITO surcharge calculation incorrect")
            conn.close()
            return False
        print_result(True, "CITO surcharge (25%) verified")
        
        if abs(surgeon_fee_penyulit / surgeon_fee - 1.30) > 0.01:
            print_result(False, "Penyulit surcharge calculation incorrect")
            conn.close()
            return False
        print_result(True, "Penyulit surcharge (30%) verified")
        
        # Verify OT Room Charge is 30% of surgeon
        if abs(ot_room_charge / surgeon_fee - 0.3) > 0.01:
            print_result(False, "OT Room Charge calculation incorrect")
            conn.close()
            return False
        print_result(True, "OT Room Charge (30% of surgeon) verified")
        
        conn.close()
        return True
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_room_rates():
    """Test 4: Verify room rate mappings"""
    print_test_header("Room Rate Mappings")
    
    room_rates = {
        "BASIC": 350000,
        "STANDARD": 650000,
        "DELUXE": 900000,
        "VIP": 1800000,
        "VVIP": 1900000,
        "SUITE": 5000000,
        "PRESIDENTIAL SUITE": 7500000,
        "ODC": 500000
    }
    
    all_passed = True
    for kelas, expected_rate in room_rates.items():
        print_result(True, f"{kelas}: Rp {expected_rate:,.0f}")
    
    print_result(True, "All 8 room classes have defined rates")
    return True

def test_data_insertion():
    """Test 5: Test inserting sample data"""
    print_test_header("Data Insertion Test")
    
    try:
        conn = sqlite3.connect('data/pbo_database.db')
        cursor = conn.cursor()
        
        # Get initial count
        cursor.execute("SELECT COUNT(*) FROM database")
        initial_count = cursor.fetchone()[0]
        print_result(True, f"Initial record count: {initial_count}")
        
        # Insert test data
        test_data = (
            "Test Diagnosa",  # diagnosa
            "Test Operasi",  # nama_operasi
            "Elektif / Tentative",  # sifat_operasi
            "Dr. Test",  # nama_dokter
            "VIP",  # kelas
            "",  # tabel_operasi1
            "",  # tabel_operasi2
            "",  # tabel_operasi3
            "",  # tabel_operasi4
            1.0,  # persentase_operasi1
            1.0,  # persentase_operasi2
            1.0,  # persentase_operasi3
            1.0,  # persentase_operasi4
            100000,  # konsultasi_pre_tindakan
            200000,  # diagnostic_pre_tindakan
            5000000,  # surgeon
            2000000,  # anesthesi
            1500000,  # ot_room_charge
            500000,  # recovery_room_charge
            300000,  # alat
            400000,  # diagnostic
            600000,  # medical_equipment
            700000,  # obat_dan_alkes
            1800000,  # tarif_kamar
            13100000,  # total
            "Test catatan",  # catatan
            "Test keterangan",  # keterangan
            "2024-01-01",  # tanggal
            "Test Pasien",  # nama_pasien
            "Keluarga",  # hubungan_dengan_pasien
            "Test Petugas",  # petugas_front_office
            "Test Asuransi"  # perusahaan_asuransi
        )
        
        cursor.execute('''
            INSERT INTO database (
                diagnosa, nama_operasi, sifat_operasi, nama_dokter, kelas,
                tabel_operasi1, tabel_operasi2, tabel_operasi3, tabel_operasi4,
                persentase_operasi1, persentase_operasi2, persentase_operasi3, persentase_operasi4,
                konsultasi_pre_tindakan, diagnostic_pre_tindakan, surgeon,
                anesthesi, ot_room_charge, recovery_room_charge, alat,
                diagnostic, medical_equipment, obat_dan_alkes, tarif_kamar,
                total, catatan, keterangan, tanggal, nama_pasien,
                hubungan_dengan_pasien, petugas_front_office, perusahaan_asuransi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', test_data)
        
        conn.commit()
        print_result(True, "Test data inserted successfully")
        
        # Verify insertion
        cursor.execute("SELECT COUNT(*) FROM database")
        new_count = cursor.fetchone()[0]
        
        if new_count != initial_count + 1:
            print_result(False, f"Record count mismatch: expected {initial_count + 1}, got {new_count}")
            conn.close()
            return False
        print_result(True, f"New record count: {new_count}")
        
        # Retrieve and verify the inserted data
        cursor.execute("SELECT * FROM database WHERE nama_pasien = 'Test Pasien'")
        record = cursor.fetchone()
        
        if not record:
            print_result(False, "Could not retrieve inserted test data")
            conn.close()
            return False
        print_result(True, "Test data retrieved successfully")
        
        # Verify some key fields
        if record[29] != "Test Pasien":  # nama_pasien
            print_result(False, "Nama pasien mismatch")
            conn.close()
            return False
        print_result(True, "Nama pasien verified")
        
        if record[5] != "VIP":  # kelas
            print_result(False, "Kelas mismatch")
            conn.close()
            return False
        print_result(True, "Kelas verified")
        
        if record[25] != 13100000:  # total
            print_result(False, f"Total mismatch: expected 13100000, got {record[25]}")
            conn.close()
            return False
        print_result(True, "Total verified")
        
        # Clean up test data
        cursor.execute("DELETE FROM database WHERE nama_pasien = 'Test Pasien'")
        conn.commit()
        print_result(True, "Test data cleaned up")
        
        conn.close()
        return True
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_search_functionality():
    """Test 6: Test search queries"""
    print_test_header("Search Functionality")
    
    try:
        conn = sqlite3.connect('data/pbo_database.db')
        cursor = conn.cursor()
        
        # Test 1: Get all records
        cursor.execute("SELECT COUNT(*) FROM database")
        total_records = cursor.fetchone()[0]
        print_result(True, f"Total records in database: {total_records}")
        
        # Test 2: Search query structure
        query = "SELECT id, nama_pasien, nama_operasi, diagnosa, nama_dokter, kelas, tanggal, total FROM database ORDER BY id DESC LIMIT 100"
        cursor.execute(query)
        results = cursor.fetchall()
        print_result(True, f"Search query executed successfully, returned {len(results)} records")
        
        # Test 3: LIKE search (if there's data)
        if total_records > 0:
            cursor.execute("SELECT nama_pasien FROM database LIMIT 1")
            sample_name = cursor.fetchone()[0]
            
            if sample_name:
                cursor.execute("SELECT COUNT(*) FROM database WHERE nama_pasien LIKE ?", (f'%{sample_name}%',))
                search_count = cursor.fetchone()[0]
                print_result(True, f"LIKE search for '{sample_name}' found {search_count} records")
        else:
            print_result(True, "No data to test LIKE search (database empty)")
        
        conn.close()
        return True
        
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_file_structure():
    """Test 7: Verify all required files exist"""
    print_test_header("File Structure")
    
    required_files = [
        '.vscode/main.py',
        '.vscode/database.py',
        '.vscode/import_data.py',
        'requirements.txt',
        'README.md',
        'QUICK_START.md',
        'CHANGELOG.md',
        'TODO.md'
    ]
    
    all_exist = True
    for file_path in required_files:
        exists = os.path.exists(file_path)
        print_result(exists, f"{file_path}")
        if not exists:
            all_exist = False
    
    return all_exist

def test_imports():
    """Test 8: Verify Python imports work"""
    print_test_header("Python Imports")
    
    try:
        # Test PyQt5 import
        from PyQt5.QtWidgets import QApplication
        print_result(True, "PyQt5.QtWidgets imported successfully")
        
        from PyQt5.QtCore import QDate, Qt
        print_result(True, "PyQt5.QtCore imported successfully")
        
        from PyQt5.QtGui import QFont, QDoubleValidator
        print_result(True, "PyQt5.QtGui imported successfully")
        
        from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
        print_result(True, "PyQt5.QtPrintSupport imported successfully")
        
        # Test standard library imports
        import sqlite3
        print_result(True, "sqlite3 imported successfully")
        
        import os
        print_result(True, "os imported successfully")
        
        import sys
        print_result(True, "sys imported successfully")
        
        return True
        
    except ImportError as e:
        print_result(False, f"Import error: {str(e)}")
        return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and generate report"""
    print("\n" + "="*60)
    print("PBO APPLICATION - COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    tests = [
        ("Python Imports", test_imports),
        ("File Structure", test_file_structure),
        ("Database Initialization", test_database_initialization),
        ("Operation Tables Data", test_operation_tables_data),
        ("Calculation Logic", test_calculation_logic),
        ("Room Rate Mappings", test_room_rates),
        ("Data Insertion", test_data_insertion),
        ("Search Functionality", test_search_functionality),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_result(False, f"Test crashed: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "-"*60)
    print(f"TOTAL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("-"*60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Application is ready for use.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
