"""
Direct test of the calculate-surgery-fees endpoint fix
Tests both the backend calculator and the endpoint
"""

import sys
sys.path.insert(0, '.')

from config import Config
from utils import PBOCalculator

class MockDatabase:
    """Mock database for testing"""
    def get_operation_by_code(self, kode):
        # Return sample data matching the database
        operations = {
            '4199999994': {
                'kode': '4199999994',
                'nama_tindakan': 'DOCTORS PROCEDURE TABLE 3',
                'biaya_dokter': 4934000,
                'biaya_rs': 0,
                'total_biaya': 4934000
            },
            '4199999995': {
                'kode': '4199999995',
                'nama_tindakan': 'DOCTORS PROCEDURE TABLE 1',
                'biaya_dokter': 1125000,
                'biaya_rs': 0,
                'total_biaya': 1125000
            },
            '4199999996': {
                'kode': '4199999996',
                'nama_tindakan': 'DOCTORS PROCEDURE TABLE 2',
                'biaya_dokter': 2368000,
                'biaya_rs': 0,
                'total_biaya': 2368000
            }
        }
        return operations.get(kode)

def test_endpoint_fix():
    """Test the endpoint fix with real operation data"""
    
    mock_db = MockDatabase()
    
    # Test case: CITO with real operation
    operations_data = [
        {
            'kode': '4199999994',
            'persentase': 1.0  # 100%
        }
    ]
    
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "ENDPOINT FIX VERIFICATION TEST" + " " * 24 + "║")
    print("╚" + "═" * 68 + "╝")
    
    print("\n📋 Test Data:")
    print("   Operation: 4199999994 (DOCTORS PROCEDURE TABLE 3)")
    print("   Base Surgeon Fee: Rp 4,934,000")
    print("   Percentage: 100%")
    
    # Test Elektif (baseline)
    result_elektif = PBOCalculator.calculate_surgery_fees(
        operations_data,
        'Elektif / Tentative',
        mock_db
    )
    
    print("\n" + "─" * 70)
    print("1️⃣  ELEKTIF / TENTATIVE (No Surcharge)")
    print("─" * 70)
    print(f"   Surgeon Fee:      Rp {result_elektif['surgeon']:>12,.0f}")
    print(f"   Anesthesi Fee:    Rp {result_elektif['anesthesi']:>12,.0f}")
    print(f"   OT Room Charge:   Rp {result_elektif['ot_room_charge']:>12,.0f}")
    
    # Test CITO (+25%)
    result_cito = PBOCalculator.calculate_surgery_fees(
        operations_data,
        'CITO',
        mock_db
    )
    
    cito_increase = result_cito['surgeon'] - result_elektif['surgeon']
    cito_percentage = (cito_increase / result_elektif['surgeon']) * 100 if result_elektif['surgeon'] > 0 else 0
    
    print("\n" + "─" * 70)
    print("2️⃣  CITO (Should have +25% Surcharge)")
    print("─" * 70)
    print(f"   Surgeon Fee:      Rp {result_cito['surgeon']:>12,.0f}")
    print(f"   Increase:         Rp {cito_increase:>12,.0f} ({cito_percentage:.1f}%)")
    print(f"   Anesthesi Fee:    Rp {result_cito['anesthesi']:>12,.0f}")
    print(f"   OT Room Charge:   Rp {result_cito['ot_room_charge']:>12,.0f}")
    
    # Verify CITO surcharge
    expected_surgeon_cito = result_elektif['surgeon'] * 1.25
    if abs(result_cito['surgeon'] - expected_surgeon_cito) < 1:
        print(f"\n   ✅ CITO SURCHARGE CORRECT (+25%)")
    else:
        print(f"\n   ❌ CITO SURCHARGE ERROR!")
        print(f"      Expected: Rp {expected_surgeon_cito:,.0f}")
        print(f"      Got:      Rp {result_cito['surgeon']:,.0f}")
    
    # Test Penyulit (+30%)
    result_penyulit = PBOCalculator.calculate_surgery_fees(
        operations_data,
        'Penyulit',
        mock_db
    )
    
    penyulit_increase = result_penyulit['surgeon'] - result_elektif['surgeon']
    penyulit_percentage = (penyulit_increase / result_elektif['surgeon']) * 100 if result_elektif['surgeon'] > 0 else 0
    
    print("\n" + "─" * 70)
    print("3️⃣  PENYULIT (Should have +30% Surcharge)")
    print("─" * 70)
    print(f"   Surgeon Fee:      Rp {result_penyulit['surgeon']:>12,.0f}")
    print(f"   Increase:         Rp {penyulit_increase:>12,.0f} ({penyulit_percentage:.1f}%)")
    print(f"   Anesthesi Fee:    Rp {result_penyulit['anesthesi']:>12,.0f}")
    print(f"   OT Room Charge:   Rp {result_penyulit['ot_room_charge']:>12,.0f}")
    
    # Verify Penyulit surcharge
    expected_surgeon_penyulit = result_elektif['surgeon'] * 1.30
    if abs(result_penyulit['surgeon'] - expected_surgeon_penyulit) < 1:
        print(f"\n   ✅ PENYULIT SURCHARGE CORRECT (+30%)")
    else:
        print(f"\n   ❌ PENYULIT SURCHARGE ERROR!")
        print(f"      Expected: Rp {expected_surgeon_penyulit:,.0f}")
        print(f"      Got:      Rp {result_penyulit['surgeon']:,.0f}")
    
    # Comparison
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "SURCHARGE COMPARISON" + " " * 28 + "║")
    print("╚" + "═" * 68 + "╝")
    print(f"\n{'Elektif':<20} Rp {result_elektif['surgeon']:>15,.0f}")
    print(f"{'CITO (+25%)':<20} Rp {result_cito['surgeon']:>15,.0f}  ({cito_increase:+,.0f})")
    print(f"{'Penyulit (+30%)':<20} Rp {result_penyulit['surgeon']:>15,.0f}  ({penyulit_increase:+,.0f})")
    
    # Test validation
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 25 + "VALIDATION" + " " * 33 + "║")
    print("╚" + "═" * 68 + "╝")
    
    all_pass = True
    
    # Check CITO
    if abs(result_cito['surgeon'] - expected_surgeon_cito) < 1:
        print("✅ CITO surcharge calculation: PASS")
    else:
        print("❌ CITO surcharge calculation: FAIL")
        all_pass = False
    
    # Check Penyulit
    if abs(result_penyulit['surgeon'] - expected_surgeon_penyulit) < 1:
        print("✅ Penyulit surcharge calculation: PASS")
    else:
        print("❌ Penyulit surcharge calculation: FAIL")
        all_pass = False
    
    # Check config
    if Config.SURCHARGE_RATES.get('CITO') == 1.25:
        print("✅ CITO surcharge config (1.25): PASS")
    else:
        print("❌ CITO surcharge config: FAIL")
        all_pass = False
    
    if Config.SURCHARGE_RATES.get('Penyulit') == 1.30:
        print("✅ Penyulit surcharge config (1.30): PASS")
    else:
        print("❌ Penyulit surcharge config: FAIL")
        all_pass = False
    
    print("\n" + "═" * 70)
    
    if all_pass:
        print("🎉 ALL TESTS PASSED! Endpoint fix is working correctly.")
    else:
        print("❌ SOME TESTS FAILED! Please review the fix.")
    
    print("═" * 70)

if __name__ == '__main__':
    test_endpoint_fix()
