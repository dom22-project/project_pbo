import requests

print("=" * 60)
print("Testing Tindakan Tambahan Removal")
print("=" * 60)

# Test 1: Check if input page loads
print("\n1. Testing /input page...")
try:
    response = requests.get('http://127.0.0.1:5000/input')
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✓ Page loads successfully")
        
        # Check if "Tindakan Tambahan" is removed
        if "Tindakan Tambahan" in response.text:
            print("   ✗ ERROR: 'Tindakan Tambahan' still found in page!")
        else:
            print("   ✓ 'Tindakan Tambahan' successfully removed from page")
        
        # Check if essential elements are present
        if "Tabel Operasi" in response.text:
            print("   ✓ 'Tabel Operasi' section present")
        if "Rincian Biaya" in response.text:
            print("   ✓ 'Rincian Biaya' section present")
        if "Input Data PBO" in response.text:
            print("   ✓ Page title correct")
    else:
        print(f"   ✗ ERROR: Page returned status {response.status_code}")
except Exception as e:
    print(f"   ✗ ERROR: {str(e)}")

# Test 2: Check if removed API endpoint returns 404
print("\n2. Testing removed API endpoint...")
try:
    response = requests.post('http://127.0.0.1:5000/api/get-tindakan-by-kelas',
                            json={'kelas': 'VIP'})
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 404:
        print("   ✓ API endpoint successfully removed (404)")
    else:
        print(f"   ✗ ERROR: Expected 404, got {response.status_code}")
except Exception as e:
    print(f"   ✗ ERROR: {str(e)}")

# Test 3: Check if other API endpoints still work
print("\n3. Testing remaining API endpoints...")
try:
    # Test get-room-rate
    response = requests.post('http://127.0.0.1:5000/api/get-room-rate',
                            json={'kelas': 'VIP'})
    print(f"   /api/get-room-rate: {response.status_code}")
    if response.status_code == 200:
        print("   ✓ get-room-rate endpoint works")
    
    # Test calculate-total
    response = requests.post('http://127.0.0.1:5000/api/calculate-total',
                            json={'surgeon': 1000000, 'anesthesi': 500000})
    print(f"   /api/calculate-total: {response.status_code}")
    if response.status_code == 200:
        print("   ✓ calculate-total endpoint works")
        
except Exception as e:
    print(f"   ✗ ERROR: {str(e)}")

print("\n" + "=" * 60)
print("Testing Complete!")
print("=" * 60)
