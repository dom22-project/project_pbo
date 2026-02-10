from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_file
from datetime import datetime
import os
import shutil
import time
import uuid
from functools import wraps
from werkzeug.utils import secure_filename
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from io import BytesIO
from config import Config
from models_sqlalchemy import db, User
from models import Database
from utils import PBOCalculator, FormValidator, ReportGenerator

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db.init_app(app)

# Initialize database helper
db_helper = Database()

# Create tables within app context dan setup default data
with app.app_context():
    try:
        # Create all tables
        db.create_all()
        
        # Add default users if none exist
        if User.query.count() == 0:
            default_users = [
                User(username='admin', password='admin123', role='admin'),
                User(username='user', password='user123', role='user'),
            ]
            db.session.add_all(default_users)
            db.session.commit()
        
        # Add default operations if none exist
        from models_sqlalchemy import OperationTable, RoomType
        if OperationTable.query.count() == 0:
            default_operations = [
                OperationTable(kode='4199999994', nama_tindakan='DOCTORS PROCEDURE TABLE 3', kelas='ODC', biaya_dokter=4934000, biaya_rs=0, total_biaya=4934000),
                OperationTable(kode='4199999995', nama_tindakan='DOCTORS PROCEDURE TABLE 1', kelas='ODC', biaya_dokter=1125000, biaya_rs=0, total_biaya=1125000),
                OperationTable(kode='4199999996', nama_tindakan='DOCTORS PROCEDURE TABLE 2', kelas='ODC', biaya_dokter=2368000, biaya_rs=0, total_biaya=2368000),
            ]
            db.session.add_all(default_operations)
            db.session.commit()
    
        # Add default room types if none exist
        if RoomType.query.count() == 0:
            default_room_types = [
                RoomType(nama_kamar='Basic', harga_per_hari=350000),
                RoomType(nama_kamar='Standard', harga_per_hari=750000),
                RoomType(nama_kamar='Deluxe', harga_per_hari=950000),
                RoomType(nama_kamar='VIP', harga_per_hari=1900000),
                RoomType(nama_kamar='VVIP', harga_per_hari=2000000),
                RoomType(nama_kamar='Suite', harga_per_hari=5000000),
                RoomType(nama_kamar='Presidential Suite', harga_per_hari=7500000),
            ]
            db.session.add_all(default_room_types)
            db.session.commit()
            print("[INIT] Default room types created")
        print("[INIT] Database connected successfully")
    except Exception as e:
        print(f"[WARNING] Database not available: {str(e)}")
        print("[INFO] Aplikasi akan berjalan tanpa database")
        print("[INFO] Pastikan MySQL XAMPP sudah dijalankan")

# Helper function to find sheet name (case-insensitive)
def find_sheet(workbook, sheet_name_pattern):
    """Find sheet by name (case-insensitive)"""
    pattern_lower = sheet_name_pattern.lower()
    for sheet_name in workbook.sheetnames:
        if sheet_name.lower() == pattern_lower:
            return sheet_name
    return None

