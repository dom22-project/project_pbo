import os
from datetime import datetime
from config import Config
from models_sqlalchemy import db, PBOData, OperationTable, Doctor, TindakanItem, PaketTindakan, User

class Database:
    """Database helper class for PBO application using SQLAlchemy ORM"""
    
    def __init__(self):
        # Database configuration is now handled in Config class
        pass
    
    # PBO Data Operations
    def create_pbo(self, data):
        """Create new PBO record"""
        pbo = PBOData(
            diagnosa=data[0], nama_operasi=data[1], sifat_operasi=data[2],
            nama_dokter=data[3], kelas=data[4], tabel_operasi1=data[5],
            tabel_operasi2=data[6], tabel_operasi3=data[7], tabel_operasi4=data[8],
            persentase_operasi1=data[9], persentase_operasi2=data[10],
            persentase_operasi3=data[11], persentase_operasi4=data[12],
            konsultasi_pre_tindakan=data[13], diagnostic_pre_tindakan=data[14],
            surgeon=data[15], anesthesi=data[16], ot_room_charge=data[17],
            recovery_room_charge=data[18], alat=data[19], diagnostic=data[20],
            medical_equipment=data[21], obat_dan_alkes=data[22], tarif_kamar=data[23],
            total=data[24], catatan=data[25], keterangan=data[26],
            tanggal=datetime.strptime(data[27], '%Y-%m-%d').date() if data[27] else None,
            nama_pasien=data[28], hubungan_dengan_pasien=data[29],
            petugas_front_office=data[30], perusahaan_asuransi=data[31]
        )
        db.session.add(pbo)
        db.session.commit()
        return pbo.id
    
    def get_pbo_by_id(self, pbo_id):
        """Get PBO record by ID"""
        pbo = PBOData.query.get(pbo_id)
        return pbo.to_dict() if pbo else None
    
    def get_all_pbo(self, limit=100, offset=0):
        """Get all PBO records with pagination"""
        results = PBOData.query.order_by(PBOData.id.desc()).limit(limit).offset(offset).all()
        return [r.to_dict() for r in results]
    
    def search_pbo(self, field, value):
        """Search PBO records by field"""
        field_mapping = {
            'Nama Pasien': 'nama_pasien',
            'Nama Operasi': 'nama_operasi',
            'Tanggal': 'tanggal',
            'Diagnosa': 'diagnosa',
            'Nama Dokter': 'nama_dokter'
        }
        db_field = field_mapping.get(field, 'nama_pasien')
        
        if field == 'Tanggal':
            results = PBOData.query.filter(getattr(PBOData, db_field) == value).order_by(PBOData.id.desc()).all()
        else:
            results = PBOData.query.filter(getattr(PBOData, db_field).like(f'%{value}%')).order_by(PBOData.id.desc()).all()
        
        return [r.to_dict() for r in results]
    
    def delete_pbo(self, pbo_id):
        """Delete PBO record"""
        pbo = PBOData.query.get(pbo_id)
        if pbo:
            db.session.delete(pbo)
            db.session.commit()
    
    def count_pbo(self):
        """Count total PBO records"""
        return PBOData.query.count()
    
    # Operation Tables Operations
    def get_all_operations(self):
        """Get all operation tables"""
        results = OperationTable.query.order_by(OperationTable.kode).all()
        return [r.to_dict() for r in results]
    
    def get_operations_by_kelas(self, kelas):
        """Get operation tables filtered by kelas (case-insensitive)"""
        # Use case-insensitive filter for kelas
        from sqlalchemy import func
        results = OperationTable.query.filter(func.lower(OperationTable.kelas) == func.lower(kelas)).order_by(OperationTable.kode).all()
        return [r.to_dict() for r in results]
    
    def get_operation_by_code(self, kode):
        """Get operation by code"""
        op = OperationTable.query.filter_by(kode=kode).first()
        return op.to_dict() if op else None
    
    def add_operation(self, kode, nama_tindakan, kelas, biaya_dokter, biaya_rs):
        """Add new operation"""
        op = OperationTable(
            kode=kode, nama_tindakan=nama_tindakan, kelas=kelas,
            biaya_dokter=biaya_dokter, biaya_rs=biaya_rs,
            total_biaya=biaya_dokter + biaya_rs
        )
        db.session.add(op)
        db.session.commit()
    
    def update_operation(self, operation_id, kode, nama_tindakan, kelas, biaya_dokter, biaya_rs):
        """Update operation"""
        op = OperationTable.query.get(operation_id)
        if op:
            op.kode = kode
            op.nama_tindakan = nama_tindakan
            op.kelas = kelas
            op.biaya_dokter = biaya_dokter
            op.biaya_rs = biaya_rs
            op.total_biaya = biaya_dokter + biaya_rs
            db.session.commit()
    
    def delete_operation(self, operation_id):
        """Delete operation"""
        op = OperationTable.query.get(operation_id)
        if op:
            db.session.delete(op)
            db.session.commit()
    
    def delete_all_operations(self):
        """Delete all operations"""
        OperationTable.query.delete()
        db.session.commit()
    
    # Doctors Operations
    def get_all_doctors(self):
        """Get all doctors"""
        results = Doctor.query.order_by(Doctor.nama_dokter).all()
        return [r.to_dict() for r in results]
    
    def get_doctor_by_name(self, nama_dokter):
        """Get doctor by name"""
        doc = Doctor.query.filter_by(nama_dokter=nama_dokter).first()
        return doc.to_dict() if doc else None
    
    def add_doctor(self, nama_dokter):
        """Add new doctor"""
        try:
            doctor = Doctor(nama_dokter=nama_dokter)
            db.session.add(doctor)
            db.session.commit()
            return doctor.id
        except:
            db.session.rollback()
            return None
    
    def delete_doctor(self, doctor_id):
        """Delete doctor"""
        doc = Doctor.query.get(doctor_id)
        if doc:
            db.session.delete(doc)
            db.session.commit()
    
    def delete_all_doctors(self):
        """Delete all doctors"""
        Doctor.query.delete()
        db.session.commit()
    
    def count_doctors(self):
        """Count total doctors"""
        return Doctor.query.count()
    
    # Tindakan Items Operations
    def get_all_tindakan_items(self):
        """Get all tindakan items"""
        results = TindakanItem.query.order_by(TindakanItem.nama_tindakan).all()
        return [r.to_dict() for r in results]
    
    def add_tindakan_item(self, nama_tindakan, kelas, kategory, sales_item_type, amount):
        """Add new tindakan item"""
        item = TindakanItem(
            nama_tindakan=nama_tindakan, kelas=kelas, kategory=kategory,
            sales_item_type=sales_item_type, amount=amount
        )
        db.session.add(item)
        db.session.commit()
        return item.id
    
    def delete_all_tindakan_items(self):
        """Delete all tindakan items"""
        TindakanItem.query.delete()
        db.session.commit()
    
    def count_tindakan_items(self):
        """Count total tindakan items"""
        return TindakanItem.query.count()
    
    def get_tindakan_by_kelas(self, kelas):
        """Get tindakan items filtered by kelas (case-insensitive)"""
        from sqlalchemy import func
        results = TindakanItem.query.filter(func.lower(TindakanItem.kelas) == func.lower(kelas)).order_by(TindakanItem.nama_tindakan).all()
        return [r.to_dict() for r in results]
    
    def get_tindakan_by_id(self, tindakan_id):
        """Get tindakan item by ID"""
        item = TindakanItem.query.get(tindakan_id)
        return item.to_dict() if item else None
    
    def update_tindakan_item(self, tindakan_id, nama_tindakan, kelas, kategory, sales_item_type, amount):
        """Update tindakan item"""
        item = TindakanItem.query.get(tindakan_id)
        if item:
            item.nama_tindakan = nama_tindakan
            item.kelas = kelas
            item.kategory = kategory
            item.sales_item_type = sales_item_type
            item.amount = amount
            db.session.commit()
    
    def delete_tindakan_item(self, tindakan_id):
        """Delete tindakan item"""
        item = TindakanItem.query.get(tindakan_id)
        if item:
            db.session.delete(item)
            db.session.commit()
    
    # Paket Tindakan Operations
    def add_paket_tindakan(self, pbo_id, tindakan_id, nama_tindakan, kategory, harga):
        """Add tindakan to paket"""
        paket = PaketTindakan(
            pbo_id=pbo_id, tindakan_id=tindakan_id, nama_tindakan=nama_tindakan,
            kategory=kategory, harga=harga
        )
        db.session.add(paket)
        db.session.commit()
        return paket.id
    
    def get_paket_tindakan_by_pbo(self, pbo_id):
        """Get all tindakan in paket for a PBO"""
        results = PaketTindakan.query.filter_by(pbo_id=pbo_id).order_by(PaketTindakan.id).all()
        return [r.to_dict() for r in results]
    
    def update_paket_tindakan(self, paket_id, tindakan_id, nama_tindakan, kategory, harga):
        """Update paket tindakan"""
        paket = PaketTindakan.query.get(paket_id)
        if paket:
            paket.tindakan_id = tindakan_id
            paket.nama_tindakan = nama_tindakan
            paket.kategory = kategory
            paket.harga = harga
            db.session.commit()
    
    def delete_paket_tindakan(self, paket_id):
        """Delete paket tindakan"""
        paket = PaketTindakan.query.get(paket_id)
        if paket:
            db.session.delete(paket)
            db.session.commit()
    
    def delete_paket_tindakan_by_pbo(self, pbo_id):
        """Delete all paket for a PBO"""
        PaketTindakan.query.filter_by(pbo_id=pbo_id).delete()
        db.session.commit()
    
    def count_paket_tindakan_by_pbo(self, pbo_id):
        """Count paket tindakan for a PBO"""
        return PaketTindakan.query.filter_by(pbo_id=pbo_id).count()
    
    # User Authentication
    def authenticate_user(self, username, password):
        """Authenticate user"""
        user = User.query.filter_by(username=username, password=password).first()
        return user.to_dict() if user else None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        user = User.query.filter_by(username=username).first()
        return user.to_dict() if user else None
    
    def get_all_users(self):
        """Get all users"""
        results = User.query.order_by(User.id).all()
        return [r.to_dict() for r in results]
    
    # PBO Versioning Operations
    def create_pbo_version(self, parent_id, data, username):
        """Create new version of PBO"""
        parent = PBOData.query.get(parent_id)
        if not parent:
            return None
        
        root_parent_id = parent.parent_id if parent.parent_id else parent_id
        new_version_number = parent.version_number + 1
        
        parent.is_latest = 0
        db.session.commit()
        
        new_pbo = PBOData(
            diagnosa=data[0], nama_operasi=data[1], sifat_operasi=data[2],
            nama_dokter=data[3], kelas=data[4], tabel_operasi1=data[5],
            tabel_operasi2=data[6], tabel_operasi3=data[7], tabel_operasi4=data[8],
            persentase_operasi1=data[9], persentase_operasi2=data[10],
            persentase_operasi3=data[11], persentase_operasi4=data[12],
            konsultasi_pre_tindakan=data[13], diagnostic_pre_tindakan=data[14],
            surgeon=data[15], anesthesi=data[16], ot_room_charge=data[17],
            recovery_room_charge=data[18], alat=data[19], diagnostic=data[20],
            medical_equipment=data[21], obat_dan_alkes=data[22], tarif_kamar=data[23],
            total=data[24], catatan=data[25], keterangan=data[26],
            tanggal=datetime.strptime(data[27], '%Y-%m-%d').date() if data[27] else None,
            nama_pasien=data[28], hubungan_dengan_pasien=data[29],
            petugas_front_office=data[30], perusahaan_asuransi=data[31],
            version_number=new_version_number, parent_id=root_parent_id,
            is_latest=1, edited_by=username, edited_at=datetime.now()
        )
        db.session.add(new_pbo)
        db.session.commit()
        return new_pbo.id
    
    def get_pbo_versions(self, pbo_id):
        """Get all versions of a PBO"""
        pbo = PBOData.query.get(pbo_id)
        if not pbo:
            return []
        
        root_parent_id = pbo.parent_id if pbo.parent_id else pbo_id
        results = PBOData.query.filter((PBOData.id == root_parent_id) | (PBOData.parent_id == root_parent_id)).order_by(PBOData.version_number.desc()).all()
        return [r.to_dict() for r in results]
    
    def get_pbo_version_by_id(self, version_id):
        """Get specific version"""
        return self.get_pbo_by_id(version_id)
    
    def restore_pbo_version(self, version_id, username):
        """Restore a previous version"""
        version = PBOData.query.get(version_id)
        if not version:
            return None
        
        root_parent_id = version.parent_id if version.parent_id else version_id
        max_version = db.session.query(db.func.max(PBOData.version_number)).filter((PBOData.id == root_parent_id) | (PBOData.parent_id == root_parent_id)).scalar() or 0
        new_version_number = max_version + 1
        
        PBOData.query.filter((PBOData.id == root_parent_id) | (PBOData.parent_id == root_parent_id)).update({PBOData.is_latest: 0})
        db.session.commit()
        
        new_pbo = PBOData(
            diagnosa=version.diagnosa, nama_operasi=version.nama_operasi,
            sifat_operasi=version.sifat_operasi, nama_dokter=version.nama_dokter,
            kelas=version.kelas, tabel_operasi1=version.tabel_operasi1,
            tabel_operasi2=version.tabel_operasi2, tabel_operasi3=version.tabel_operasi3,
            tabel_operasi4=version.tabel_operasi4, persentase_operasi1=version.persentase_operasi1,
            persentase_operasi2=version.persentase_operasi2, persentase_operasi3=version.persentase_operasi3,
            persentase_operasi4=version.persentase_operasi4, konsultasi_pre_tindakan=version.konsultasi_pre_tindakan,
            diagnostic_pre_tindakan=version.diagnostic_pre_tindakan, surgeon=version.surgeon,
            anesthesi=version.anesthesi, ot_room_charge=version.ot_room_charge,
            recovery_room_charge=version.recovery_room_charge, alat=version.alat,
            diagnostic=version.diagnostic, medical_equipment=version.medical_equipment,
            obat_dan_alkes=version.obat_dan_alkes, tarif_kamar=version.tarif_kamar,
            total=version.total, catatan=version.catatan, keterangan=version.keterangan,
            tanggal=version.tanggal, nama_pasien=version.nama_pasien,
            hubungan_dengan_pasien=version.hubungan_dengan_pasien, petugas_front_office=version.petugas_front_office,
            perusahaan_asuransi=version.perusahaan_asuransi, version_number=new_version_number,
            parent_id=root_parent_id, is_latest=1, edited_by=username, edited_at=datetime.now()
        )
        db.session.add(new_pbo)
        db.session.commit()
        return new_pbo.id
    
    def compare_pbo_versions(self, version1_id, version2_id):
        """Compare two versions"""
        v1 = PBOData.query.get(version1_id)
        v2 = PBOData.query.get(version2_id)
        
        if not v1 or not v2:
            return None
        
        differences = []
        fields = ['diagnosa', 'nama_operasi', 'sifat_operasi', 'nama_dokter', 'kelas',
                 'tabel_operasi1', 'tabel_operasi2', 'tabel_operasi3', 'tabel_operasi4',
                 'persentase_operasi1', 'persentase_operasi2', 'persentase_operasi3', 'persentase_operasi4',
                 'konsultasi_pre_tindakan', 'diagnostic_pre_tindakan', 'surgeon', 'anesthesi',
                 'ot_room_charge', 'recovery_room_charge', 'alat', 'diagnostic', 'medical_equipment',
                 'obat_dan_alkes', 'tarif_kamar', 'total', 'catatan', 'keterangan', 'tanggal',
                 'nama_pasien', 'hubungan_dengan_pasien', 'petugas_front_office', 'perusahaan_asuransi']
        
        for field in fields:
            val1 = getattr(v1, field)
            val2 = getattr(v2, field)
            if val1 != val2:
                differences.append({'field': field, 'version1_value': val1, 'version2_value': val2})
        
        return {
            'version1': v1.to_dict(),
            'version2': v2.to_dict(),
            'differences': differences,
            'has_differences': len(differences) > 0
        }
    
    def get_all_latest_pbo(self, limit=100, offset=0):
        """Get all latest PBO records"""
        results = PBOData.query.filter_by(is_latest=1).order_by(PBOData.id.desc()).limit(limit).offset(offset).all()
        return [r.to_dict() for r in results]
    
    def search_latest_pbo(self, field, value):
        """Search latest PBO records"""
        field_mapping = {
            'Nama Pasien': 'nama_pasien',
            'Nama Operasi': 'nama_operasi',
            'Tanggal': 'tanggal',
            'Diagnosa': 'diagnosa',
            'Nama Dokter': 'nama_dokter'
        }
        db_field = field_mapping.get(field, 'nama_pasien')
        
        if field == 'Tanggal':
            results = PBOData.query.filter((getattr(PBOData, db_field) == value) & (PBOData.is_latest == 1)).order_by(PBOData.id.desc()).all()
        else:
            results = PBOData.query.filter((getattr(PBOData, db_field).like(f'%{value}%')) & (PBOData.is_latest == 1)).order_by(PBOData.id.desc()).all()
        
        return [r.to_dict() for r in results]
    
    # Room Type Operations
    def get_all_room_types(self):
        """Get all room types"""
        from models_sqlalchemy import RoomType
        results = RoomType.query.order_by(RoomType.harga_per_hari).all()
        return [r.to_dict() for r in results]
    
    def get_room_type_by_name(self, nama_kamar):
        """Get room type by name"""
        from models_sqlalchemy import RoomType
        room = RoomType.query.filter_by(nama_kamar=nama_kamar).first()
        return room.to_dict() if room else None
    
    def add_room_type(self, nama_kamar, harga_per_hari, deskripsi=''):
        """Add new room type"""
        from models_sqlalchemy import RoomType
        try:
            room = RoomType(nama_kamar=nama_kamar, harga_per_hari=harga_per_hari, deskripsi=deskripsi)
            db.session.add(room)
            db.session.commit()
            return room.id
        except Exception as e:
            db.session.rollback()
            print(f"Error adding room type: {e}")
            return None
    
    def update_room_type(self, room_id, nama_kamar, harga_per_hari, deskripsi=''):
        """Update room type"""
        from models_sqlalchemy import RoomType
        room = RoomType.query.get(room_id)
        if room:
            room.nama_kamar = nama_kamar
            room.harga_per_hari = harga_per_hari
            room.deskripsi = deskripsi
            db.session.commit()
            return True
        return False
    
    def delete_room_type(self, room_id):
        """Delete room type"""
        from models_sqlalchemy import RoomType
        room = RoomType.query.get(room_id)
        if room:
            db.session.delete(room)
            db.session.commit()
            return True
        return False
    
    def delete_all_room_types(self):
        """Delete all room types"""
        from models_sqlalchemy import RoomType
        RoomType.query.delete()
        db.session.commit()
    
    def count_latest_pbo(self):
        """Count latest PBO records"""
        return PBOData.query.filter_by(is_latest=1).count()
    
    def get_monthly_report(self, year, month):
        """Get monthly report with operation name, doctor name, and insurance company"""
        from datetime import date
        from sqlalchemy import extract
        
        # Query data for specific month and year
        results = PBOData.query.filter(
            extract('year', PBOData.tanggal) == year,
            extract('month', PBOData.tanggal) == month,
            PBOData.is_latest == 1
        ).order_by(PBOData.tanggal.desc()).all()
        
        # Format result
        report_data = []
        for pbo in results:
            report_data.append({
                'id': pbo.id,
                'tanggal': pbo.tanggal,
                'nama_operasi': pbo.nama_operasi,
                'nama_dokter': pbo.nama_dokter,
                'perusahaan_asuransi': pbo.perusahaan_asuransi,
                'nama_pasien': pbo.nama_pasien,
                'kelas': pbo.kelas,
                'total': pbo.total
            })
        
        return report_data
    
    def get_available_months(self):
        """Get list of months that have data"""
        from sqlalchemy import func, distinct, extract
        
        months = db.session.query(
            extract('year', PBOData.tanggal).label('year'),
            extract('month', PBOData.tanggal).label('month'),
            func.count(distinct(PBOData.id)).label('count')
        ).filter(
            PBOData.tanggal.isnot(None),
            PBOData.is_latest == 1
        ).group_by(
            extract('year', PBOData.tanggal),
            extract('month', PBOData.tanggal)
        ).order_by(
            extract('year', PBOData.tanggal).desc(),
            extract('month', PBOData.tanggal).desc()
        ).all()
        
        return months
