#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Auto-Surgeon Price Feature
Testing the /api/get-operation-price endpoint
"""

import sys
import json

# Add parent directory to path
sys.path.insert(0, '.')

from app import app, db_helper
from models_sqlalchemy import OperationTable, TindakanItem

def test_operation_table_price():
    """Test getting price from OperationTable"""
    print("\n" + "="*60)
    print("TEST 1: Get Price from OperationTable")
    print("="*60)
    
    with app.app_context():
        # Get first operation from database
        operation = OperationTable.query.first()
        
        if operation:
            print(f"\n✓ Found Operation: {operation.kode} - {operation.nama_tindakan}")
            print(f"  Biaya Dokter: Rp {operation.biaya_dokter:,.0f}")
            print(f"  Biaya RS: Rp {operation.biaya_rs:,.0f}")
            
            # Test via db_helper
            op_data = db_helper.get_operation_by_code(operation.kode)
            if op_data:
                print(f"\n✓ Retrieved via db_helper: {op_data}")
                return True
            else:
                print("✗ Failed to retrieve via db_helper")
                return False
        else:
            print("✗ No operation found in database")
            return False

def test_tindakan_item_price():
    """Test getting price from TindakanItem"""
    print("\n" + "="*60)
    print("TEST 2: Get Price from TindakanItem")
    print("="*60)
    
    with app.app_context():
        # Get first tindakan item from database
        tindakan = TindakanItem.query.first()
        
        if tindakan:
            print(f"\n✓ Found Tindakan: {tindakan.nama_tindakan}")
            print(f"  ID: {tindakan.id}")
            print(f"  Amount: Rp {tindakan.amount:,.0f}")
            print(f"  Kelas: {tindakan.kelas}")
            print(f"  Kategory: {tindakan.kategory}")
            
            # Test via db_helper
            tindakan_data = db_helper.get_tindakan_by_id(tindakan.id)
            if tindakan_data:
                print(f"\n✓ Retrieved via db_helper: {tindakan_data}")
                return True
            else:
                print("✗ Failed to retrieve via db_helper")
                return False
        else:
            print("✗ No tindakan item found in database")
            return False

def test_api_endpoint_operation():
    """Test API endpoint with operation code"""
    print("\n" + "="*60)
    print("TEST 3: API Endpoint - OperationTable")
    print("="*60)
    
    with app.test_client() as client:
        with app.app_context():
            # Get first operation
            operation = OperationTable.query.first()
            
            if not operation:
                print("✗ No operation found in database")
                return False
            
            print(f"\nSending POST /api/get-operation-price")
            print(f"Payload: {json.dumps({'kode': operation.kode}, indent=2)}")
            
            response = client.post('/api/get-operation-price',
                                 json={'kode': operation.kode},
                                 content_type='application/json')
            
            print(f"\nResponse Status: {response.status_code}")
            data = response.get_json()
            print(f"Response Data: {json.dumps(data, indent=2)}")
            
            if data.get('success') and data.get('type') == 'operation':
                print(f"\n✓ Successfully fetched operation price: Rp {data.get('price'):,.0f}")
                return True
            else:
                print("✗ Failed to fetch operation price")
                return False

def test_api_endpoint_tindakan():
    """Test API endpoint with tindakan code"""
    print("\n" + "="*60)
    print("TEST 4: API Endpoint - TindakanItem")
    print("="*60)
    
    with app.test_client() as client:
        with app.app_context():
            # Get first tindakan item
            tindakan = TindakanItem.query.first()
            
            if not tindakan:
                print("✗ No tindakan item found in database")
                return False
            
            kode = f"TINDAKAN-{tindakan.id}"
            print(f"\nSending POST /api/get-operation-price")
            print(f"Payload: {json.dumps({'kode': kode}, indent=2)}")
            
            response = client.post('/api/get-operation-price',
                                 json={'kode': kode},
                                 content_type='application/json')
            
            print(f"\nResponse Status: {response.status_code}")
            data = response.get_json()
            print(f"Response Data: {json.dumps(data, indent=2)}")
            
            if data.get('success') and data.get('type') == 'tindakan':
                print(f"\n✓ Successfully fetched tindakan price: Rp {data.get('price'):,.0f}")
                return True
            else:
                print("✗ Failed to fetch tindakan price")
                return False

def test_api_endpoint_not_found():
    """Test API endpoint with non-existent code"""
    print("\n" + "="*60)
    print("TEST 5: API Endpoint - Not Found")
    print("="*60)
    
    with app.test_client() as client:
        kode = "NONEXISTENT-9999"
        print(f"\nSending POST /api/get-operation-price")
        print(f"Payload: {json.dumps({'kode': kode}, indent=2)}")
        
        response = client.post('/api/get-operation-price',
                             json={'kode': kode},
                             content_type='application/json')
        
        print(f"\nResponse Status: {response.status_code}")
        data = response.get_json()
        print(f"Response Data: {json.dumps(data, indent=2)}")
        
        if not data.get('success') and response.status_code == 404:
            print(f"\n✓ Correctly returned 404 for non-existent code")
            return True
        else:
            print("✗ Should return 404 for non-existent code")
            return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("AUTO-SURGEON PRICE FEATURE - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Operation Table Price", test_operation_table_price),
        ("Tindakan Item Price", test_tindakan_item_price),
        ("API Endpoint - Operation", test_api_endpoint_operation),
        ("API Endpoint - Tindakan", test_api_endpoint_tindakan),
        ("API Endpoint - Not Found", test_api_endpoint_not_found),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
