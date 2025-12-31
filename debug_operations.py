#!/usr/bin/env python
"""Debug script to check operation data in database"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import Config
from models_sqlalchemy import db, OperationTable
from models import Database
from flask import Flask

# Initialize Flask app and database
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create database context
with app.app_context():
    db_helper = Database()
    
    print("=" * 80)
    print("DEBUG: OPERASI DATABASE STATUS")
    print("=" * 80)
    
    # Count total operations
    total_ops = OperationTable.query.count()
    print(f"\n✓ Total Operasi di Database: {total_ops}")
    
    if total_ops == 0:
        print("\n❌ MASALAH: Database operasi kosong!")
        print("   Action: Upload data operasi melalui halaman Upload Database")
        sys.exit(1)
    
    # Get unique classes
    all_ops = db_helper.get_all_operations()
    unique_classes = set()
    for op in all_ops:
        if op.get('kelas'):
            unique_classes.add(op['kelas'])
    
    print(f"\n✓ Kelas Unik yang Ada: {sorted(list(unique_classes))}")
    
    # Count by class
    print("\n✓ Jumlah Operasi per Kelas:")
    for kelas in sorted(list(unique_classes)):
        ops_by_class = db_helper.get_operations_by_kelas(kelas)
        print(f"  - {kelas}: {len(ops_by_class)} operasi")
    
    # Check for operations with missing data
    print("\n✓ Verifikasi Integritas Data:")
    missing_harga = 0
    missing_kelas = 0
    valid_ops = 0
    
    for op in all_ops:
        if not op.get('kelas'):
            missing_kelas += 1
        elif op.get('biaya_dokter') == 0 and op.get('biaya_rs') == 0:
            missing_harga += 1
        else:
            valid_ops += 1
    
    print(f"  - Operasi Valid: {valid_ops}")
    print(f"  - Operasi tanpa Kelas: {missing_kelas}")
    print(f"  - Operasi tanpa Harga: {missing_harga}")
    
    if missing_kelas > 0 or missing_harga > 0:
        print("\n❌ MASALAH: Ada operasi dengan data tidak lengkap!")
        print("   Operasi tanpa kelas atau harga tidak akan tertampil di form")
    
    # Sample some operations
    print("\n✓ Sample Data Operasi (5 pertama):")
    print(f"  {'Kode':<15} {'Nama Tindakan':<30} {'Kelas':<15} {'Harga Dokter':>15} {'Harga RS':>15}")
    print(f"  {'-'*15} {'-'*30} {'-'*15} {'-'*15} {'-'*15}")
    
    for i, op in enumerate(all_ops[:5]):
        print(f"  {op['kode']:<15} {op['nama_tindakan'][:29]:<30} {op['kelas']:<15} Rp{op['biaya_dokter']:>13,.0f} Rp{op['biaya_rs']:>13,.0f}")
    
    if total_ops > 5:
        print(f"  ... dan {total_ops - 5} operasi lainnya")
    
    print("\n" + "=" * 80)
    print("REKOMENDASI:")
    print("=" * 80)
    
    if total_ops == 0:
        print("1. Upload file Excel dengan data operasi melalui halaman 'Upload Database'")
        print("2. Format Excel harus memiliki sheet 'db table operasi' dengan kolom:")
        print("   - No, Fee Operator, Kelas, Harga Operator, Harga Anestesi")
        print("3. Gunakan kelas: Basic, Standard, Deluxe, President Suite, ED, OPD, OPD Executive")
    
    elif missing_kelas > 0:
        print("1. Ada operasi yang tidak memiliki kelas")
        print("2. Hapus operasi dan re-upload data yang lengkap")
        print("3. Pastikan semua operasi memiliki kelas yang valid")
    
    elif missing_harga > 0:
        print("1. Ada operasi yang tidak memiliki harga")
        print("2. Data harga penting untuk perhitungan biaya")
        print("3. Re-upload data dengan harga yang lengkap")
    
    else:
        print("✓ Data operasi terlihat baik-baik saja!")
        print("1. Verifikasi bahwa kelas yang Anda pilih ada di database")
        print("2. Cek console browser (F12) untuk melihat response API")
        print("3. Jika masih tidak muncul, bisa ada masalah di frontend filtering")
    
    print("=" * 80)
