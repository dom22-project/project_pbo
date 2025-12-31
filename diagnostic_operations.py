#!/usr/bin/env python
"""
Diagnostic and Recovery Script for Operation Data Issues
Helps identify and fix the issue where operation prices don't appear based on selected class
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import Config
from models_sqlalchemy import db, OperationTable
from models import Database
from flask import Flask
from sqlalchemy import func

# Initialize Flask app and database
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def print_header(text):
    print("\n" + "="*80)
    print(text.center(80))
    print("="*80)

def print_section(text):
    print(f"\n{'─'*80}")
    print(f"► {text}")
    print(f"{'─'*80}")

def main():
    with app.app_context():
        db_helper = Database()
        
        print_header("DIAGNOSTIC LAPORAN: OPERASI HARGA TIDAK MUNCUL")
        
        # === CHECK 1: Database Connection ===
        print_section("1. Koneksi Database")
        try:
            db_path = Config.DATABASE_PATH
            if os.path.exists(db_path):
                print(f"✓ Database ditemukan: {db_path}")
                print(f"  Ukuran: {os.path.getsize(db_path) / 1024:.2f} KB")
            else:
                print(f"✗ Database TIDAK ditemukan: {db_path}")
                return
        except Exception as e:
            print(f"✗ Error mengecek database: {e}")
            return
        
        # === CHECK 2: Operation Table Count ===
        print_section("2. Jumlah Data di Tabel Operasi")
        try:
            total_ops = OperationTable.query.count()
            print(f"Total Operasi dalam Database: {total_ops}")
            
            if total_ops == 0:
                print("\n  ✗ MASALAH: Tabel Operasi KOSONG!")
                print("    Tidak ada data operasi yang ter-upload ke database.")
                print("    SOLUSI: Upload file Excel dengan data operasi melalui halaman 'Upload Database'")
                return
            elif total_ops < 100:
                print(f"\n  ⚠ PERINGATAN: Hanya {total_ops} operasi.")
                print("    Data mungkin tidak lengkap atau belum ter-upload semua.")
            else:
                print(f"  ✓ Data operasi terlihat cukup ({total_ops} records)")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return
        
        # === CHECK 3: Data Integrity ===
        print_section("3. Integritas Data Operasi")
        try:
            all_ops = db_helper.get_all_operations()
            
            # Count issues
            no_kode = sum(1 for op in all_ops if not op.get('kode'))
            no_kelas = sum(1 for op in all_ops if not op.get('kelas'))
            no_harga = sum(1 for op in all_ops if (op.get('biaya_dokter', 0) == 0 and op.get('biaya_rs', 0) == 0))
            
            print(f"Total operasi: {len(all_ops)}")
            print(f"  - Dengan Kode: {len(all_ops) - no_kode} ✓")
            if no_kode > 0:
                print(f"    ✗ Tanpa Kode: {no_kode}")
            
            print(f"  - Dengan Kelas: {len(all_ops) - no_kelas} ✓")
            if no_kelas > 0:
                print(f"    ✗ Tanpa Kelas: {no_kelas}")
            
            print(f"  - Dengan Harga: {len(all_ops) - no_harga} ✓")
            if no_harga > 0:
                print(f"    ✗ Tanpa Harga (0): {no_harga}")
            
            if no_kode + no_kelas + no_harga > 0:
                print("\n  ✗ MASALAH DITEMUKAN: Data tidak lengkap!")
                return
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return
        
        # === CHECK 4: Classes in Database ===
        print_section("4. Kelas yang Ada di Database")
        try:
            # Get unique classes
            class_query = db.session.query(OperationTable.kelas.distinct()).all()
            classes_in_db = [row[0] for row in class_query if row[0]]
            
            # Expected classes (dari form)
            expected_classes = [
                'basic', 'standard', 'deluxe', 'vip', 'vvip', 'suite', 
                'president suite', 'odc', 'ed', 'opd', 'opd executive'
            ]
            
            print(f"Kelas dalam Database ({len(classes_in_db)}):")
            for kelas in sorted(classes_in_db):
                count = len(db_helper.get_operations_by_kelas(kelas.title()))
                status = "✓" if kelas.lower() in expected_classes else "⚠"
                print(f"  {status} {kelas.title().ljust(20)}: {count} operasi")
            
            print(f"\nKelas yang Diharapkan di Form ({len(expected_classes)}):")
            missing = []
            for exp_class in expected_classes:
                found = any(db_class.lower() == exp_class.lower() for db_class in classes_in_db)
                status = "✓" if found else "✗"
                print(f"  {status} {exp_class.title()}")
                if not found:
                    missing.append(exp_class)
            
            if missing:
                print(f"\n  ✗ MASALAH: Kelas berikut TIDAK ada di database:")
                for m in missing:
                    print(f"    - {m.title()}")
                print("\n  Ini adalah AKAR MASALAH!")
                print("  Saat memilih kelas ini, dropdown operasi akan KOSONG.")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return
        
        # === CHECK 5: Sample Data ===
        print_section("5. Sample Data Operasi (10 pertama)")
        try:
            print(f"{'Kode':<12} {'Nama Tindakan':<30} {'Kelas':<15} {'Biaya Dokter':>15} {'Biaya RS':>15}")
            print(f"{'-'*12} {'-'*30} {'-'*15} {'-'*15} {'-'*15}")
            
            for i, op in enumerate(all_ops[:10]):
                print(f"{op['kode']:<12} {op['nama_tindakan'][:29]:<30} {op['kelas']:<15} Rp{op['biaya_dokter']:>13,.0f} Rp{op['biaya_rs']:>13,.0f}")
            
            if len(all_ops) > 10:
                print(f"... dan {len(all_ops) - 10} operasi lainnya")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        # === RECOMMENDATIONS ===
        print_section("REKOMENDASI & SOLUSI")
        
        # Check what the issue is
        if total_ops == 0:
            print("\n1. MASALAH: Database operasi KOSONG")
            print("   SOLUSI:")
            print("   a. Buka halaman 'Upload Database'")
            print("   b. Upload file Excel dengan sheet 'db table operasi'")
            print("   c. Format harus: No | Fee Operator | Kelas | Harga Operator | Harga Anestesi")
            print("   d. Gunakan kelas: Basic, Standard, Deluxe, VIP, VVIP, Suite, President Suite, ODC, ED, OPD, OPD Executive")
        
        elif no_kelas > 0:
            print("\n1. MASALAH: Ada operasi tanpa kelas")
            print("   Operasi tanpa kelas tidak akan tertampil saat memilih kelas apapun")
            print("   SOLUSI:")
            print("   a. Clean up: Hapus semua operasi dari database")
            print("   b. Re-upload file Excel dengan data operasi yang lengkap")
            print("   c. Pastikan SEMUA operasi memiliki kelas yang valid")
        
        elif missing:
            print("\n1. MASALAH UTAMA: Kelas-kelas berikut tidak ada di database:")
            for m in missing:
                print(f"   - {m.title()}")
            print("\n   Saat Anda memilih kelas-kelas ini, dropdown operasi akan KOSONG")
            print("   karena API tidak menemukan operasi dengan kelas tersebut.")
            print("\n   SOLUSI:")
            print("   a. Verifikasi file Excel Anda memiliki operasi untuk kelas-kelas ini")
            print("   b. Jika tidak, upload saja file dengan kelas yang Anda punya")
            print("   c. Sistem akan berfungsi normal untuk kelas yang ada datanya")
            print("   d. Untuk kelas tanpa data, dropdown akan tetap kosong (ini NORMAL)")
        
        elif total_ops > 0 and no_kode == 0 and no_kelas == 0 and no_harga == 0:
            print("\n✓ DATA OPERASI TERLIHAT BAIK SEMUA!")
            print("\n  Jika harga masih tidak muncul, kemungkinan:")
            print("  1. Buka Console Browser (F12) saat memilih kelas")
            print("  2. Cek apakah ada error message")
            print("  3. Cek Network tab untuk response dari /api/get-tindakan-by-kelas")
            print("  4. Verifikasi bahwa operasi ada untuk kelas yang dipilih")
        
        print("\n" + "="*80)

if __name__ == '__main__':
    main()
