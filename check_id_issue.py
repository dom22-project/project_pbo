#!/usr/bin/env python
"""Check for ID=0 issue in database"""
from models_sqlalchemy import db, PBOData
from app import app

with app.app_context():
    # Check for ID = 0
    pbo_zero = PBOData.query.filter_by(id=0).first()
    if pbo_zero:
        print(f'Found PBOData with ID=0: {pbo_zero}')
        print(f'Nama Pasien: {pbo_zero.nama_pasien}')
    else:
        print('No data with ID=0 found')
    
    # Check max ID
    max_id = db.session.query(db.func.max(PBOData.id)).scalar()
    print(f'Max ID in database: {max_id}')
    
    # Check all IDs
    all_ids = db.session.query(PBOData.id).order_by(PBOData.id).all()
    print(f'All IDs in database: {[r[0] for r in all_ids]}')