"""
Test script to verify CITO and Penyulit surcharge calculation
"""

from config import Config
from models import Database

class MockDatabase:
    """Mock database for testing"""
    def get_operation_by_code(self, kode):
        # Return sample operation data
        return {
            'kode': kode,
            'nama_tindakan': 'Sample Operation',
            'biaya_dokter': 1000000,  # 1 juta
            'biaya_rs': 500000,        # 500 ribu
            'total_biaya': 1500000
        }

def test_surcharge_calculation():
    """Test surcharge calculation for different operation types"""
    from utils import PBOCalculator
    
    # Create mock database
    mock_db = MockDatabase()
    
    # Test data: single operation with 100% percentage
    operations_data = [
        {
            'kode': '4199999994',
            'persentase': 100  # 100%
        }
    ]
    
    # Base fees (without surcharge)
    base_surgeon = 1000000  # biaya_dokter
    base_anesthesi = 500000  # biaya_rs
    
    print("=" * 60)
    print("SURCHARGE CALCULATION TEST")
    print("=" * 60)
    print(f"\nBase Surgeon Fee (Elektif): Rp {base_surgeon:,.0f}")
    print(f"Base Anesthesi Fee: Rp {base_anesthesi:,.0f}")
    
    # Test 1: Elektif / Tentative (no surcharge)
    result_elektif = PBOCalculator.calculate_surgery_fees(
        operations_data, 
        'Elektif / Tentative', 
        mock_db
    )
    
    print(f"\n{'─' * 60}")
    print("1. ELEKTIF / TENTATIVE (Surcharge: 1.0x / 0%)")
    print(f"{'─' * 60}")
    print(f"   Surgeon Fee: Rp {result_elektif['surgeon']:,.0f}")
    print(f"   Anesthesi Fee: Rp {result_elektif['anesthesi']:,.0f}")
    print(f"   OT Room Charge (30%): Rp {result_elektif['ot_room_charge']:,.0f}")
    
    # Verify calculation
    expected_surgeon_elektif = base_surgeon * 1.0
    expected_anesthesi_elektif = base_anesthesi * 1.0
    assert result_elektif['surgeon'] == int(expected_surgeon_elektif), f"Elektif surgeon fee mismatch"
    assert result_elektif['anesthesi'] == int(expected_anesthesi_elektif), f"Elektif anesthesi fee mismatch"
    print("   ✓ Calculation verified")
    
    # Test 2: CITO (25% surcharge = 1.25x)
    result_cito = PBOCalculator.calculate_surgery_fees(
        operations_data, 
        'CITO', 
        mock_db
    )
    
    print(f"\n{'─' * 60}")
    print("2. CITO (Surcharge: 1.25x / +25%)")
    print(f"{'─' * 60}")
    print(f"   Surgeon Fee: Rp {result_cito['surgeon']:,.0f}")
    print(f"   Anesthesi Fee: Rp {result_cito['anesthesi']:,.0f}")
    print(f"   OT Room Charge (30%): Rp {result_cito['ot_room_charge']:,.0f}")
    
    # Verify calculation
    expected_surgeon_cito = base_surgeon * 1.25
    expected_anesthesi_cito = base_anesthesi * 1.25
    expected_ot_cito = expected_surgeon_cito * 0.30
    
    print(f"\n   Expected Surgeon Fee: Rp {expected_surgeon_cito:,.0f}")
    print(f"   (+25% = Rp {base_surgeon * 0.25:,.0f})")
    print(f"   Difference: Rp {result_cito['surgeon'] - result_elektif['surgeon']:,.0f}")
    
    assert result_cito['surgeon'] == int(expected_surgeon_cito), f"CITO surgeon fee mismatch"
    assert result_cito['anesthesi'] == int(expected_anesthesi_cito), f"CITO anesthesi fee mismatch"
    assert result_cito['ot_room_charge'] == int(expected_ot_cito), f"CITO OT room charge mismatch"
    print("   ✓ Calculation verified")
    
    # Test 3: Penyulit (30% surcharge = 1.30x)
    result_penyulit = PBOCalculator.calculate_surgery_fees(
        operations_data, 
        'Penyulit', 
        mock_db
    )
    
    print(f"\n{'─' * 60}")
    print("3. PENYULIT (Surcharge: 1.30x / +30%)")
    print(f"{'─' * 60}")
    print(f"   Surgeon Fee: Rp {result_penyulit['surgeon']:,.0f}")
    print(f"   Anesthesi Fee: Rp {result_penyulit['anesthesi']:,.0f}")
    print(f"   OT Room Charge (30%): Rp {result_penyulit['ot_room_charge']:,.0f}")
    
    # Verify calculation
    expected_surgeon_penyulit = base_surgeon * 1.30
    expected_anesthesi_penyulit = base_anesthesi * 1.30
    expected_ot_penyulit = expected_surgeon_penyulit * 0.30
    
    print(f"\n   Expected Surgeon Fee: Rp {expected_surgeon_penyulit:,.0f}")
    print(f"   (+30% = Rp {base_surgeon * 0.30:,.0f})")
    print(f"   Difference from Elektif: Rp {result_penyulit['surgeon'] - result_elektif['surgeon']:,.0f}")
    
    assert result_penyulit['surgeon'] == int(expected_surgeon_penyulit), f"Penyulit surgeon fee mismatch"
    assert result_penyulit['anesthesi'] == int(expected_anesthesi_penyulit), f"Penyulit anesthesi fee mismatch"
    assert result_penyulit['ot_room_charge'] == int(expected_ot_penyulit), f"Penyulit OT room charge mismatch"
    print("   ✓ Calculation verified")
    
    # Comparison summary
    print(f"\n{'=' * 60}")
    print("SUMMARY - SURGEON FEE COMPARISON")
    print(f"{'=' * 60}")
    print(f"Elektif / Tentative: Rp {result_elektif['surgeon']:>15,.0f}")
    print(f"CITO (+25%):         Rp {result_cito['surgeon']:>15,.0f} ({result_cito['surgeon'] - result_elektif['surgeon']:+,.0f})")
    print(f"Penyulit (+30%):     Rp {result_penyulit['surgeon']:>15,.0f} ({result_penyulit['surgeon'] - result_elektif['surgeon']:+,.0f})")
    
    print(f"\n{'=' * 60}")
    print("SUMMARY - ANESTHESI FEE COMPARISON")
    print(f"{'=' * 60}")
    print(f"Elektif / Tentative: Rp {result_elektif['anesthesi']:>15,.0f}")
    print(f"CITO (+25%):         Rp {result_cito['anesthesi']:>15,.0f} ({result_cito['anesthesi'] - result_elektif['anesthesi']:+,.0f})")
    print(f"Penyulit (+30%):     Rp {result_penyulit['anesthesi']:>15,.0f} ({result_penyulit['anesthesi'] - result_elektif['anesthesi']:+,.0f})")
    
    print("\n✅ ALL TESTS PASSED!")
    print("Surcharge calculation is working correctly!")

if __name__ == '__main__':
    test_surcharge_calculation()
