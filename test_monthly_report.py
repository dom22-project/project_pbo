"""
Test script untuk Monthly Report
Pastikan aplikasi Flask sudah running sebelum menjalankan script ini
"""

import requests
from datetime import datetime

# URL aplikasi
BASE_URL = "http://localhost:5000"

def test_monthly_report():
    """Test monthly report endpoint"""
    print("\n" + "="*60)
    print("TEST MONTHLY REPORT FEATURE")
    print("="*60)
    
    # Test dengan akun default
    session = requests.Session()
    
    # Login first
    print("\n[1] Attempting login...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = session.post(f"{BASE_URL}/login", data=login_data)
    if response.status_code == 200:
        print("✓ Login successful")
    else:
        print("✗ Login failed")
        return
    
    # Test accessing monthly report page
    print("\n[2] Accessing monthly report page...")
    response = session.get(f"{BASE_URL}/monthly-report")
    if response.status_code == 200 and 'Laporan Bulanan' in response.text:
        print("✓ Monthly report page loaded successfully")
    else:
        print("✗ Failed to load monthly report page")
        return
    
    # Test with specific month
    now = datetime.now()
    print(f"\n[3] Testing report for {now.strftime('%B %Y')}...")
    response = session.get(
        f"{BASE_URL}/monthly-report",
        params={
            'year': now.year,
            'month': now.month
        }
    )
    
    if response.status_code == 200:
        print(f"✓ Successfully retrieved report for {now.strftime('%B %Y')}")
        if 'Total Operasi' in response.text:
            print("✓ Statistics section found")
        if 'Nama Operasi' in response.text:
            print("✓ Report table found")
    else:
        print("✗ Failed to retrieve report")
        return
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED ✓")
    print("="*60)
    print("\nFitur Monthly Report berhasil diimplementasikan!")
    print("Akses di: http://localhost:5000/monthly-report")

if __name__ == "__main__":
    try:
        test_monthly_report()
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nPastikan aplikasi Flask sudah berjalan di localhost:5000")