# Helper function to import Excel to database
def import_excel_to_database(file_path, db_helper):
    """Import data from Excel file to database dengan batch processing untuk menghindari timeout"""
    from config import Config
    
    wb = None  # Initialize to None for finally block
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
        stats = {
            'operations_imported': 0,
            'operations_skipped': 0,
            'doctors_imported': 0,
            'doctors_duplicates': 0,
            'doctors_skipped': 0,
            'tindakan_imported': 0,
            'tindakan_skipped': 0,
            'warnings': []
        }
        
        batch_size = Config.BATCH_SIZE  # Commit setiap 500 baris
        
        print(f"[IMPORT] Starting import from {file_path}")
        print(f"[IMPORT] Available sheets: {wb.sheetnames}")
        print(f"[IMPORT] Batch size: {batch_size} rows")
        
        # Find sheets (case-insensitive)
        operasi_sheet = find_sheet(wb, 'db table operasi')
        dokter_sheet = find_sheet(wb, 'db nama dokter')
        tindakan_sheet = find_sheet(wb, 'db nama tindakan')
        
        # Log warnings for missing sheets
        if not operasi_sheet:
            warning_msg = "Sheet 'db table operasi' tidak ditemukan dalam file Excel"
            print(f"[IMPORT WARNING] {warning_msg}")
            stats['warnings'].append(warning_msg)
        
        if not dokter_sheet:
            warning_msg = "Sheet 'db nama dokter' tidak ditemukan dalam file Excel"
            print(f"[IMPORT WARNING] {warning_msg}")
            stats['warnings'].append(warning_msg)
        
        # Import Operasi (Tabel Operasi) dengan BATCH PROCESSING
        if operasi_sheet:
            print(f"\n{'='*80}")
            print(f"[IMPORT] Starting OPERASI import from sheet: {operasi_sheet}")
            print(f"{'='*80}\n")
            ws = wb[operasi_sheet]
            print(f"[IMPORT] Sheet '{operasi_sheet}' has {ws.max_row} total rows")
            print(f"[IMPORT] Sheet has {ws.max_column} columns")
            
            # Debug: Print first 10 rows raw
            print(f"\n[IMPORT] === FIRST 10 ROWS (RAW) ===")
            all_rows = list(ws.iter_rows(values_only=True))
            for idx, row in enumerate(all_rows[:10], 1):
                print(f"[IMPORT] Row {idx}: {row}")
            print(f"[IMPORT] === END ===\n")
            
            # SIMPLE APPROACH: Just use fixed column positions
            # Column A (0) = No/ID
            # Column B (1) = Operation Name
            # Column C (2) = Kelas (class)
            # Column D (3) = Harga Dokter/Operator
            # Column E (4) = Harga Anestesi/RS
            
            print(f"[IMPORT] Using SIMPLE column reading:")
            print(f"[IMPORT]   Column A (idx 0) = No/ID")
            print(f"[IMPORT]   Column B (idx 1) = Operation Name")  
            print(f"[IMPORT]   Column C (idx 2) = Kelas (CLASS)")
            print(f"[IMPORT]   Column D (idx 3) = Harga Dokter")
            print(f"[IMPORT]   Column E (idx 4) = Harga Anestesi\n")
            
            # Skip header row (row 1), start from row 2
            rows_checked = 0
            batch_operations = []
            skip_reasons = {'empty_both': 0, 'duplicate': 0, 'exception': 0}
            
            for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
                # Skip completely empty rows
                if not row or not any(row):
                    continue
                
                rows_checked += 1
                actual_row_num = row_idx + 2  # min_row=2, so row_idx=0 is row 2
                
                try:
                    # Read columns - use simple fixed positions
                    # If row has less than expected columns, use None
                    no = row[0] if len(row) > 0 else None
                    nama_tindakan = row[1] if len(row) > 1 else None
                    kelas = row[2] if len(row) > 2 else None
                    biaya_dokter_raw = row[3] if len(row) > 3 else None
                    biaya_rs_raw = row[4] if len(row) > 4 else None
                    
                    # Convert strings, clean up
                    if nama_tindakan is not None:
                        nama_tindakan = str(nama_tindakan).strip()
                        if not nama_tindakan:
                            nama_tindakan = None
                    
                    if kelas is not None:
                        kelas = str(kelas).strip()
                        if not kelas:
                            kelas = None
                    
                    # Debug output for first 10 rows
                    if rows_checked <= 10:
                        print(f"[IMPORT] Row {actual_row_num} (data row {rows_checked}):")
                        print(f"[IMPORT]   Raw: {row}")
                        print(f"[IMPORT]   Parsed: no={no}, nama='{nama_tindakan}', kelas='{kelas}', biaya_dok={biaya_dokter_raw}, biaya_rs={biaya_rs_raw}")
                    
                    # Validation: Skip only if BOTH nama and kelas are missing
                    if not nama_tindakan and not kelas:
                        if rows_checked <= 10:
                            print(f"[IMPORT]   ❌ SKIP - both nama_tindakan and kelas are empty")
                        stats['operations_skipped'] += 1
                        skip_reasons['empty_both'] += 1
                        continue
                    
                    # Provide fallbacks if either is missing
                    if not kelas:
                        kelas = 'GENERAL'
                        if rows_checked <= 10:
                            print(f"[IMPORT]   ℹ️  kelas missing, using fallback: GENERAL")
                    
                    if not nama_tindakan:
                        nama_tindakan = f"Operation {kelas}"
                        if rows_checked <= 10:
                            print(f"[IMPORT]   ℹ️  nama missing, using derived: {nama_tindakan}")
                    
                    # Convert prices
                    try:
                        biaya_dokter = float(biaya_dokter_raw) if biaya_dokter_raw else 0
                    except (ValueError, TypeError):
                        biaya_dokter = 0
                    
                    try:
                        biaya_rs = float(biaya_rs_raw) if biaya_rs_raw else 0
                    except (ValueError, TypeError):
                        biaya_rs = 0
                    
                    # Generate kode with UUID for uniqueness guarantee
                    try:
                        if no and no != '':
                            base_kode = f"{int(float(no)):04d}"
                        else:
                            base_kode = f"{actual_row_num:04d}"
                    except:
                        base_kode = f"{actual_row_num:04d}"
                    
                    # Generate unique kode - use UUID suffix to guarantee uniqueness
                    # This prevents PRIMARY KEY conflicts
                    unique_suffix = str(uuid.uuid4())[:8].upper()
                    kode = f"{base_kode}_{unique_suffix}"
                    
                    # Final check - should never happen with UUID but just in case
                    max_attempts = 5
                    attempt = 0
                    while db_helper.get_operation_by_code(kode) and attempt < max_attempts:
                        unique_suffix = str(uuid.uuid4())[:8].upper()
                        kode = f"{base_kode}_{unique_suffix}"
                        attempt += 1
                    
                    if attempt >= max_attempts:
                        if rows_checked <= 10:
                            print(f"[IMPORT]   ⚠️  WARNING - Could not generate unique kode after {max_attempts} attempts")
                        stats['operations_skipped'] += 1
                        skip_reasons['duplicate'] += 1
                        continue
                    
                    batch_operations.append({
                        'kode': kode,
                        'nama_tindakan': str(nama_tindakan),
                        'kelas': str(kelas),
                        'biaya_dokter': biaya_dokter,
                        'biaya_rs': biaya_rs
                    })
                    
                    if rows_checked <= 10:
                        print(f"[IMPORT]   ✅ ADDED to batch - kode={kode}")
                    
                    # Commit batch
                    if len(batch_operations) >= batch_size:
                        # Try batch commit first
                        batch_committed = False
                        try:
                            for op in batch_operations:
                                db_helper.add_operation(**op)
                            db.session.commit()
                            stats['operations_imported'] += len(batch_operations)
                            batch_committed = True
                        except Exception as batch_error:
                            print(f"[IMPORT] Batch commit failed, trying individual inserts...")
                            db.session.rollback()
                            # Try one by one
                            for op in batch_operations:
                                try:
                                    db_helper.add_operation(**op)
                                    db.session.commit()
                                    stats['operations_imported'] += 1
                                except Exception as individual_error:
                                    db.session.rollback()
                                    print(f"[IMPORT]   Single insert failed for {op.get('kode')}: {str(individual_error)[:100]}")
                                    stats['operations_skipped'] += 1
                        batch_operations = []
                    
                except Exception as e:
                    if rows_checked <= 10:
                        print(f"[IMPORT]   ❌ EXCEPTION: {str(e)}")
                    stats['operations_skipped'] += 1
                    skip_reasons['exception'] += 1
            
            # Commit remaining
            if batch_operations:
                try:
                    for op in batch_operations:
                        db_helper.add_operation(**op)
                    db.session.commit()
                    stats['operations_imported'] += len(batch_operations)
                except Exception as batch_error:
                    print(f"[IMPORT] Final batch commit failed, trying individual inserts...")
                    db.session.rollback()
                    for op in batch_operations:
                        try:
                            db_helper.add_operation(**op)
                            db.session.commit()
                            stats['operations_imported'] += 1
                        except Exception as individual_error:
                            db.session.rollback()
                            print(f"[IMPORT]   Single insert failed for {op.get('kode')}: {str(individual_error)[:100]}")
                            stats['operations_skipped'] += 1
            
            # Summary
            print(f"\n{'='*80}")
            print(f"[IMPORT] OPERASI SUMMARY")
            print(f"{'='*80}")
            print(f"  Total rows checked: {rows_checked}")
            print(f"  Successfully imported: {stats['operations_imported']}")
            print(f"  Skipped: {stats['operations_skipped']}")
            print(f"{'='*80}\n")
        
        # Import Dokter dengan BATCH PROCESSING
        if dokter_sheet:
            print(f"[IMPORT] Processing sheet: {dokter_sheet}")
            ws = wb[dokter_sheet]
            doctor_count = 0
            batch_doctors = []
            
            for row_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
                if row_idx == 1:  # Skip header
                    continue
                if not row or not row[0]:  # Skip empty rows
                    continue
                
                try:
                    # Get nama_dokter from column 2 (index 1) or column 1 (index 0)
                    nama_dokter = row[1] if len(row) > 1 and row[1] else row[0]
                    
                    if not nama_dokter:
                        stats['doctors_skipped'] += 1
                        continue
                    
                    nama_dokter = str(nama_dokter).strip()
                    if not nama_dokter:
                        stats['doctors_skipped'] += 1
                        continue
                    
                    # Check if doctor already exists
                    existing = db_helper.get_doctor_by_name(nama_dokter)
                    if existing:
                        stats['doctors_duplicates'] += 1
                        continue
                    
                    batch_doctors.append(nama_dokter)
                    
                    # Commit batch
                    if len(batch_doctors) >= batch_size:
                        print(f"[IMPORT] Committing batch of {len(batch_doctors)} doctors...")
                        try:
                            for doctor_name in batch_doctors:
                                db_helper.add_doctor(doctor_name)
                            db.session.commit()
                            stats['doctors_imported'] += len(batch_doctors)
                            doctor_count += len(batch_doctors)
                            print(f"[IMPORT] Total doctors imported so far: {doctor_count}")
                        except Exception as batch_error:
                            db.session.rollback()
                            print(f"[IMPORT ERROR] Doctor batch commit failed: {str(batch_error)}")
                            # Try adding them one by one
                            for doctor_name in batch_doctors:
                                try:
                                    db_helper.add_doctor(doctor_name)
                                    db.session.commit()
                                    stats['doctors_imported'] += 1
                                    doctor_count += 1
                                except Exception as e:
                                    db.session.rollback()
                                    print(f"[IMPORT ERROR] Failed to add doctor {doctor_name}: {str(e)}")
                                    stats['doctors_skipped'] += 1
                        batch_doctors = []
                        
                except Exception as e:
                    print(f"[IMPORT ERROR] Doctor Row {row_idx}: {str(e)}")
                    stats['doctors_skipped'] += 1
                    continue
            
            # Commit remaining batch
            if batch_doctors:
                print(f"[IMPORT] Committing final batch of {len(batch_doctors)} doctors...")
                try:
                    for doctor_name in batch_doctors:
                        db_helper.add_doctor(doctor_name)
                    db.session.commit()
                    stats['doctors_imported'] += len(batch_doctors)
                    doctor_count += len(batch_doctors)
                except Exception as batch_error:
                    db.session.rollback()
                    print(f"[IMPORT ERROR] Final doctor batch commit failed: {str(batch_error)}")
                    # Try adding them one by one
                    for doctor_name in batch_doctors:
                        try:
                            db_helper.add_doctor(doctor_name)
                            db.session.commit()
                            stats['doctors_imported'] += 1
                            doctor_count += 1
                        except Exception as e:
                            db.session.rollback()
                            print(f"[IMPORT ERROR] Failed to add doctor {doctor_name}: {str(e)}")
                            stats['doctors_skipped'] += 1
            
            print(f"[IMPORT] Total doctors imported: {doctor_count}")
        else:
            print("[IMPORT] Sheet 'db nama dokter' not found - skipping doctor import")
        
        # Import Tindakan dengan BATCH PROCESSING
        if tindakan_sheet:
            print(f"[IMPORT] Processing sheet: {tindakan_sheet}")
            ws = wb[tindakan_sheet]
            batch_tindakan = []
            
            for row_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
                if row_idx == 1:  # Skip header
                    continue
                if not row or not row[0]:  # Skip empty rows
                    continue
                
                try:
                    no = row[0]
                    nama_tindakan = row[1] if len(row) > 1 else None
                    kelas = row[2] if len(row) > 2 else None
                    kategory = row[3] if len(row) > 3 else ''
                    sales_item_type = row[4] if len(row) > 4 else ''
                    amount = row[5] if len(row) > 5 else 0
                    
                    if not all([nama_tindakan, kelas]):
                        stats['tindakan_skipped'] += 1
                        continue
                    
                    # Safely convert amount to float
                    try:
                        amount_float = float(amount) if amount else 0
                    except (ValueError, TypeError):
                        amount_float = 0
                    
                    batch_tindakan.append({
                        'nama_tindakan': str(nama_tindakan),
                        'kelas': str(kelas),
                        'kategory': str(kategory or ''),
                        'sales_item_type': str(sales_item_type or ''),
                        'amount': amount_float
                    })
                    
                    # Commit batch
                    if len(batch_tindakan) >= batch_size:
                        print(f"[IMPORT] Committing batch of {len(batch_tindakan)} tindakan...")
                        try:
                            for tind in batch_tindakan:
                                db_helper.add_tindakan_item(**tind)
                            db.session.commit()
                            stats['tindakan_imported'] += len(batch_tindakan)
                            print(f"[IMPORT] Total tindakan imported so far: {stats['tindakan_imported']}")
                        except Exception as batch_error:
                            db.session.rollback()
                            print(f"[IMPORT ERROR] Tindakan batch commit failed: {str(batch_error)}")
                            # Try adding them one by one
                            for tind in batch_tindakan:
                                try:
                                    db_helper.add_tindakan_item(**tind)
                                    db.session.commit()
                                    stats['tindakan_imported'] += 1
                                except Exception as e:
                                    db.session.rollback()
                                    print(f"[IMPORT ERROR] Failed to add tindakan: {str(e)}")
                                    stats['tindakan_skipped'] += 1
                        batch_tindakan = []
                        
                except Exception as e:
                    print(f"[IMPORT ERROR] Tindakan Row {row_idx}: {str(e)}")
                    stats['tindakan_skipped'] += 1
                    continue
            
            # Commit remaining batch
            if batch_tindakan:
                print(f"[IMPORT] Committing final batch of {len(batch_tindakan)} tindakan...")
                try:
                    for tind in batch_tindakan:
                        db_helper.add_tindakan_item(**tind)
                    db.session.commit()
                    stats['tindakan_imported'] += len(batch_tindakan)
                except Exception as batch_error:
                    db.session.rollback()
                    print(f"[IMPORT ERROR] Final tindakan batch commit failed: {str(batch_error)}")
                    # Try adding them one by one
                    for tind in batch_tindakan:
                        try:
                            db_helper.add_tindakan_item(**tind)
                            db.session.commit()
                            stats['tindakan_imported'] += 1
                        except Exception as e:
                            db.session.rollback()
                            print(f"[IMPORT ERROR] Failed to add tindakan: {str(e)}")
                            stats['tindakan_skipped'] += 1
        
        print(f"[IMPORT] Import completed successfully")
        print(f"[IMPORT] Final Stats - Operations: {stats['operations_imported']}, Doctors: {stats['doctors_imported']}, Tindakan: {stats['tindakan_imported']}")
        
        # Verify data was actually saved
        verify_ops = len(db_helper.get_all_operations())
        verify_docs = db_helper.count_doctors()
        verify_tind = db_helper.count_tindakan_items()
        print(f"[IMPORT] Verification - Operations in DB: {verify_ops}, Doctors in DB: {verify_docs}, Tindakan in DB: {verify_tind}")
        
        return stats
        
    except Exception as e:
        print(f"[IMPORT FATAL ERROR] {str(e)}")
        raise Exception(f"Error importing Excel: {str(e)}")
    finally:
        # Always close the file, even if exception occurs
        if wb:
            try:
                wb.close()
                print(f"[IMPORT] Excel file closed successfully")
            except Exception as close_error:
                print(f"[IMPORT WARNING] Error closing Excel file: {str(close_error)}")

