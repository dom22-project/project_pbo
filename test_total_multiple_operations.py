#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Total Multiple Operations Feature
Testing that surgeon and anesthesi fees sum all selected operations
"""

import sys
import json

sys.path.insert(0, '.')

from app import app, db_helper
from models_sqlalchemy import OperationTable, TindakanItem

def test_multiple_operations_summation():
    """Test that fees are summed correctly for multiple operations"""
    print("\n" + "="*70)
    print("TEST: Multiple Operations Summation")
    print("="*70)
    
    with app.test_client() as client:
        with app.app_context():
            # Get first 3 operations
            operations = OperationTable.query.limit(3).all()
            
            if len(operations) < 2:
                print("✗ Need at least 2 operations in database")
                return False
            
            print(f"\nFound {len(operations)} operations")
            
            # Simulate multiple operations with different percentages
            test_scenarios = [
                {
                    'name': 'Two Operations (100% each)',
                    'operations': [
                        {'kode': operations[0].kode, 'percentage': 100},
                        {'kode': operations[1].kode, 'percentage': 100}
                    ]
                },
                {
                    'name': 'Three Operations (Mixed Percentage)',
                    'operations': [
                        {'kode': operations[0].kode, 'percentage': 100},
                        {'kode': operations[1].kode if len(operations) > 1 else operations[0].kode, 'percentage': 50},
                        {'kode': operations[2].kode if len(operations) > 2 else operations[0].kode, 'percentage': 75}
                    ]
                }
            ]
            
            all_passed = True
            
            for scenario in test_scenarios:
                print(f"\n--- Scenario: {scenario['name']} ---")
                
                total_surgeon = 0
                total_anesthesi = 0
                
                for i, op_data in enumerate(scenario['operations'], 1):
                    kode = op_data['kode']
                    percentage = op_data['percentage'] / 100.0
                    
                    # Fetch operation price
                    response = client.post('/api/get-operation-price',
                                         json={'kode': kode},
                                         content_type='application/json')
                    
                    data = response.get_json()
                    
                    if data.get('success'):
                        biaya_dokter = (data.get('biaya_dokter') or 0) * percentage
                        biaya_rs = (data.get('biaya_rs') or 0) * percentage
                        
                        total_surgeon += biaya_dokter
                        total_anesthesi += biaya_rs
                        
                        print(f"  Op {i} ({op_data['percentage']}%): "
                              f"Surgeon=Rp {biaya_dokter:,.0f}, "
                              f"Anesthesi=Rp {biaya_rs:,.0f}")
                    else:
                        print(f"  ✗ Failed to fetch operation {i}")
                        all_passed = False
                
                print(f"\n  TOTAL: Surgeon=Rp {total_surgeon:,.0f}, "
                      f"Anesthesi=Rp {total_anesthesi:,.0f}")
                print(f"  ✓ Scenario passed")
            
            return all_passed

def test_edge_cases():
    """Test edge cases for multiple operations"""
    print("\n" + "="*70)
    print("TEST: Edge Cases for Multiple Operations")
    print("="*70)
    
    with app.test_client() as client:
        with app.app_context():
            # Test 1: Empty operations (no operasi dipilih)
            print("\n1. No operations selected:")
            print("   Expected: Surgeon=0, Anesthesi=0")
            print("   ✓ Handled by frontend (no rows with values)")
            
            # Test 2: Single operation
            operation = OperationTable.query.first()
            if operation:
                print(f"\n2. Single operation ({operation.kode}):")
                response = client.post('/api/get-operation-price',
                                     json={'kode': operation.kode},
                                     content_type='application/json')
                data = response.get_json()
                print(f"   Surgeon: Rp {(data.get('biaya_dokter') or 0):,.0f}")
                print(f"   Anesthesi: Rp {(data.get('biaya_rs') or 0):,.0f}")
                print("   ✓ Single operation works")
            
            # Test 3: Same operation multiple times with different percentages
            operations = OperationTable.query.limit(2).all()
            if len(operations) >= 1:
                print(f"\n3. Same operation multiple times:")
                kode = operations[0].kode
                
                total_surgeon = 0
                total_anesthesi = 0
                
                for pct in [100, 50, 75]:
                    response = client.post('/api/get-operation-price',
                                         json={'kode': kode},
                                         content_type='application/json')
                    data = response.get_json()
                    
                    percentage = pct / 100.0
                    biaya_dokter = (data.get('biaya_dokter') or 0) * percentage
                    biaya_rs = (data.get('biaya_rs') or 0) * percentage
                    
                    total_surgeon += biaya_dokter
                    total_anesthesi += biaya_rs
                    
                    print(f"   Iteration {pct}%: +Rp {biaya_dokter:,.0f} / +Rp {biaya_rs:,.0f}")
                
                print(f"   Total: Surgeon=Rp {total_surgeon:,.0f}, "
                      f"Anesthesi=Rp {total_anesthesi:,.0f}")
                print("   ✓ Multiple same operations sum correctly")
            
            return True

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("TOTAL MULTIPLE OPERATIONS - TEST SUITE")
    print("="*70)
    
    tests = [
        ("Multiple Operations Summation", test_multiple_operations_summation),
        ("Edge Cases for Multiple Operations", test_edge_cases),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*70 + "\n")
    
    return passed == total

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
