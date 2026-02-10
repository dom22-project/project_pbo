from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PBOData(db.Model):
    __tablename__ = 'database'
    
    id = db.Column(db.Integer, primary_key=True)
    diagnosa = db.Column(db.String(255))
    nama_operasi = db.Column(db.String(255))
    sifat_operasi = db.Column(db.String(100))
    nama_dokter = db.Column(db.String(255))
    kelas = db.Column(db.String(50))
    tabel_operasi1 = db.Column(db.String(50))
    tabel_operasi2 = db.Column(db.String(50))
    tabel_operasi3 = db.Column(db.String(50))
    tabel_operasi4 = db.Column(db.String(50))
    persentase_operasi1 = db.Column(db.Float, default=1.0)
    persentase_operasi2 = db.Column(db.Float, default=1.0)
    persentase_operasi3 = db.Column(db.Float, default=1.0)
    persentase_operasi4 = db.Column(db.Float, default=1.0)
    konsultasi_pre_tindakan = db.Column(db.Float, default=0)
    diagnostic_pre_tindakan = db.Column(db.Float, default=0)
    surgeon = db.Column(db.Float, default=0)
    anesthesi = db.Column(db.Float, default=0)
    ot_room_charge = db.Column(db.Float, default=0)
    recovery_room_charge = db.Column(db.Float, default=0)
    alat = db.Column(db.Float, default=0)
    diagnostic = db.Column(db.Float, default=0)
    medical_equipment = db.Column(db.Float, default=0)
    obat_dan_alkes = db.Column(db.Float, default=0)
    tarif_kamar = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    catatan = db.Column(db.Text)
    keterangan = db.Column(db.Text)
    tanggal = db.Column(db.Date)
    nama_pasien = db.Column(db.String(255))
    hubungan_dengan_pasien = db.Column(db.String(100))
    petugas_front_office = db.Column(db.String(255))
    perusahaan_asuransi = db.Column(db.String(255))
    tindakan_tambahan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    version_number = db.Column(db.Integer, default=1)
    parent_id = db.Column(db.Integer)
    is_latest = db.Column(db.Integer, default=1)
    edited_by = db.Column(db.String(255))
    edited_at = db.Column(db.DateTime)
    
    # Relationships
    paket_tindakan = db.relationship('PaketTindakan', backref='database', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PBOData {self.id}>'
    
    def to_dict(self):
        # Parse operations JSON if stored in tabel_operasi1
        operations = []
        try:
            if self.tabel_operasi1:
                # Try parsing as JSON for dynamic operations
                import json
                operations = json.loads(self.tabel_operasi1)
        except (json.JSONDecodeError, TypeError):
            # Fall back to legacy format
            if self.tabel_operasi1:
                operations.append({
                    'kode': self.tabel_operasi1,
                    'persentase': self.persentase_operasi1
                })
            if self.tabel_operasi2:
                operations.append({
                    'kode': self.tabel_operasi2,
                    'persentase': self.persentase_operasi2
                })
            if self.tabel_operasi3:
                operations.append({
                    'kode': self.tabel_operasi3,
                    'persentase': self.persentase_operasi3
                })
            if self.tabel_operasi4:
                operations.append({
                    'kode': self.tabel_operasi4,
                    'persentase': self.persentase_operasi4
                })
        
        return {
            'id': self.id,
            'diagnosa': self.diagnosa,
            'nama_operasi': self.nama_operasi,
            'sifat_operasi': self.sifat_operasi,
            'nama_dokter': self.nama_dokter,
            'kelas': self.kelas,
            'operations': operations,  # New field with parsed/converted operations
            'tabel_operasi1': self.tabel_operasi1,
            'tabel_operasi2': self.tabel_operasi2,
            'tabel_operasi3': self.tabel_operasi3,
            'tabel_operasi4': self.tabel_operasi4,
            'persentase_operasi1': self.persentase_operasi1,
            'persentase_operasi2': self.persentase_operasi2,
            'persentase_operasi3': self.persentase_operasi3,
            'persentase_operasi4': self.persentase_operasi4,
            'konsultasi_pre_tindakan': self.konsultasi_pre_tindakan,
            'diagnostic_pre_tindakan': self.diagnostic_pre_tindakan,
            'surgeon': self.surgeon,
            'anesthesi': self.anesthesi,
            'ot_room_charge': self.ot_room_charge,
            'recovery_room_charge': self.recovery_room_charge,
            'alat': self.alat,
            'diagnostic': self.diagnostic,
            'medical_equipment': self.medical_equipment,
            'obat_dan_alkes': self.obat_dan_alkes,
            'tarif_kamar': self.tarif_kamar,
            'total': self.total,
            'catatan': self.catatan,
            'keterangan': self.keterangan,
            'tanggal': self.tanggal.isoformat() if self.tanggal and hasattr(self.tanggal, 'isoformat') else str(self.tanggal) if self.tanggal else None,
            'nama_pasien': self.nama_pasien,
            'hubungan_dengan_pasien': self.hubungan_dengan_pasien,
            'petugas_front_office': self.petugas_front_office,
            'perusahaan_asuransi': self.perusahaan_asuransi,
            'created_at': self.created_at.isoformat() if self.created_at and hasattr(self.created_at, 'isoformat') else str(self.created_at) if self.created_at else None,
            'version_number': self.version_number,
            'parent_id': self.parent_id,
            'is_latest': self.is_latest,
            'edited_by': self.edited_by,
            'edited_at': self.edited_at.isoformat() if self.edited_at and hasattr(self.edited_at, 'isoformat') else str(self.edited_at) if self.edited_at else None
        }

class OperationTable(db.Model):
    __tablename__ = 'operation_tables'
    
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(50), unique=True)
    nama_tindakan = db.Column(db.String(255))
    kelas = db.Column(db.String(50))
    biaya_dokter = db.Column(db.Float, default=0)
    biaya_rs = db.Column(db.Float, default=0)
    total_biaya = db.Column(db.Float, default=0)
    
    def __repr__(self):
        return f'<OperationTable {self.kode}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'kode': self.kode,
            'nama_tindakan': self.nama_tindakan,
            'kelas': self.kelas,
            'biaya_dokter': self.biaya_dokter,
            'biaya_rs': self.biaya_rs,
            'total_biaya': self.total_biaya
        }

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    nama_dokter = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Doctor {self.nama_dokter}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nama_dokter': self.nama_dokter,
            'created_at': self.created_at.isoformat() if self.created_at and hasattr(self.created_at, 'isoformat') else str(self.created_at) if self.created_at else None
        }