# Authentication decorator
def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu', 'warning')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Akses ditolak! Hanya admin yang dapat mengakses halaman ini.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        user = db_helper.authenticate_user(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Selamat datang, {user["username"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah!', 'danger')
            return redirect(url_for('login'))
    
    # If already logged in, redirect to index
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Anda telah logout, {username}!', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Home page / Dashboard"""
    total_pbo = db_helper.count_latest_pbo()
    recent_pbo = db_helper.get_all_latest_pbo(limit=5)
    return render_template('index.html', 
                         total_pbo=total_pbo,
                         recent_pbo=recent_pbo)

@app.route('/input', methods=['GET', 'POST'])
@login_required
def input_pbo():
    """Input PBO form page"""
    if request.method == 'POST':
        try:
            # Helper function to safely convert percentage
            def safe_percentage_convert(value, default=100):
                """Safely convert percentage value to decimal format"""
                try:
                    if not value or value == '':
                        return default / 100
                    val = float(value)
                    # If value is > 1, assume it's in integer format (50, 100)
                    if val > 1:
                        return val / 100
                    # Otherwise it's already in decimal format (0.5, 1.0)
                    return val
                except (ValueError, TypeError):
                    return default / 100
            
            # Parse dynamic operations from form
            operations_list = []
            op_index = 0
            while True:
                kode_key = f'operations[{op_index}][kode]'
                persentase_key = f'operations[{op_index}][persentase]'
                
                if kode_key not in request.form:
                    break
                
                kode = request.form.get(kode_key, '').strip()
                if kode:
                    persentase = safe_percentage_convert(request.form.get(persentase_key, 100))
                    operations_list.append({
                        'kode': kode,
                        'persentase': persentase
                    })
                
                op_index += 1
            
            # Backward compatibility: if no operations in new format, try old format
            if not operations_list:
                for i in range(1, 5):
                    kode = request.form.get(f'tabel_operasi{i}', '').strip()
                    if kode:
                        persentase = safe_percentage_convert(request.form.get(f'persentase_operasi{i}', 100))
                        operations_list.append({
                            'kode': kode,
                            'persentase': persentase
                        })
            
            # Get form data
            form_data = {
                'diagnosa': request.form.get('diagnosa', ''),
                'nama_operasi': request.form.get('nama_operasi', ''),
                'sifat_operasi': request.form.get('sifat_operasi', 'Elektif / Tentative'),
                'nama_dokter': request.form.get('nama_dokter', ''),
                'kelas': request.form.get('kelas', ''),
                'operations': operations_list,  # Store as JSON
                'konsultasi_pre_tindakan': float(request.form.get('konsultasi_pre_tindakan', 0)),
                'diagnostic_pre_tindakan': float(request.form.get('diagnostic_pre_tindakan', 0)),
                'surgeon': float(request.form.get('surgeon', 0)),
                'anesthesi': float(request.form.get('anesthesi', 0)),
                'ot_room_charge': float(request.form.get('ot_room_charge', 0)),
                'recovery_room_charge': float(request.form.get('recovery_room_charge', 0)),
                'alat': float(request.form.get('alat', 0)),
                'diagnostic': float(request.form.get('diagnostic', 0)),
                'medical_equipment': float(request.form.get('medical_equipment', 0)),
                'obat_dan_alkes': float(request.form.get('obat_dan_alkes', 0)),
                'tarif_kamar': float(request.form.get('tarif_kamar', 0)),
                'total': float(request.form.get('total', 0)),
                'catatan': request.form.get('catatan', ''),
                'keterangan': request.form.get('keterangan', ''),
                'tanggal': request.form.get('tanggal', datetime.now().strftime('%Y-%m-%d')),
                'nama_pasien': request.form.get('nama_pasien', ''),
                'hubungan_dengan_pasien': request.form.get('hubungan_dengan_pasien', ''),
                'petugas_front_office': request.form.get('petugas_front_office', ''),
                'perusahaan_asuransi': request.form.get('perusahaan_asuransi', '')
            }
            
            # Validate form
            is_valid, errors = FormValidator.validate_pbo_form(form_data)
            
            if not is_valid:
                for error in errors:
                    flash(error, 'danger')
                return redirect(url_for('input_pbo'))
            
            # Convert operations list to JSON string for storage
            import json
            operations_json = json.dumps(form_data['operations'])
            
            # Prepare data tuple for database - use JSON for operations
            data = (
                form_data['diagnosa'],
                form_data['nama_operasi'],
                form_data['sifat_operasi'],
                form_data['nama_dokter'],
                form_data['kelas'],
                operations_json,  # Store operations as JSON
                '',  # tabel_operasi2 - deprecated
                '',  # tabel_operasi3 - deprecated
                '',  # tabel_operasi4 - deprecated
                0,   # persentase_operasi1 - deprecated
                0,   # persentase_operasi2 - deprecated
                0,   # persentase_operasi3 - deprecated
                0,   # persentase_operasi4 - deprecated
                form_data['konsultasi_pre_tindakan'],
                form_data['diagnostic_pre_tindakan'],
                form_data['surgeon'],
                form_data['anesthesi'],
                form_data['ot_room_charge'],
                form_data['recovery_room_charge'],
                form_data['alat'],
                form_data['diagnostic'],
                form_data['medical_equipment'],
                form_data['obat_dan_alkes'],
                form_data['tarif_kamar'],
                form_data['total'],
                form_data['catatan'],
                form_data['keterangan'],
                form_data['tanggal'],
                form_data['nama_pasien'],
                form_data['hubungan_dengan_pasien'],
                form_data['petugas_front_office'],
                form_data['perusahaan_asuransi']
            )
            
            # Save to database
            pbo_id = db_helper.create_pbo(data)
            
            flash(f'Data PBO berhasil disimpan dengan ID: {pbo_id}', 'success')
            return redirect(url_for('detail_pbo', pbo_id=pbo_id))
            
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('input_pbo'))
    
    # GET request - show form
    operations = db_helper.get_all_operations()
    doctors = db_helper.get_all_doctors()
    tindakan_items = db_helper.get_all_tindakan_items()
    
    return render_template('input_pbo.html', 
                         operations=operations,
                         doctors=doctors,
                         tindakan_items=tindakan_items,
                         today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search_pbo():
    """Search PBO records - only show latest versions"""
    results = []
    search_performed = False
    
    if request.method == 'POST':
        search_field = request.form.get('search_field', 'Nama Pasien')
        search_value = request.form.get('search_value', '')
        
        if search_value:
            results = db_helper.search_latest_pbo(search_field, search_value)
            search_performed = True
        else:
            results = db_helper.get_all_latest_pbo(limit=100)
            search_performed = True
    
    return render_template('search_pbo.html', 
                         results=results,
                         search_performed=search_performed)

@app.route('/detail/<int:pbo_id>')
@login_required
def detail_pbo(pbo_id):
    """View PBO detail"""
    pbo_data = db_helper.get_pbo_by_id(pbo_id)
    
    if not pbo_data:
        flash('Data PBO tidak ditemukan', 'danger')
        return redirect(url_for('search_pbo'))
    
    return render_template('detail_pbo.html', pbo=pbo_data)

@app.route('/edit/<int:pbo_id>', methods=['GET', 'POST'])
@login_required
def edit_pbo(pbo_id):
    """Edit PBO record - Creates new version"""
    if request.method == 'POST':
        try:
            # Helper function to safely convert percentage
            def safe_percentage_convert(value, default=100):
                """Safely convert percentage value to decimal format"""
                try:
                    if not value or value == '':
                        return default / 100
                    val = float(value)
                    # If value is > 1, assume it's in integer format (50, 100)
                    if val > 1:
                        return val / 100
                    # Otherwise it's already in decimal format (0.5, 1.0)
                    return val
                except (ValueError, TypeError):
                    return default / 100
            
            # Parse dynamic operations from form
            operations_list = []
            op_index = 0
            while True:
                kode_key = f'operations[{op_index}][kode]'
                persentase_key = f'operations[{op_index}][persentase]'
                
                if kode_key not in request.form:
                    break
                
                kode = request.form.get(kode_key, '').strip()
                if kode:
                    persentase = safe_percentage_convert(request.form.get(persentase_key, 100))
                    operations_list.append({
                        'kode': kode,
                        'persentase': persentase
                    })
                
                op_index += 1
            
            # Backward compatibility: if no operations in new format, try old format
            if not operations_list:
                for i in range(1, 5):
                    kode = request.form.get(f'tabel_operasi{i}', '').strip()
                    if kode:
                        persentase = safe_percentage_convert(request.form.get(f'persentase_operasi{i}', 100))
                        operations_list.append({
                            'kode': kode,
                            'persentase': persentase
                        })
            
            # Get form data (same as input_pbo)
            form_data = {
                'diagnosa': request.form.get('diagnosa', ''),
                'nama_operasi': request.form.get('nama_operasi', ''),
                'sifat_operasi': request.form.get('sifat_operasi', 'Elektif / Tentative'),
                'nama_dokter': request.form.get('nama_dokter', ''),
                'kelas': request.form.get('kelas', ''),
                'operations': operations_list,
                'konsultasi_pre_tindakan': float(request.form.get('konsultasi_pre_tindakan', 0)),
                'diagnostic_pre_tindakan': float(request.form.get('diagnostic_pre_tindakan', 0)),
                'surgeon': float(request.form.get('surgeon', 0)),
                'anesthesi': float(request.form.get('anesthesi', 0)),
                'ot_room_charge': float(request.form.get('ot_room_charge', 0)),
                'recovery_room_charge': float(request.form.get('recovery_room_charge', 0)),
                'alat': float(request.form.get('alat', 0)),
                'diagnostic': float(request.form.get('diagnostic', 0)),
                'medical_equipment': float(request.form.get('medical_equipment', 0)),
                'obat_dan_alkes': float(request.form.get('obat_dan_alkes', 0)),
                'tarif_kamar': float(request.form.get('tarif_kamar', 0)),
                'total': float(request.form.get('total', 0)),
                'catatan': request.form.get('catatan', ''),
                'keterangan': request.form.get('keterangan', ''),
                'tanggal': request.form.get('tanggal', datetime.now().strftime('%Y-%m-%d')),
                'nama_pasien': request.form.get('nama_pasien', ''),
                'hubungan_dengan_pasien': request.form.get('hubungan_dengan_pasien', ''),
                'petugas_front_office': request.form.get('petugas_front_office', ''),
                'perusahaan_asuransi': request.form.get('perusahaan_asuransi', '')
            }
            
            # Convert operations list to JSON string for storage
            import json
            operations_json = json.dumps(form_data['operations'])
            
            # Prepare data tuple
            data = (
                form_data['diagnosa'], form_data['nama_operasi'], form_data['sifat_operasi'],
                form_data['nama_dokter'], form_data['kelas'], operations_json,
                '', '', '',
                0, 0, 0, 0,
                form_data['konsultasi_pre_tindakan'], form_data['diagnostic_pre_tindakan'],
                form_data['surgeon'], form_data['anesthesi'], form_data['ot_room_charge'],
                form_data['recovery_room_charge'], form_data['alat'], form_data['diagnostic'],
                form_data['medical_equipment'], form_data['obat_dan_alkes'], form_data['tarif_kamar'],
                form_data['total'], form_data['catatan'], form_data['keterangan'],
                form_data['tanggal'], form_data['nama_pasien'], form_data['hubungan_dengan_pasien'],
                form_data['petugas_front_office'], form_data['perusahaan_asuransi']
            )
            
            # Create new version instead of updating
            new_version_id = db_helper.create_pbo_version(
                parent_id=pbo_id,
                data=data,
                username=session.get('username', 'unknown')
            )
            
            if new_version_id:
                flash(f'Data PBO berhasil diupdate sebagai versi baru (ID: {new_version_id})', 'success')
                return redirect(url_for('detail_pbo', pbo_id=new_version_id))
            else:
                flash('Gagal membuat versi baru', 'danger')
                return redirect(url_for('edit_pbo', pbo_id=pbo_id))
            
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('edit_pbo', pbo_id=pbo_id))
    
    # GET request - show form with existing data
    pbo_data = db_helper.get_pbo_by_id(pbo_id)
    
    if not pbo_data:
        flash('Data PBO tidak ditemukan', 'danger')
        return redirect(url_for('search_pbo'))
    
    operations = db_helper.get_all_operations()
    doctors = db_helper.get_all_doctors()
    return render_template('edit_pbo.html', 
                         pbo=pbo_data,
                         operations=operations,
                         doctors=doctors)

