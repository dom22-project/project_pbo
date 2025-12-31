#!/usr/bin/env python
"""
Debug script untuk melihat detail duplikasi kelas dan operasi yang sesuai per kelas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import Config
from models_sqlalchemy import db, OperationTable
from models import Database
from flask import Flask
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def main():
    with app.app_context():
        db_helper = Database()
        
        print("\n" + "="*80)
        print("DEBUG: CEK DUPLIKASI KELAS")
        print("="*80)
        
        # Get raw kelas values
        print("\nKelas UNIK (tanpa uppercase/lowercase):")
        kelas_values = db.session.query(OperationTable.kelas.distinct()).all()
        kelas_list = [row[0] for row in kelas_values if row[0]]
        
        for kelas in sorted(kelas_list):
            count = OperationTable.query.filter_by(kelas=kelas).count()
            print(f"  '{kelas}' -> {count} operasi")
        
        # Test API filtering dengan berbagai case
        print("\n" + "="*80)
        print("TEST: API Filtering untuk setiap kelas")
        print("="*80)
        
        test_cases = [
            ('Basic', 'Case 1'),
            ('basic', 'Lowercase'),
            ('BASIC', 'Uppercase'),
            ('Standard', 'Case 1'),
            ('standard', 'Lowercase'),
            ('STANDARD', 'Uppercase'),
            ('Deluxe', 'Case 1'),
            ('President Suite', 'Case 1'),
            ('ED', 'Case 1'),
            ('ed', 'Lowercase'),
            ('OPD', 'Case 1'),
            ('OPD Executive', 'Case 1'),
        ]
        
        for kelas, desc in test_cases:
            ops = db_helper.get_operations_by_kelas(kelas)
            status = f"✓ {len(ops):4d} operasi" if ops else "✗ 0 operasi (EMPTY!)"
            print(f"  {kelas.ljust(20)}: {status.ljust(25)} [{desc}]")
        
        # Check if any kelas have leading/trailing spaces
        print("\n" + "="*80)
        print("CHECK: Kelas dengan spasi leading/trailing")
        print("="*80)
        
        suspect_classes = db.session.query(
            OperationTable.kelas, 
            func.count(OperationTable.id).label('count')
        ).filter(
            (OperationTable.kelas.like(' %')) | 
            (OperationTable.kelas.like('% '))
        ).group_by(OperationTable.kelas).all()
        
        if suspect_classes:
            print("  ✗ DITEMUKAN kelas dengan spasi!")
            for kelas, count in suspect_classes:
                print(f"    '{kelas}' → {count} operasi")
        else:
            print("  ✓ Tidak ada kelas dengan spasi leading/trailing")
        
        # Check form dropdown kelas vs database
        print("\n" + "="*80)
        print("CHECK: Form Dropdown Kelas vs Database")
        print("="*80)
        
        form_classes = [
            'Basic', 'Standard', 'Deluxe', 'VIP', 'VVIP', 'Suite',
            'President Suite', 'ODC', 'ED', 'OPD', 'OPD Executive'
        ]
        
        kelas_db = [row[0] for row in kelas_values if row[0]]
        
        print("\nForm Dropdown:")
        for fc in form_classes:
            found = any(fc.lower() == kc.lower() for kc in kelas_db)
            status = "✓" if found else "✗"
            count = len(db_helper.get_operations_by_kelas(fc)) if found else 0
            print(f"  {status} {fc.ljust(20)}: {count} operasi")
        
        print("\n" + "="*80)
        print("REKOMENDASI")
        print("="*80)
        
        # Determine what the issue is
        duplicates = len(kelas_list) != len(form_classes)
        
        if duplicates:
            print("\n⚠ Ditemukan duplikasi atau data inkonsisten di database")
            print("  Solusi: Clean up duplikasi dan standardize kelas format")
            print("  Jalankan: python fix_class_duplicates.py")
        else:
            print("\n✓ Format kelas terlihat konsisten")
            print("  Jika harga masih tidak muncul, issue ada di frontend/browser")
            print("  Cek: Buka Console Browser (F12) saat memilih kelas")

if __name__ == '__main__':
    main()