class TindakanItem(db.Model):
    __tablename__ = 'tindakan_items'
    
    id = db.Column(db.Integer, primary_key=True)
    nama_tindakan = db.Column(db.String(255))
    kelas = db.Column(db.String(50))
    kategory = db.Column(db.String(100))
    sales_item_type = db.Column(db.String(100))
    amount = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    paket_tindakan = db.relationship('PaketTindakan', backref='tindakan_item', lazy=True)
    
    def __repr__(self):
        return f'<TindakanItem {self.nama_tindakan}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nama_tindakan': self.nama_tindakan,
            'kelas': self.kelas,
            'kategory': self.kategory,
            'sales_item_type': self.sales_item_type,
            'amount': self.amount,
            'created_at': self.created_at.isoformat() if self.created_at and hasattr(self.created_at, 'isoformat') else str(self.created_at) if self.created_at else None
        }

class PaketTindakan(db.Model):
    __tablename__ = 'paket_tindakan'
    
    id = db.Column(db.Integer, primary_key=True)
    pbo_id = db.Column(db.Integer, db.ForeignKey('database.id'), nullable=False)
    tindakan_id = db.Column(db.Integer, db.ForeignKey('tindakan_items.id'))
    nama_tindakan = db.Column(db.String(255))
    kategory = db.Column(db.String(100))
    harga = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<PaketTindakan {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'pbo_id': self.pbo_id,
            'tindakan_id': self.tindakan_id,
            'nama_tindakan': self.nama_tindakan,
            'kategory': self.kategory,
            'harga': self.harga,
            'created_at': self.created_at.isoformat() if self.created_at and hasattr(self.created_at, 'isoformat') else str(self.created_at) if self.created_at else None
        }

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at and hasattr(self.created_at, 'isoformat') else str(self.created_at) if self.created_at else None
        }

class RoomType(db.Model):
    __tablename__ = 'room_types'
    
    id = db.Column(db.Integer, primary_key=True)
    nama_kamar = db.Column(db.String(255), unique=True, nullable=False)
    harga_per_hari = db.Column(db.Float, nullable=False)
    deskripsi = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<RoomType {self.nama_kamar}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nama_kamar': self.nama_kamar,
            'harga_per_hari': self.harga_per_hari,
            'deskripsi': self.deskripsi,
            'created_at': self.created_at.isoformat() if self.created_at and hasattr(self.created_at, 'isoformat') else str(self.created_at) if self.created_at else None
        }