@app.route('/delete/<int:pbo_id>', methods=['POST'])
@admin_required
def delete_pbo(pbo_id):
    """Delete PBO record - Admin only"""
    try:
        db_helper.delete_pbo(pbo_id)
        flash('Data PBO berhasil dihapus', 'success')
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('search_pbo'))

@app.route('/print/<int:pbo_id>')
@login_required
def print_pbo(pbo_id):
    """Print PBO form"""
    pbo_data = db_helper.get_pbo_by_id(pbo_id)
    
    if not pbo_data:
        flash('Data PBO tidak ditemukan', 'danger')
        return redirect(url_for('search_pbo'))
    
    summary = ReportGenerator.generate_pbo_summary(pbo_data)
    
    return render_template('print_pbo.html', 
                         pbo=pbo_data,
                         summary=summary)

# PBO Versioning Routes
@app.route('/history/<int:pbo_id>')
@login_required
def pbo_history(pbo_id):
    """View version history of PBO"""
    # Get all versions
    versions = db_helper.get_pbo_versions(pbo_id)
    
    if not versions:
        flash('Data PBO tidak ditemukan', 'danger')
        return redirect(url_for('search_pbo'))
    
    # Get current PBO data for context
    current_pbo = db_helper.get_pbo_by_id(pbo_id)
    
    # Get all operations from database for reference
    from models_sqlalchemy import OperationTable
    all_operations = OperationTable.query.all()
    operations_dict = {op.kode: op.to_dict() for op in all_operations}
    
    # Enhance versions with operation details
    for version in versions:
        version['operations'] = []
        for i in range(1, 5):
            kode_key = f'tabel_operasi{i}'
            if version.get(kode_key):
                kode = version[kode_key]
                op_detail = operations_dict.get(kode, {})
                version['operations'].append({
                    'index': i,
                    'kode': kode,
                    'nama_tindakan': op_detail.get('nama_tindakan', 'Tidak dikenal'),
                    'kelas': op_detail.get('kelas', '-'),
                    'biaya_dokter': op_detail.get('biaya_dokter', 0),
                    'biaya_rs': op_detail.get('biaya_rs', 0),
                    'total_biaya': op_detail.get('total_biaya', 0),
                    'persentase': version.get(f'persentase_operasi{i}', 1.0)
                })
    
    return render_template('pbo_history.html', 
                         versions=versions,
                         current_pbo=current_pbo,
                         operations_dict=operations_dict)

