#!/usr/bin/env python
"""
Fix script: Standardize kelas naming dan hapus duplikasi
Mengubah semua kelas menjadi format PascalCase yang konsisten
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import Config
from models_sqlalchemy import db, OperationTable
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Mapping dari kelas lama ke kelas baru yang standar
KELAS_MAPPING = {
    'BASIC': 'Basic',
    'basic': 'Basic',
    'STANDARD': 'Standard',
    'standard': 'Standard',
    'DELUXE': 'Deluxe',
    'deluxe': 'Deluxe',
    'VIP': 'VIP',
    'vip': 'VIP',
    'VVIP': 'VVIP',
    'vvip': 'VVIP',
    'SUITE': 'Suite',
    'suite': 'Suite',
    'PRESIDENT SUITE': 'President Suite',
    'president suite': 'President Suite',
    'ODC': 'ODC',
    'odc': 'ODC',
    'ED': 'ED',
    'ed': 'ED',
    'OPD': 'OPD',
    'opd': 'OPD',
    'OPD EXECUTIVE': 'OPD Executive',
    'opd executive': 'OPD Executive',
}

def fix_class_duplicates():
    with app.app_context():
        print("\n" + "="*80)
        print("FIX: Standardize Kelas dan Hapus Duplikasi")
        print("="*80)
        
        print("\n1. Scanning database untuk kelas yang perlu diperbaiki...")
        
        # Get all operations grouped by current kelas value
        current_classes = db.session.query(OperationTable.kelas.distinct()).filter(
            OperationTable.kelas.isnot(None)
        ).all()
        
        total_fixed = 0
        
        for (kelas,) in current_classes:
            if kelas in KELAS_MAPPING:
                new_kelas = KELAS_MAPPING[kelas]
                if kelas != new_kelas:
                    # Count how many need to be updated
                    count = OperationTable.query.filter_by(kelas=kelas).count()
                    
                    print(f"\n   Updating '{kelas}' → '{new_kelas}' ({count} operasi)")
                    
                    # Update all operations with old kelas to new kelas
                    OperationTable.query.filter_by(kelas=kelas).update({
                        OperationTable.kelas: new_kelas
                    })
                    
                    total_fixed += count
                    db.session.commit()
                    print(f"   ✓ Berhasil diupdate")
        
        print(f"\n2. Total operasi yang diperbaiki: {total_fixed}")
        
        # Verify result
        print("\n3. Verifikasi hasil perbaikan...")
        print("\n   Kelas setelah perbaikan:")
        
        final_classes = db.session.query(
            OperationTable.kelas,
            db.func.count(OperationTable.id).label('count')
        ).filter(
            OperationTable.kelas.isnot(None)
        ).group_by(OperationTable.kelas).order_by(OperationTable.kelas).all()
        
        for kelas, count in final_classes:
            print(f"   ✓ {kelas.ljust(20)}: {count} operasi")
        
        print("\n" + "="*80)
        print("✓ PERBAIKAN SELESAI!")
        print("="*80)
        print("\nPerubahan yang telah dibuat:")
        print("- Semua kelas sudah distandarkan ke format PascalCase")
        print("- Duplikasi kelas sudah dihilangkan")
        print("- Sekarang aplikasi akan menampilkan harga dengan benar")
        print("\nSelanjutnya:")
        print("1. Refresh aplikasi browser Anda (F5)")
        print("2. Pilih kelas kamar di form Input PBO")
        print("3. Harga operasi seharusnya sudah muncul dengan benar")

if __name__ == '__main__':
    try:
        fix_class_duplicates()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
