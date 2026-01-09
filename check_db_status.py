"""
Script untuk check database counts dan operations dengan detail
"""

import sys
sys.path.insert(0, '.')

from app import app, db_helper
from models_sqlalchemy import OperationTable, Doctor, TindakanItem

with app.app_context():
    ops = OperationTable.query.all()
    docs = Doctor.query.all()
    tind = TindakanItem.query.all()
    
    print("=" * 80)
    print("DATABASE STATUS")
    print("=" * 80)
    print(f"\nOperations: {len(ops)}")
    if len(ops) <= 10:
        for op in ops:
            print(f"  - {op.kode}: {op.nama_tindakan} ({op.kelas})")
    else:
        for op in ops[:5]:
            print(f"  - {op.kode}: {op.nama_tindakan} ({op.kelas})")
        print(f"  ... and {len(ops) - 5} more")
    
    print(f"\nDoctors: {len(docs)}")
    if len(docs) <= 10:
        for doc in docs:
            print(f"  - {doc.nama_dokter}")
    else:
        for doc in docs[:5]:
            print(f"  - {doc.nama_dokter}")
        print(f"  ... and {len(docs) - 5} more")
    
    print(f"\nTindakan: {len(tind)}")
    if len(tind) <= 10:
        for t in tind:
            print(f"  - {t.nama_tindakan} ({t.kelas})")
    else:
        for t in tind[:5]:
            print(f"  - {t.nama_tindakan} ({t.kelas})")
        print(f"  ... and {len(tind) - 5} more")
    
    print("\n" + "=" * 80)