@app.route('/compare/<int:version1_id>/<int:version2_id>')
@login_required
def compare_versions(version1_id, version2_id):
    """Compare two versions of PBO"""
    comparison = db_helper.compare_pbo_versions(version1_id, version2_id)
    
    if not comparison:
        flash('Versi tidak ditemukan', 'danger')
        return redirect(url_for('search_pbo'))
    
    return render_template('pbo_compare.html', 
                         comparison=comparison)

@app.route('/monthly-report', methods=['GET', 'POST'])
@login_required
def monthly_report():
    """Monthly report dashboard"""
    from datetime import datetime
    
    # Get available months
    available_months = db_helper.get_available_months()
    
    # Default to current month
    now = datetime.now()
    selected_year = int(request.args.get('year', now.year))
    selected_month = int(request.args.get('month', now.month))
    
    # Get report data for selected month
    report_data = db_helper.get_monthly_report(selected_year, selected_month)
    
    # Convert tanggal from string to date if needed for template
    from datetime import date, datetime as dt
    for item in report_data:
        if isinstance(item['tanggal'], str):
            try:
                # Try to parse string as date
                if len(item['tanggal']) == 10:  # YYYY-MM-DD format
                    item['tanggal'] = dt.strptime(item['tanggal'], '%Y-%m-%d').date()
                else:
                    item['tanggal'] = dt.fromisoformat(item['tanggal']).date()
            except (ValueError, AttributeError):
                # If parsing fails, keep as string
                pass
    
    # Get month name in Indonesian
    month_names = {
        1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni',
        7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }
    
    month_name = month_names.get(selected_month, '')
    
    # Calculate statistics
    total_operations = len(report_data)
    total_revenue = sum([item['total'] or 0 for item in report_data])
    
    # Most frequent names in the month
    from collections import Counter

    # Clean and normalize data for accurate counting
    # IMPORTANT: Include ALL data, including empty/null values (convert to "Umum")
    operasi_names = []
    dokter_names = []
    insurance_names = []
    
    for item in report_data:
        # Operations - filter only non-empty
        nama_op = str(item.get('nama_operasi', '')).strip() if item.get('nama_operasi') else None
        if nama_op:
            operasi_names.append(nama_op)
        
        # Doctors - filter only non-empty
        nama_dok = str(item.get('nama_dokter', '')).strip() if item.get('nama_dokter') else None
        if nama_dok:
            dokter_names.append(nama_dok)
        
        # Insurance - IMPORTANT: Convert empty/null to "Umum" to capture all data
        nama_asuransi = str(item.get('perusahaan_asuransi', '')).strip() if item.get('perusahaan_asuransi') else None
        if nama_asuransi:  # If has value
            insurance_names.append(nama_asuransi)
        else:  # If empty/null
            insurance_names.append('Umum')
    
    # Count unique values (for unique_insurances use only actual non-"Umum" values)
    unique_doctors = len(set([d for d in dokter_names if d]))
    actual_insurances = [i for i in insurance_names if i != 'Umum']
    unique_insurances = len(set(actual_insurances)) if actual_insurances else 1

    top_operasi = Counter(operasi_names).most_common(1)
    top_dokter = Counter(dokter_names).most_common(1)
    top_insurance = Counter(insurance_names).most_common(1)

    top_operasi_name, top_operasi_count = (top_operasi[0][0], top_operasi[0][1]) if top_operasi else ('-', 0)
    top_dokter_name, top_dokter_count = (top_dokter[0][0], top_dokter[0][1]) if top_dokter else ('-', 0)
    top_insurance_name, top_insurance_count = (top_insurance[0][0], top_insurance[0][1]) if top_insurance else ('-', 0)
    
    return render_template('monthly_report.html',
                         report_data=report_data,
                         available_months=available_months,
                         selected_year=selected_year,
                         selected_month=selected_month,
                         month_name=month_name,
                         total_operations=total_operations,
                         total_revenue=total_revenue,
                         unique_doctors=unique_doctors,
                         unique_insurances=unique_insurances,
                         top_operasi_name=top_operasi_name,
                         top_operasi_count=top_operasi_count,
                         top_dokter_name=top_dokter_name,
                         top_dokter_count=top_dokter_count,
                         top_insurance_name=top_insurance_name,
                         top_insurance_count=top_insurance_count)
                         

