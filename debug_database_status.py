"""
Debug script untuk cek data di database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db_helper

with app.app_context():
    print("="*60)
    print("DATABASE STATUS")
    print("="*60)
    
    # Check operations
    all_ops = db_helper.get_all_operations()
    print(f"\nTotal Operations: {len(all_ops)}")
    if len(all_ops) > 0:
        print(f"First 5 operations:")
        for op in all_ops[:5]:
            print(f"  Kode: {op['kode']}, Nama: {op['nama_tindakan']}, Kelas: {op['kelas']}")
    
    # Check doctors
    all_docs = db_helper.get_all_doctors()
    print(f"\nTotal Doctors: {len(all_docs)}")
    if len(all_docs) > 0:
        print(f"First 5 doctors:")
        for doc in all_docs[:5]:
            print(f"  {doc['nama_dokter']}")
    
    # Check tindakan
    try:
        all_tindakan = db_helper.get_all_tindakan_items()
        print(f"\nTotal Tindakan Items: {len(all_tindakan)}")
        if len(all_tindakan) > 0:
            print(f"First 5 tindakan:")
            for tind in all_tindakan[:5]:
                print(f"  {tind['nama_tindakan']} ({tind['kelas']})")
    except Exception as e:
        print(f"Error checking tindakan: {e}")
    
    print("\n" + "="*60)
    print("OPTIONS:")
    print("="*60)
    print("1. Keep existing data")
    print("2. Clear operations before import")
    print("3. Clear doctors before import")
    print("4. Clear all before import")
