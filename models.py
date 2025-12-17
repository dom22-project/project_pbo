import sqlite3
import os
from datetime import datetime
from config import Config

class Database:
    """Database helper class for PBO application"""
    
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        if not os.path.exists('data'):
            os.makedirs('data')
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create main PBO data table with versioning support
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS database (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                diagnosa TEXT,
                nama_operasi TEXT,
                sifat_operasi TEXT,
                nama_dokter TEXT,
                kelas TEXT,
                tabel_operasi1 TEXT,
                tabel_operasi2 TEXT,
                tabel_operasi3 TEXT,
                tabel_operasi4 TEXT,
                persentase_operasi1 REAL,
                persentase_operasi2 REAL,
                persentase_operasi3 REAL,
                persentase_operasi4 REAL,
                konsultasi_pre_tindakan REAL,
                diagnostic_pre_tindakan REAL,
                surgeon REAL,
                anesthesi REAL,
                ot_room_charge REAL,
                recovery_room_charge REAL,
                alat REAL,
                diagnostic REAL,
                medical_equipment REAL,
                obat_dan_alkes REAL,
                tarif_kamar REAL,
                total REAL,
                catatan TEXT,
                keterangan TEXT,
                tanggal DATE,
                nama_pasien TEXT,
                hubungan_dengan_pasien TEXT,
                petugas_front_office TEXT,
                perusahaan_asuransi TEXT,
                tindakan_tambahan TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                version_number INTEGER DEFAULT 1,
                parent_id INTEGER,
                is_latest INTEGER DEFAULT 1,
                edited_by TEXT,
                edited_at TIMESTAMP
            )
        ''')
        
        # Add versioning columns to existing database if they don't exist
        try:
            cursor.execute("ALTER TABLE database ADD COLUMN version_number INTEGER DEFAULT 1")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE database ADD COLUMN parent_id INTEGER")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE database ADD COLUMN is_latest INTEGER DEFAULT 1")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE database ADD COLUMN edited_by TEXT")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE database ADD COLUMN edited_at TIMESTAMP")
        except sqlite3.OperationalError:
            pass
        
        # Update existing records to have version_number = 1 and is_latest = 1
        cursor.execute("UPDATE database SET version_number = 1 WHERE version_number IS NULL")
        cursor.execute("UPDATE database SET is_latest = 1 WHERE is_latest IS NULL")
        
        # Create operation tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operation_tables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kode TEXT,
                nama_tindakan TEXT,
                kelas TEXT,
                biaya_dokter REAL,
                biaya_rs REAL,
                total_biaya REAL
            )
        ''')
        
        # Create doctors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_dokter TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create tindakan items table (from "db nama tindakan" sheet)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tindakan_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_tindakan TEXT,
                kelas TEXT,
                kategory TEXT,
                sales_item_type TEXT,
                amount REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create paket tindakan table (for storing selected tindakan in PBO)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS paket_tindakan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pbo_id INTEGER,
                tindakan_id INTEGER,
                nama_tindakan TEXT,
                kategory TEXT,
                harga REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pbo_id) REFERENCES database(id) ON DELETE CASCADE,
                FOREIGN KEY (tindakan_id) REFERENCES tindakan_items(id)
            )
        ''')
        
        # Create users table for authentication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default users if table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            default_users = [
                ('admin', 'admin123', 'admin'),
                ('user', 'user123', 'user'),
            ]
            cursor.executemany('''
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
            ''', default_users)
        
        # Insert default operations if table is empty
        cursor.execute("SELECT COUNT(*) FROM operation_tables")
        if cursor.fetchone()[0] == 0:
            default_operations = [
                ('4199999994', 'DOCTORS PROCEDURE TABLE 3', 'ODC', 4934000, 0, 4934000),
                ('4199999995', 'DOCTORS PROCEDURE TABLE 1', 'ODC', 1125000, 0, 1125000),
                ('4199999996', 'DOCTORS PROCEDURE TABLE 2', 'ODC', 2368000, 0, 2368000),
            ]
            cursor.executemany('''
                INSERT INTO operation_tables (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', default_operations)
        
        conn.commit()
        conn.close()
    
    # PBO Data Operations
    def create_pbo(self, data):
        """Create new PBO record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO database (
                diagnosa, nama_operasi, sifat_operasi, nama_dokter, kelas,
                tabel_operasi1, tabel_operasi2, tabel_operasi3, tabel_operasi4,
                persentase_operasi1, persentase_operasi2, persentase_operasi3, persentase_operasi4,
                konsultasi_pre_tindakan, diagnostic_pre_tindakan, surgeon,
                anesthesi, ot_room_charge, recovery_room_charge, alat,
                diagnostic, medical_equipment, obat_dan_alkes, tarif_kamar,
                total, catatan, keterangan, tanggal, nama_pasien,
                hubungan_dengan_pasien, petugas_front_office, perusahaan_asuransi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        
        pbo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return pbo_id
    
    def get_pbo_by_id(self, pbo_id):
        """Get PBO record by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM database WHERE id = ?", (pbo_id,))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def get_all_pbo(self, limit=100, offset=0):
        """Get all PBO records with pagination"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nama_pasien, nama_operasi, diagnosa, nama_dokter, kelas, tanggal, total 
            FROM database 
            ORDER BY id DESC 
            LIMIT ? OFFSET ?
        """, (limit, offset))
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def search_pbo(self, field, value):
        """Search PBO records by field"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        field_mapping = {
            'Nama Pasien': 'nama_pasien',
            'Nama Operasi': 'nama_operasi',
            'Tanggal': 'tanggal',
            'Diagnosa': 'diagnosa',
            'Nama Dokter': 'nama_dokter'
        }
        
        db_field = field_mapping.get(field, 'nama_pasien')
        
        if field == 'Tanggal':
            query = f"SELECT * FROM database WHERE {db_field} = ? ORDER BY id DESC"
            params = (value,)
        else:
            query = f"SELECT * FROM database WHERE {db_field} LIKE ? ORDER BY id DESC"
            params = (f'%{value}%',)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def update_pbo(self, pbo_id, data):
        """Update PBO record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE database SET
                diagnosa=?, nama_operasi=?, sifat_operasi=?, nama_dokter=?, kelas=?,
                tabel_operasi1=?, tabel_operasi2=?, tabel_operasi3=?, tabel_operasi4=?,
                persentase_operasi1=?, persentase_operasi2=?, persentase_operasi3=?, persentase_operasi4=?,
                konsultasi_pre_tindakan=?, diagnostic_pre_tindakan=?, surgeon=?,
                anesthesi=?, ot_room_charge=?, recovery_room_charge=?, alat=?,
                diagnostic=?, medical_equipment=?, obat_dan_alkes=?, tarif_kamar=?,
                total=?, catatan=?, keterangan=?, tanggal=?, nama_pasien=?,
                hubungan_dengan_pasien=?, petugas_front_office=?, perusahaan_asuransi=?
            WHERE id=?
        ''', data + (pbo_id,))
        
        conn.commit()
        conn.close()
    
    def delete_pbo(self, pbo_id):
        """Delete PBO record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM database WHERE id = ?", (pbo_id,))
        conn.commit()
        conn.close()
    
    def count_pbo(self):
        """Count total PBO records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM database")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    # Operation Tables Operations
    def get_all_operations(self):
        """Get all operation tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM operation_tables ORDER BY kode")
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def get_operations_by_kelas(self, kelas):
        """Get operation tables filtered by kelas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM operation_tables WHERE kelas = ? ORDER BY kode", (kelas,))
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def get_operation_by_code(self, kode):
        """Get operation by code"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM operation_tables WHERE kode = ?", (kode,))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def add_operation(self, kode, nama_tindakan, kelas, biaya_dokter, biaya_rs):
        """Add new operation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        total_biaya = biaya_dokter + biaya_rs
        
        cursor.execute('''
            INSERT INTO operation_tables (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya))
        
        conn.commit()
        conn.close()
    
    def update_operation(self, operation_id, kode, nama_tindakan, kelas, biaya_dokter, biaya_rs):
        """Update operation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        total_biaya = biaya_dokter + biaya_rs
        
        cursor.execute('''
            UPDATE operation_tables 
            SET kode=?, nama_tindakan=?, kelas=?, biaya_dokter=?, biaya_rs=?, total_biaya=?
            WHERE id=?
        ''', (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya, operation_id))
        
        conn.commit()
        conn.close()
    
    def delete_operation(self, operation_id):
        """Delete operation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM operation_tables WHERE id=?", (operation_id,))
        conn.commit()
        conn.close()
    
    def delete_all_operations(self):
        """Delete all operations from the table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM operation_tables")
        conn.commit()
        conn.close()
    
    # Doctors Operations
    def get_all_doctors(self):
        """Get all doctors"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors ORDER BY nama_dokter")
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def add_doctor(self, nama_dokter):
        """Add new doctor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO doctors (nama_dokter)
                VALUES (?)
            ''', (nama_dokter,))
            conn.commit()
            doctor_id = cursor.lastrowid
            conn.close()
            return doctor_id
        except sqlite3.IntegrityError:
            # Doctor already exists
            conn.close()
            return None
    
    def delete_doctor(self, doctor_id):
        """Delete doctor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctors WHERE id=?", (doctor_id,))
        conn.commit()
        conn.close()
    
    def delete_all_doctors(self):
        """Delete all doctors from the table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctors")
        conn.commit()
        conn.close()
    
    def count_doctors(self):
        """Count total doctors"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM doctors")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    # Tindakan Items Operations (from "db nama tindakan" sheet)
    def get_all_tindakan_items(self):
        """Get all tindakan items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tindakan_items ORDER BY nama_tindakan")
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def add_tindakan_item(self, nama_tindakan, kelas, kategory, sales_item_type, amount):
        """Add new tindakan item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tindakan_items (nama_tindakan, kelas, kategory, sales_item_type, amount)
            VALUES (?, ?, ?, ?, ?)
        ''', (nama_tindakan, kelas, kategory, sales_item_type, amount))
        
        conn.commit()
        item_id = cursor.lastrowid
        conn.close()
        return item_id
    
    def delete_all_tindakan_items(self):
        """Delete all tindakan items from the table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tindakan_items")
        conn.commit()
        conn.close()
    
    def count_tindakan_items(self):
        """Count total tindakan items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tindakan_items")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_tindakan_by_kelas(self, kelas):
        """Get tindakan items filtered by kelas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tindakan_items WHERE kelas = ? ORDER BY nama_tindakan", (kelas,))
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def get_tindakan_by_id(self, tindakan_id):
        """Get tindakan item by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tindakan_items WHERE id = ?", (tindakan_id,))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def update_tindakan_item(self, tindakan_id, nama_tindakan, kelas, kategory, sales_item_type, amount):
        """Update tindakan item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tindakan_items 
            SET nama_tindakan=?, kelas=?, kategory=?, sales_item_type=?, amount=?
            WHERE id=?
        ''', (nama_tindakan, kelas, kategory, sales_item_type, amount, tindakan_id))
        
        conn.commit()
        conn.close()
    
    def delete_tindakan_item(self, tindakan_id):
        """Delete tindakan item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tindakan_items WHERE id=?", (tindakan_id,))
        conn.commit()
        conn.close()
    
    # Paket Tindakan Operations (CRUD for selected tindakan in PBO)
    def add_paket_tindakan(self, pbo_id, tindakan_id, nama_tindakan, kategory, harga):
        """Add tindakan to paket for a specific PBO"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO paket_tindakan (pbo_id, tindakan_id, nama_tindakan, kategory, harga)
            VALUES (?, ?, ?, ?, ?)
        ''', (pbo_id, tindakan_id, nama_tindakan, kategory, harga))
        
        conn.commit()
        paket_id = cursor.lastrowid
        conn.close()
        return paket_id
    
    def get_paket_tindakan_by_pbo(self, pbo_id):
        """Get all tindakan in paket for a specific PBO"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM paket_tindakan WHERE pbo_id = ? ORDER BY id", (pbo_id,))
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def update_paket_tindakan(self, paket_id, tindakan_id, nama_tindakan, kategory, harga):
        """Update a tindakan in paket"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE paket_tindakan 
            SET tindakan_id=?, nama_tindakan=?, kategory=?, harga=?
            WHERE id=?
        ''', (tindakan_id, nama_tindakan, kategory, harga, paket_id))
        
        conn.commit()
        conn.close()
    
    def delete_paket_tindakan(self, paket_id):
        """Delete a tindakan from paket"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM paket_tindakan WHERE id=?", (paket_id,))
        conn.commit()
        conn.close()
    
    def delete_paket_tindakan_by_pbo(self, pbo_id):
        """Delete all tindakan in paket for a specific PBO"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM paket_tindakan WHERE pbo_id=?", (pbo_id,))
        conn.commit()
        conn.close()
    
    def count_paket_tindakan_by_pbo(self, pbo_id):
        """Count total tindakan in paket for a specific PBO"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM paket_tindakan WHERE pbo_id=?", (pbo_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    # User Authentication Operations
    def authenticate_user(self, username, password):
        """Authenticate user and return user data if valid"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def get_all_users(self):
        """Get all users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role, created_at FROM users ORDER BY id")
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    # PBO Versioning Operations
    def create_pbo_version(self, parent_id, data, username):
        """Create a new version of PBO record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get parent version info
        cursor.execute("SELECT version_number, parent_id FROM database WHERE id = ?", (parent_id,))
        parent = cursor.fetchone()
        
        if not parent:
            conn.close()
            return None
        
        # Determine the root parent_id (original record)
        root_parent_id = parent['parent_id'] if parent['parent_id'] else parent_id
        new_version_number = parent['version_number'] + 1
        
        # Set old version as not latest
        cursor.execute("UPDATE database SET is_latest = 0 WHERE id = ?", (parent_id,))
        
        # Create new version
        cursor.execute('''
            INSERT INTO database (
                diagnosa, nama_operasi, sifat_operasi, nama_dokter, kelas,
                tabel_operasi1, tabel_operasi2, tabel_operasi3, tabel_operasi4,
                persentase_operasi1, persentase_operasi2, persentase_operasi3, persentase_operasi4,
                konsultasi_pre_tindakan, diagnostic_pre_tindakan, surgeon,
                anesthesi, ot_room_charge, recovery_room_charge, alat,
                diagnostic, medical_equipment, obat_dan_alkes, tarif_kamar,
                total, catatan, keterangan, tanggal, nama_pasien,
                hubungan_dengan_pasien, petugas_front_office, perusahaan_asuransi,
                version_number, parent_id, is_latest, edited_by, edited_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data + (new_version_number, root_parent_id, 1, username, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        new_version_id = cursor.lastrowid
        
        # Cleanup old versions (keep only last 10)
        self._cleanup_old_versions(cursor, root_parent_id)
        
        conn.commit()
        conn.close()
        return new_version_id
    
    def _cleanup_old_versions(self, cursor, root_parent_id):
        """Keep only the last 10 versions of a PBO record"""
        # Get all versions for this root parent
        cursor.execute("""
            SELECT id FROM database 
            WHERE (id = ? OR parent_id = ?)
            ORDER BY version_number DESC
        """, (root_parent_id, root_parent_id))
        
        all_versions = cursor.fetchall()
        
        # If more than 10 versions, delete the oldest ones
        if len(all_versions) > 10:
            versions_to_delete = [v['id'] for v in all_versions[10:]]
            placeholders = ','.join('?' * len(versions_to_delete))
            cursor.execute(f"DELETE FROM database WHERE id IN ({placeholders})", versions_to_delete)
    
    def get_pbo_versions(self, pbo_id):
        """Get all versions of a PBO record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # First, determine if this is a root or child record
        cursor.execute("SELECT parent_id FROM database WHERE id = ?", (pbo_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return []
        
        # Get the root parent ID
        root_parent_id = result['parent_id'] if result['parent_id'] else pbo_id
        
        # Get all versions
        cursor.execute("""
            SELECT id, version_number, is_latest, edited_by, edited_at, created_at, 
                   nama_pasien, nama_operasi, total, tanggal
            FROM database 
            WHERE (id = ? OR parent_id = ?)
            ORDER BY version_number DESC
        """, (root_parent_id, root_parent_id))
        
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def get_pbo_version_by_id(self, version_id):
        """Get a specific version of PBO record"""
        return self.get_pbo_by_id(version_id)
    
    def get_latest_pbo_version(self, pbo_id):
        """Get the latest version of a PBO record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # First, determine if this is a root or child record
        cursor.execute("SELECT parent_id FROM database WHERE id = ?", (pbo_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return None
        
        # Get the root parent ID
        root_parent_id = result['parent_id'] if result['parent_id'] else pbo_id
        
        # Get the latest version
        cursor.execute("""
            SELECT * FROM database 
            WHERE (id = ? OR parent_id = ?) AND is_latest = 1
            LIMIT 1
        """, (root_parent_id, root_parent_id))
        
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def restore_pbo_version(self, version_id, username):
        """Restore a previous version as the latest version"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get the version to restore
        cursor.execute("SELECT * FROM database WHERE id = ?", (version_id,))
        version_to_restore = cursor.fetchone()
        
        if not version_to_restore:
            conn.close()
            return None
        
        # Get the root parent ID
        root_parent_id = version_to_restore['parent_id'] if version_to_restore['parent_id'] else version_id
        
        # Get current latest version number
        cursor.execute("""
            SELECT MAX(version_number) as max_version FROM database 
            WHERE (id = ? OR parent_id = ?)
        """, (root_parent_id, root_parent_id))
        
        max_version = cursor.fetchone()['max_version']
        new_version_number = max_version + 1
        
        # Set all versions as not latest
        cursor.execute("""
            UPDATE database SET is_latest = 0 
            WHERE (id = ? OR parent_id = ?)
        """, (root_parent_id, root_parent_id))
        
        # Create new version from restored data
        data = (
            version_to_restore['diagnosa'], version_to_restore['nama_operasi'], 
            version_to_restore['sifat_operasi'], version_to_restore['nama_dokter'], 
            version_to_restore['kelas'], version_to_restore['tabel_operasi1'],
            version_to_restore['tabel_operasi2'], version_to_restore['tabel_operasi3'], 
            version_to_restore['tabel_operasi4'], version_to_restore['persentase_operasi1'],
            version_to_restore['persentase_operasi2'], version_to_restore['persentase_operasi3'],
            version_to_restore['persentase_operasi4'], version_to_restore['konsultasi_pre_tindakan'],
            version_to_restore['diagnostic_pre_tindakan'], version_to_restore['surgeon'],
            version_to_restore['anesthesi'], version_to_restore['ot_room_charge'],
            version_to_restore['recovery_room_charge'], version_to_restore['alat'],
            version_to_restore['diagnostic'], version_to_restore['medical_equipment'],
            version_to_restore['obat_dan_alkes'], version_to_restore['tarif_kamar'],
            version_to_restore['total'], version_to_restore['catatan'],
            version_to_restore['keterangan'], version_to_restore['tanggal'],
            version_to_restore['nama_pasien'], version_to_restore['hubungan_dengan_pasien'],
            version_to_restore['petugas_front_office'], version_to_restore['perusahaan_asuransi'],
            new_version_number, root_parent_id, 1, username, datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        cursor.execute('''
            INSERT INTO database (
                diagnosa, nama_operasi, sifat_operasi, nama_dokter, kelas,
                tabel_operasi1, tabel_operasi2, tabel_operasi3, tabel_operasi4,
                persentase_operasi1, persentase_operasi2, persentase_operasi3, persentase_operasi4,
                konsultasi_pre_tindakan, diagnostic_pre_tindakan, surgeon,
                anesthesi, ot_room_charge, recovery_room_charge, alat,
                diagnostic, medical_equipment, obat_dan_alkes, tarif_kamar,
                total, catatan, keterangan, tanggal, nama_pasien,
                hubungan_dengan_pasien, petugas_front_office, perusahaan_asuransi,
                version_number, parent_id, is_latest, edited_by, edited_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        
        restored_id = cursor.lastrowid
        
        # Cleanup old versions
        self._cleanup_old_versions(cursor, root_parent_id)
        
        conn.commit()
        conn.close()
        return restored_id
    
    def compare_pbo_versions(self, version1_id, version2_id):
        """Compare two versions of PBO record and return differences"""
        version1 = self.get_pbo_by_id(version1_id)
        version2 = self.get_pbo_by_id(version2_id)
        
        if not version1 or not version2:
            return None
        
        # Fields to compare
        fields_to_compare = [
            'diagnosa', 'nama_operasi', 'sifat_operasi', 'nama_dokter', 'kelas',
            'tabel_operasi1', 'tabel_operasi2', 'tabel_operasi3', 'tabel_operasi4',
            'persentase_operasi1', 'persentase_operasi2', 'persentase_operasi3', 'persentase_operasi4',
            'konsultasi_pre_tindakan', 'diagnostic_pre_tindakan', 'surgeon',
            'anesthesi', 'ot_room_charge', 'recovery_room_charge', 'alat',
            'diagnostic', 'medical_equipment', 'obat_dan_alkes', 'tarif_kamar',
            'total', 'catatan', 'keterangan', 'tanggal', 'nama_pasien',
            'hubungan_dengan_pasien', 'petugas_front_office', 'perusahaan_asuransi'
        ]
        
        differences = []
        for field in fields_to_compare:
            val1 = version1.get(field)
            val2 = version2.get(field)
            
            if val1 != val2:
                differences.append({
                    'field': field,
                    'version1_value': val1,
                    'version2_value': val2
                })
        
        return {
            'version1': version1,
            'version2': version2,
            'differences': differences,
            'has_differences': len(differences) > 0
        }
    
    def get_all_latest_pbo(self, limit=100, offset=0):
        """Get all latest versions of PBO records with pagination"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nama_pasien, nama_operasi, diagnosa, nama_dokter, kelas, tanggal, total, version_number
            FROM database 
            WHERE is_latest = 1
            ORDER BY id DESC 
            LIMIT ? OFFSET ?
        """, (limit, offset))
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def search_latest_pbo(self, field, value):
        """Search only latest versions of PBO records by field"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        field_mapping = {
            'Nama Pasien': 'nama_pasien',
            'Nama Operasi': 'nama_operasi',
            'Tanggal': 'tanggal',
            'Diagnosa': 'diagnosa',
            'Nama Dokter': 'nama_dokter'
        }
        
        db_field = field_mapping.get(field, 'nama_pasien')
        
        if field == 'Tanggal':
            query = f"SELECT * FROM database WHERE {db_field} = ? AND is_latest = 1 ORDER BY id DESC"
            params = (value,)
        else:
            query = f"SELECT * FROM database WHERE {db_field} LIKE ? AND is_latest = 1 ORDER BY id DESC"
            params = (f'%{value}%',)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def count_latest_pbo(self):
        """Count total latest PBO records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM database WHERE is_latest = 1")
        count = cursor.fetchone()[0]
        conn.close()
        return count