@app.route('/restore/<int:version_id>', methods=['POST'])
@login_required
def restore_version(version_id):
    """Restore a previous version"""
    try:
        restored_id = db_helper.restore_pbo_version(
            version_id=version_id,
            username=session.get('username', 'unknown')
        )
        
        if restored_id:
            flash(f'Versi berhasil di-restore sebagai versi terbaru (ID: {restored_id})', 'success')
            return redirect(url_for('detail_pbo', pbo_id=restored_id))
        else:
            flash('Gagal restore versi', 'danger')
            return redirect(url_for('search_pbo'))
            
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
        return redirect(url_for('search_pbo'))

# API Endpoints for AJAX
@app.route('/api/get-operation-details', methods=['POST'])
def api_get_operation_details():
    """Get operation details by kode"""
    try:
        data = request.get_json()
        kode = data.get('kode', '')
        
        if not kode:
            return jsonify({
                'success': False,
                'error': 'Kode operasi tidak boleh kosong'
            }), 400
        
        operation = db_helper.get_operation_by_code(kode)
        
        if not operation:
            return jsonify({
                'success': False,
                'error': f'Operasi dengan kode {kode} tidak ditemukan'
            }), 404
        
        return jsonify({
            'success': True,
            'data': operation
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
def api_calculate_surgery_fees():
    """API endpoint to calculate surgery fees from dynamic operations"""
    try:
        data = request.get_json()
        
        # Support both old format (tabel_operasi1-4) and new dynamic format (operations array)
        operations_data = []
        
        # Check for new dynamic format (operations array)
        if 'operations' in data and isinstance(data['operations'], list):
            for op in data['operations']:
                if op.get('kode'):
                    operations_data.append({
                        'kode': op.get('kode'),
                        'persentase': float(op.get('persentase', 100))
                    })
        else:
            # Fall back to old format for backward compatibility
            for i in range(1, 5):
                kode = data.get(f'tabel_operasi{i}')
                if kode:
                    operations_data.append({
                        'kode': kode,
                        'persentase': float(data.get(f'persentase_operasi{i}', 100))
                    })
        
        sifat_operasi = data.get('sifat_operasi', 'Elektif / Tentative')
        
        result = PBOCalculator.calculate_surgery_fees(operations_data, sifat_operasi, db_helper)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/get-operation-price', methods=['POST'])
def api_get_operation_price():
    """API endpoint to get operation price by operation code"""
    try:
        data = request.get_json()
        kode = data.get('kode', '').strip()
        
        if not kode:
            return jsonify({
                'success': False,
                'error': 'Operation code is required'
            }), 400
        
        # Extract operation code (remove description if present)
        # Handle format like "4199999994 - DOCTORS PROCEDURE TABLE 3"
        kode = kode.split(' - ')[0].strip()
        
        # Try to get from OperationTable first
        operation = db_helper.get_operation_by_code(kode)
        
        if operation:
            return jsonify({
                'success': True,
                'type': 'operation',
                'price': operation['biaya_dokter'],
                'biaya_dokter': operation['biaya_dokter'],
                'biaya_rs': operation['biaya_rs'],
                'nama_tindakan': operation.get('nama_tindakan', '')
            })
        
        # If not found in OperationTable, check TindakanItem
        # Format: "TINDAKAN-{id} - {nama_tindakan}"
        if kode.startswith('TINDAKAN-'):
            tindakan_id = kode.replace('TINDAKAN-', '').strip()
            try:
                tindakan_id = int(tindakan_id)
                tindakan = db_helper.get_tindakan_by_id(tindakan_id)
                if tindakan:
                    return jsonify({
                        'success': True,
                        'type': 'tindakan',
                        'price': tindakan['amount'],
                        'amount': tindakan['amount'],
                        'nama_tindakan': tindakan.get('nama_tindakan', '')
                    })
            except (ValueError, TypeError):
                pass
        
        return jsonify({
            'success': False,
            'error': f'Operation with code {kode} not found'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/get-room-rate', methods=['POST'])
def api_get_room_rate():
    """API endpoint to get room rate"""
    try:
        data = request.get_json()
        kelas = data.get('kelas', '')
        
        tarif = PBOCalculator.get_room_rate(kelas)
        
        return jsonify({
            'success': True,
            'tarif_kamar': tarif
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/calculate-total', methods=['POST'])
def api_calculate_total():
    """API endpoint to calculate total"""
    try:
        data = request.get_json()
        total = PBOCalculator.calculate_total(data)
        
        return jsonify({
            'success': True,
            'total': total
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/get-tindakan-by-kelas', methods=['POST'])
def api_get_tindakan_by_kelas():
    """API endpoint to get tindakan items and operations filtered by kelas"""
    try:
        data = request.get_json()
        kelas = data.get('kelas', '')

        if not kelas:
            # If no kelas specified, return all items
            tindakan_items = db_helper.get_all_tindakan_items()
            operations = db_helper.get_all_operations()
        else:
            # Filter by kelas
            tindakan_items = db_helper.get_tindakan_by_kelas(kelas)
            operations = db_helper.get_operations_by_kelas(kelas)
        
        return jsonify({
            'success': True,
            'tindakan_items': tindakan_items,
            'operations': operations
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# View Tindakan Items Route
@app.route('/view-tindakan')
@login_required
def view_tindakan():
    """View all tindakan items"""
    tindakan_items = db_helper.get_all_tindakan_items()
    total_items = db_helper.count_tindakan_items()
    
    return render_template('view_tindakan.html',
                         tindakan_items=tindakan_items,
                         total_items=total_items)

# CRUD Tindakan Items Routes
@app.route('/tindakan/add', methods=['GET', 'POST'])
@login_required
def add_tindakan():
    """Add new tindakan item"""
    if request.method == 'POST':
        try:
            nama_tindakan = request.form.get('nama_tindakan', '')
            kelas = request.form.get('kelas', '')
            kategory = request.form.get('kategory', '')
            sales_item_type = request.form.get('sales_item_type', '')
            amount = float(request.form.get('amount', 0))
            
            if not nama_tindakan or not kelas or not kategory:
                flash('Nama Tindakan, Kelas, dan Kategory harus diisi!', 'danger')
                return redirect(url_for('add_tindakan'))
            
            db_helper.add_tindakan_item(nama_tindakan, kelas, kategory, sales_item_type, amount)
            flash('Tindakan berhasil ditambahkan!', 'success')
            return redirect(url_for('view_tindakan'))
            
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('add_tindakan'))
    
    return render_template('add_tindakan.html')

@app.route('/tindakan/edit/<int:tindakan_id>', methods=['GET', 'POST'])
@login_required
def edit_tindakan(tindakan_id):
    """Edit tindakan item"""
    if request.method == 'POST':
        try:
            nama_tindakan = request.form.get('nama_tindakan', '')
            kelas = request.form.get('kelas', '')
            kategory = request.form.get('kategory', '')
            sales_item_type = request.form.get('sales_item_type', '')
            amount = float(request.form.get('amount', 0))
            
            if not nama_tindakan or not kelas or not kategory:
                flash('Nama Tindakan, Kelas, dan Kategory harus diisi!', 'danger')
                return redirect(url_for('edit_tindakan', tindakan_id=tindakan_id))
            
            db_helper.update_tindakan_item(tindakan_id, nama_tindakan, kelas, kategory, sales_item_type, amount)
            flash('Tindakan berhasil diupdate!', 'success')
            return redirect(url_for('view_tindakan'))
            
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('edit_tindakan', tindakan_id=tindakan_id))
    
    tindakan = db_helper.get_tindakan_by_id(tindakan_id)
    if not tindakan:
        flash('Tindakan tidak ditemukan!', 'danger')
        return redirect(url_for('view_tindakan'))
    
    return render_template('edit_tindakan.html', tindakan=tindakan)

@app.route('/tindakan/delete/<int:tindakan_id>', methods=['POST'])
@admin_required
def delete_tindakan(tindakan_id):
    """Delete tindakan item"""
    try:
        db_helper.delete_tindakan_item(tindakan_id)
        flash('Tindakan berhasil dihapus!', 'success')
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('view_tindakan'))

# Room Type Routes
@app.route('/room-types')
@login_required
@admin_required
def view_room_types():
    """View all room types"""
    room_types = db_helper.get_all_room_types()
    return render_template('room_types.html', room_types=room_types)

@app.route('/room-type/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_room_type():
    """Add new room type"""
    if request.method == 'POST':
        try:
            nama_kamar = request.form.get('nama_kamar', '').strip()
            harga_per_hari = float(request.form.get('harga_per_hari', 0))
            deskripsi = request.form.get('deskripsi', '')
            
            if not nama_kamar or harga_per_hari <= 0:
                flash('Nama kamar dan harga harus diisi dengan benar', 'danger')
                return redirect(url_for('add_room_type'))
            
            result = db_helper.add_room_type(nama_kamar, harga_per_hari, deskripsi)
            if result:
                flash(f'Tipe kamar "{nama_kamar}" berhasil ditambahkan', 'success')
                return redirect(url_for('view_room_types'))
            else:
                flash('Gagal menambahkan tipe kamar', 'danger')
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('add_room_type.html')

@app.route('/room-type/edit/<int:room_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_room_type(room_id):
    """Edit room type"""
    from models_sqlalchemy import RoomType
    room = RoomType.query.get(room_id)
    
    if not room:
        flash('Tipe kamar tidak ditemukan', 'danger')
        return redirect(url_for('view_room_types'))
    
    if request.method == 'POST':
        try:
            nama_kamar = request.form.get('nama_kamar', '').strip()
            harga_per_hari = float(request.form.get('harga_per_hari', 0))
            deskripsi = request.form.get('deskripsi', '')
            
            if not nama_kamar or harga_per_hari <= 0:
                flash('Nama kamar dan harga harus diisi dengan benar', 'danger')
                return redirect(url_for('edit_room_type', room_id=room_id))
            
            if db_helper.update_room_type(room_id, nama_kamar, harga_per_hari, deskripsi):
                flash(f'Tipe kamar "{nama_kamar}" berhasil diperbarui', 'success')
                return redirect(url_for('view_room_types'))
            else:
                flash('Gagal memperbarui tipe kamar', 'danger')
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('edit_room_type.html', room=room.to_dict())

@app.route('/room-type/delete/<int:room_id>', methods=['POST'])
@login_required
@admin_required
def delete_room_type(room_id):
    """Delete room type"""
    try:
        if db_helper.delete_room_type(room_id):
            flash('Tipe kamar berhasil dihapus', 'success')
        else:
            flash('Gagal menghapus tipe kamar', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('view_room_types'))

@app.route('/api/get-room-types', methods=['GET'])
def api_get_room_types():
    """API endpoint to get all room types"""
    try:
        room_types = db_helper.get_all_room_types()
        return jsonify({
            'success': True,
            'room_types': room_types
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# Database Upload Route
@app.route('/upload-database', methods=['GET', 'POST'])
@login_required
def upload_database():
    """Upload and import database from Excel file"""
    if request.method == 'POST':
        try:
            # Check if file was uploaded
            if 'database_file' not in request.files:
                flash('Tidak ada file yang dipilih', 'danger')
                return redirect(url_for('upload_database'))
            
            file = request.files['database_file']
            
            # Check if file is selected
            if file.filename == '':
                flash('Tidak ada file yang dipilih', 'danger')
                return redirect(url_for('upload_database'))
            
            # Validate file extension
            if not file.filename.lower().endswith('.xlsx'):
                flash('Format file tidak valid! Hanya file .xlsx yang diperbolehkan.', 'danger')
                return redirect(url_for('upload_database'))
            
            # Secure the filename
            filename = secure_filename(file.filename)
            
            # Create upload folder if not exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            os.makedirs(app.config['BACKUP_FOLDER'], exist_ok=True)
            
            # Save uploaded file
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            
            # Validate Excel file structure
            try:
                wb = openpyxl.load_workbook(upload_path)
                
                # Check for required sheets (case-insensitive)
                sheet_names_lower = [s.lower() for s in wb.sheetnames]
                required_sheets = ['db table operasi', 'db nama dokter']
                missing_sheets = []
                
                for req_sheet in required_sheets:
                    if req_sheet.lower() not in sheet_names_lower:
                        missing_sheets.append(req_sheet)
                
                wb.close()  # Close BEFORE removing file
                
                if missing_sheets:
                    try:
                        os.remove(upload_path)
                    except Exception as e:
                        print(f"[UPLOAD WARNING] Could not delete invalid file: {str(e)}")
                    error_msg = f'File Excel tidak memiliki sheet yang diperlukan:\n- {chr(10).join(missing_sheets)}\n\nSheet yang ditemukan dalam file Anda:\n- {chr(10).join(wb.sheetnames)}'
                    flash(error_msg, 'danger')
                    print(f"[UPLOAD ERROR] Missing sheets: {missing_sheets}")
                    print(f"[UPLOAD ERROR] Available sheets: {wb.sheetnames}")
                    return redirect(url_for('upload_database'))
                    
            except Exception as e:
                print(f"[UPLOAD ERROR] Excel validation error: {str(e)}")
                if os.path.exists(upload_path):
                    try:
                        os.remove(upload_path)
                    except Exception as del_error:
                        print(f"[UPLOAD WARNING] Could not delete invalid file: {str(del_error)}")
                flash(f'File Excel tidak valid: {str(e)}', 'danger')
                return redirect(url_for('upload_database'))
            
            # Backup current database
            backup_path = None
            try:
                if app.config.get('DATABASE_PATH') and os.path.exists(app.config['DATABASE_PATH']):
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    backup_filename = f'pbo_database_backup_{timestamp}.db'
                    backup_path = os.path.join(app.config['BACKUP_FOLDER'], backup_filename)
                    shutil.copy2(app.config['DATABASE_PATH'], backup_path)
                    print(f"[UPLOAD] Database backup created: {backup_path}")
            except Exception as e:
                print(f"[UPLOAD INFO] Database backup skipped (using MySQL): {str(e)}")
            
            # Check if replace mode is enabled
            replace_mode = request.form.get('replace_mode', 'false').lower() == 'true'
            
            if replace_mode:
                print("[UPLOAD] Replace mode enabled - clearing existing data...")
                try:
                    # Clear all data first
                    db_helper.delete_all_operations()
                    db.session.commit()
                    print("[UPLOAD] Cleared all operations")
                    
                    db_helper.delete_all_doctors()
                    db.session.commit()
                    print("[UPLOAD] Cleared all doctors")
                    
                    db_helper.delete_all_tindakan_items()
                    db.session.commit()
                    print("[UPLOAD] Cleared all tindakan items")
                except Exception as e:
                    db.session.rollback()
                    print(f"[UPLOAD ERROR] Failed to clear data: {str(e)}")
                    flash(f'Gagal menghapus data lama: {str(e)}', 'danger')
                    return redirect(url_for('upload_database'))
            else:
                # Non-replace mode: keep existing data and append new data
                print("[UPLOAD] Non-replace mode - KEEPING existing data")
            
            # Import data from Excel
            try:
                import_stats = import_excel_to_database(upload_path, db_helper)
            except Exception as import_error:
                # Clean up uploaded file
                time.sleep(0.5)  # Give Windows time to release file lock
                if os.path.exists(upload_path):
                    try:
                        os.remove(upload_path)
                    except Exception as del_error:
                        print(f"[UPLOAD WARNING] Could not delete uploaded file: {str(del_error)}")
                flash(f'Error saat import data: {str(import_error)}', 'danger')
                return redirect(url_for('upload_database'))
            
            # Clean up uploaded file
            time.sleep(0.5)  # Give Windows time to release file lock
            if os.path.exists(upload_path):
                try:
                    os.remove(upload_path)
                except Exception as del_error:
                    print(f"[UPLOAD WARNING] Could not delete uploaded file after import: {str(del_error)}")
            
            # Prepare success data
            upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            return render_template('upload_success.html',
                                 filename=filename,
                                 upload_time=upload_time,
                                 operations_imported=import_stats['operations_imported'],
                                 operations_skipped=import_stats['operations_skipped'],
                                 doctors_imported=import_stats['doctors_imported'],
                                 doctors_duplicates=import_stats['doctors_duplicates'],
                                 doctors_skipped=import_stats['doctors_skipped'],
                                 tindakan_imported=import_stats['tindakan_imported'],
                                 tindakan_skipped=import_stats['tindakan_skipped'],
                                 total_operations=len(db_helper.get_all_operations()),
                                 total_doctors=db_helper.count_doctors(),
                                 total_tindakan=db_helper.count_tindakan_items(),
                                 backup_path=backup_path,
                                 warnings=import_stats.get('warnings', []))
            
        except Exception as e:
            flash(f'Terjadi kesalahan saat upload: {str(e)}', 'danger')
            return redirect(url_for('upload_database'))
    
    # GET request - show upload form
    return render_template('upload_database.html')

@app.route('/download-template', methods=['GET'])
@login_required
def download_template():
    """Download Excel template for database import"""
    try:
        # Create workbook
        wb = openpyxl.Workbook()
        wb.remove(wb.active)  # Remove default sheet
        
        # Define styles
        header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF', size=11)
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        center_alignment = Alignment(horizontal='center', vertical='center')
        
        # Sheet 1: db table operasi
        ws1 = wb.create_sheet('db table operasi')
        headers1 = ['No', 'Fee Operator', 'Kelas', 'Harga Operator', 'Harga Anestesi']
        
        for col, header in enumerate(headers1, 1):
            cell = ws1.cell(row=1, column=col, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.border = border
            cell.alignment = center_alignment
        
        # Add sample data
        sample_data1 = [
            [1, 'OPERASI MAYOR', 'BASIC', 2000000, 500000],
            [2, 'OPERASI MINOR', 'STANDARD', 1000000, 250000],
            [3, 'KONSULTASI', 'VIP', 500000, 100000],
        ]
        
        for row_idx, row_data in enumerate(sample_data1, 2):
            for col_idx, value in enumerate(row_data, 1):
                cell = ws1.cell(row=row_idx, column=col_idx, value=value)
                cell.border = border
                if col_idx > 1:
                    cell.alignment = center_alignment
        
        # Set column widths
        ws1.column_dimensions['A'].width = 5
        ws1.column_dimensions['B'].width = 25
        ws1.column_dimensions['C'].width = 15
        ws1.column_dimensions['D'].width = 18
        ws1.column_dimensions['E'].width = 18
        
        # Sheet 2: db nama dokter
        ws2 = wb.create_sheet('db nama dokter')
        headers2 = ['No', 'Nama Dokter']
        
        for col, header in enumerate(headers2, 1):
            cell = ws2.cell(row=1, column=col, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.border = border
            cell.alignment = center_alignment
        
        # Add sample data
        sample_data2 = [
            [1, 'Dr. Budi Santoso'],
            [2, 'Dr. Siti Nurhaliza'],
            [3, 'Dr. Ahmad Wijaya'],
        ]
        
        for row_idx, row_data in enumerate(sample_data2, 2):
            for col_idx, value in enumerate(row_data, 1):
                cell = ws2.cell(row=row_idx, column=col_idx, value=value)
                cell.border = border
                if col_idx > 1:
                    cell.alignment = center_alignment
        
        # Set column widths
        ws2.column_dimensions['A'].width = 5
        ws2.column_dimensions['B'].width = 30
        
        # Sheet 3: db nama tindakan
        ws3 = wb.create_sheet('db nama tindakan')
        headers3 = ['No', 'Nama Tindakan', 'Kelas', 'Kategory', 'Sales Item Type', 'Amount']
        
        for col, header in enumerate(headers3, 1):
            cell = ws3.cell(row=1, column=col, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.border = border
            cell.alignment = center_alignment
        
        # Add sample data
        sample_data3 = [
            [1, 'Obat Anestesi', 'BASIC', 'Obat', 'Medicine', 150000],
            [2, 'Alat Steril', 'STANDARD', 'Alat', 'Equipment', 200000],
            [3, 'Transfusi Darah', 'VIP', 'Layanan', 'Service', 500000],
        ]
        
        for row_idx, row_data in enumerate(sample_data3, 2):
            for col_idx, value in enumerate(row_data, 1):
                cell = ws3.cell(row=row_idx, column=col_idx, value=value)
                cell.border = border
                if col_idx > 1:
                    cell.alignment = center_alignment
        
        # Set column widths
        ws3.column_dimensions['A'].width = 5
        ws3.column_dimensions['B'].width = 25
        ws3.column_dimensions['C'].width = 15
        ws3.column_dimensions['D'].width = 15
        ws3.column_dimensions['E'].width = 18
        ws3.column_dimensions['F'].width = 15
        
        # Save to BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        # Return file
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'template_pbo_database_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
        
    except Exception as e:
        flash(f'Terjadi kesalahan saat membuat template: {str(e)}', 'danger')
        return redirect(url_for('upload_database'))

# Template filters
@app.template_filter('currency')
def currency_filter(value):
    """Format number as currency"""
    return PBOCalculator.format_currency(value)

@app.template_filter('percentage')
def percentage_filter(value):
    """Format decimal as percentage"""
    try:
        return f"{int(float(value) * 100)}%"
    except (ValueError, TypeError):
        return "0%"

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
