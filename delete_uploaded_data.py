"""
Script untuk menghapus data yang sudah diupload dari database
Menghapus data dari:
- Table operasi (operation_tables)
- Table tindakan (tindakan_items)
- Table nama dokter (doctors)
"""

import sys
from config import Config
from models_sqlalchemy import db, OperationTable, Doctor, TindakanItem
from flask import Flask

# Create Flask app context
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def delete_uploaded_data():
    """Menghapus semua data yang diupload dari ketiga tabel"""
    with app.app_context():
        try:
            # Count before deletion
            operasi_count = OperationTable.query.count()
            tindakan_count = TindakanItem.query.count()
            dokter_count = Doctor.query.count()
            
            print("=" * 70)
            print("MENGHAPUS DATA YANG SUDAH DIUPLOAD")
            print("=" * 70)
            
            print(f"\nData sebelum penghapusan:")
            print(f"  • Table Operasi: {operasi_count} record")
            print(f"  • Table Tindakan: {tindakan_count} record")
            print(f"  • Table Nama Dokter: {dokter_count} record")
            
            # Confirmation
            print("\n" + "-" * 70)
            response = input("Yakin ingin menghapus semua data ini? (yes/no): ").strip().lower()
            
            if response != 'yes':
                print("\n✗ Operasi dibatalkan.")
                return False
            
            print("\n" + "-" * 70)
            print("Menghapus data...\n")
            
            # Delete from operation_tables
            if operasi_count > 0:
                OperationTable.query.delete()
                print(f"✓ Tabel Operasi: {operasi_count} record dihapus")
            else:
                print(f"✓ Tabel Operasi: Tidak ada data untuk dihapus")
            
            # Delete from tindakan_items
            if tindakan_count > 0:
                TindakanItem.query.delete()
                print(f"✓ Tabel Tindakan: {tindakan_count} record dihapus")
            else:
                print(f"✓ Tabel Tindakan: Tidak ada data untuk dihapus")
            
            # Delete from doctors
            if dokter_count > 0:
                Doctor.query.delete()
                print(f"✓ Tabel Nama Dokter: {dokter_count} record dihapus")
            else:
                print(f"✓ Tabel Nama Dokter: Tidak ada data untuk dihapus")
            
            # Commit changes
            db.session.commit()
            
            # Verify deletion
            print("\n" + "-" * 70)
            print("Verifikasi data setelah penghapusan:")
            print(f"  • Table Operasi: {OperationTable.query.count()} record")
            print(f"  • Table Tindakan: {TindakanItem.query.count()} record")
            print(f"  • Table Nama Dokter: {Doctor.query.count()} record")
            
            print("\n" + "=" * 70)
            print("✓ SEMUA DATA BERHASIL DIHAPUS")
            print("=" * 70)
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ ERROR: {str(e)}")
            print("Operasi dibatalkan - tidak ada data yang dihapus")
            return False

if __name__ == '__main__':
    delete_uploaded_data()
