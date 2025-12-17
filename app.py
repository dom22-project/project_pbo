from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_file
from datetime import datetime
import os
import shutil
from functools import wraps
from werkzeug.utils import secure_filename
import openpyxl
from config import Config
from models import Database
from utils import PBOCalculator, FormValidator, ReportGenerator

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = Database()

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
        
        user = db.authenticate_user(username, password)
        
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
    total_pbo = db.count_latest_pbo()
    recent_pbo = db.get_all_latest_pbo(limit=5)
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
            
            # Get form data
            form_data = {
                'diagnosa': request.form.get('diagnosa', ''),
                'nama_operasi': request.form.get('nama_operasi', ''),
                'sifat_operasi': request.form.get('sifat_operasi', 'Elektif / Tentative'),
                'nama_dokter': request.form.get('nama_dokter', ''),
                'kelas': request.form.get('kelas', ''),
                'tabel_operasi1': request.form.get('tabel_operasi1', ''),
                'tabel_operasi2': request.form.get('tabel_operasi2', ''),
                'tabel_operasi3': request.form.get('tabel_operasi3', ''),
                'tabel_operasi4': request.form.get('tabel_operasi4', ''),
                'persentase_operasi1': safe_percentage_convert(request.form.get('persentase_operasi1', 100)),
                'persentase_operasi2': safe_percentage_convert(request.form.get('persentase_operasi2', 100)),
                'persentase_operasi3': safe_percentage_convert(request.form.get('persentase_operasi3', 100)),
                'persentase_operasi4': safe_percentage_convert(request.form.get('persentase_operasi4', 100)),
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
            
            # Prepare data tuple for database
            data = (
                form_data['diagnosa'],
                form_data['nama_operasi'],
                form_data['sifat_operasi'],
                form_data['nama_dokter'],
                form_data['kelas'],
                form_data['tabel_operasi1'],
                form_data['tabel_operasi2'],
                form_data['tabel_operasi3'],
                form_data['tabel_operasi4'],
                form_data['persentase_operasi1'],
                form_data['persentase_operasi2'],
                form_data['persentase_operasi3'],
                form_data['persentase_operasi4'],
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
            pbo_id = db.create_pbo(data)
            
            flash(f'Data PBO berhasil disimpan dengan ID: {pbo_id}', 'success')
            return redirect(url_for('detail_pbo', pbo_id=pbo_id))
            
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('input_pbo'))
    
    # GET request - show form
    operations = db.get_all_operations()
    doctors = db.get_all_doctors()
    print(operations)
    tindakan_items = db.get_all_tindakan_items()
    
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
            results = db.search_latest_pbo(search_field, search_value)
            search_performed = True
        else:
            results = db.get_all_latest_pbo(limit=100)
            search_performed = True
    
    return render_template('search_pbo.html', 
                         results=results,
                         search_performed=search_performed)

@app.route('/detail/<int:pbo_id>')
@login_required
def detail_pbo(pbo_id):
    """View PBO detail"""
    pbo_data = db.get_pbo_by_id(pbo_id)
    
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
            
            # Get form data (same as input_pbo)
            form_data = {
                'diagnosa': request.form.get('diagnosa', ''),
                'nama_operasi': request.form.get('nama_operasi', ''),
                'sifat_operasi': request.form.get('sifat_operasi', 'Elektif / Tentative'),
                'nama_dokter': request.form.get('nama_dokter', ''),
                'kelas': request.form.get('kelas', ''),
                'tabel_operasi1': request.form.get('tabel_operasi1', ''),
                'tabel_operasi2': request.form.get('tabel_operasi2', ''),
                'tabel_operasi3': request.form.get('tabel_operasi3', ''),
                'tabel_operasi4': request.form.get('tabel_operasi4', ''),
                'persentase_operasi1': safe_percentage_convert(request.form.get('persentase_operasi1', 100)),
                'persentase_operasi2': safe_percentage_convert(request.form.get('persentase_operasi2', 100)),
                'persentase_operasi3': safe_percentage_convert(request.form.get('persentase_operasi3', 100)),
                'persentase_operasi4': safe_percentage_convert(request.form.get('persentase_operasi4', 100)),
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
            
            # Prepare data tuple
            data = (
                form_data['diagnosa'], form_data['nama_operasi'], form_data['sifat_operasi'],
                form_data['nama_dokter'], form_data['kelas'], form_data['tabel_operasi1'],
                form_data['tabel_operasi2'], form_data['tabel_operasi3'], form_data['tabel_operasi4'],
                form_data['persentase_operasi1'], form_data['persentase_operasi2'],
                form_data['persentase_operasi3'], form_data['persentase_operasi4'],
                form_data['konsultasi_pre_tindakan'], form_data['diagnostic_pre_tindakan'],
                form_data['surgeon'], form_data['anesthesi'], form_data['ot_room_charge'],
                form_data['recovery_room_charge'], form_data['alat'], form_data['diagnostic'],
                form_data['medical_equipment'], form_data['obat_dan_alkes'], form_data['tarif_kamar'],
                form_data['total'], form_data['catatan'], form_data['keterangan'],
                form_data['tanggal'], form_data['nama_pasien'], form_data['hubungan_dengan_pasien'],
                form_data['petugas_front_office'], form_data['perusahaan_asuransi']
            )
            
            # Create new version instead of updating
            new_version_id = db.create_pbo_version(
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
    pbo_data = db.get_pbo_by_id(pbo_id)
    
    if not pbo_data:
        flash('Data PBO tidak ditemukan', 'danger')
        return redirect(url_for('search_pbo'))
    
    operations = db.get_all_operations()
    doctors = db.get_all_doctors()
    return render_template('edit_pbo.html', 
                         pbo=pbo_data,
                         operations=operations,
                         doctors=doctors)

@app.route('/delete/<int:pbo_id>', methods=['POST'])
@admin_required
def delete_pbo(pbo_id):
    """Delete PBO record - Admin only"""
    try:
        db.delete_pbo(pbo_id)
        flash('Data PBO berhasil dihapus', 'success')
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('search_pbo'))

@app.route('/print/<int:pbo_id>')
@login_required
def print_pbo(pbo_id):
    """Print PBO form"""
    pbo_data = db.get_pbo_by_id(pbo_id)
    
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
    versions = db.get_pbo_versions(pbo_id)
    
    if not versions:
        flash('Data PBO tidak ditemukan', 'danger')
        return redirect(url_for('search_pbo'))
    
    # Get current PBO data for context
    current_pbo = db.get_pbo_by_id(pbo_id)
    
    return render_template('pbo_history.html', 
                         versions=versions,
                         current_pbo=current_pbo)

@app.route('/compare/<int:version1_id>/<int:version2_id>')
@login_required
def compare_versions(version1_id, version2_id):
    """Compare two versions of PBO"""
    comparison = db.compare_pbo_versions(version1_id, version2_id)
    
    if not comparison:
        flash('Versi tidak ditemukan', 'danger')
        return redirect(url_for('search_pbo'))
    
    return render_template('pbo_compare.html', 
                         comparison=comparison)

@app.route('/restore/<int:version_id>', methods=['POST'])
@login_required
def restore_version(version_id):
    """Restore a previous version"""
    try:
        restored_id = db.restore_pbo_version(
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
@app.route('/api/calculate-surgery-fees', methods=['POST'])
def api_calculate_surgery_fees():
    """API endpoint to calculate surgery fees"""
    try:
        data = request.get_json()
        
        operations_data = []
        for i in range(1, 5):
            kode = data.get(f'tabel_operasi{i}')
            if kode:
                operations_data.append({
                    'kode': kode,
                    'persentase': float(data.get(f'persentase_operasi{i}', 100))
                })
        
        sifat_operasi = data.get('sifat_operasi', 'Elektif / Tentative')
        
        result = PBOCalculator.calculate_surgery_fees(operations_data, sifat_operasi, db)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
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
            tindakan_items = db.get_all_tindakan_items()
            operations = db.get_all_operations()
        else:
            # Filter by kelas
            tindakan_items = db.get_tindakan_by_kelas(kelas)
            operations = db.get_operations_by_kelas(kelas)
        
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
    tindakan_items = db.get_all_tindakan_items()
    total_items = db.count_tindakan_items()
    
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
            
            db.add_tindakan_item(nama_tindakan, kelas, kategory, sales_item_type, amount)
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
            
            db.update_tindakan_item(tindakan_id, nama_tindakan, kelas, kategory, sales_item_type, amount)
            flash('Tindakan berhasil diupdate!', 'success')
            return redirect(url_for('view_tindakan'))
            
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('edit_tindakan', tindakan_id=tindakan_id))
    
    tindakan = db.get_tindakan_by_id(tindakan_id)
    if not tindakan:
        flash('Tindakan tidak ditemukan!', 'danger')
        return redirect(url_for('view_tindakan'))
    
    return render_template('edit_tindakan.html', tindakan=tindakan)

@app.route('/tindakan/delete/<int:tindakan_id>', methods=['POST'])
@admin_required
def delete_tindakan(tindakan_id):
    """Delete tindakan item"""
    try:
        db.delete_tindakan_item(tindakan_id)
        flash('Tindakan berhasil dihapus!', 'success')
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('view_tindakan'))

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
                required_sheets = ['db table operasi', 'db nama dokter']
                missing_sheets = [sheet for sheet in required_sheets if sheet not in wb.sheetnames]
                
                if missing_sheets:
                    os.remove(upload_path)
                    flash(f'File Excel tidak memiliki sheet yang diperlukan: {", ".join(missing_sheets)}', 'danger')
                    return redirect(url_for('upload_database'))
                
                wb.close()
            except Exception as e:
                if os.path.exists(upload_path):
                    os.remove(upload_path)
                flash(f'File Excel tidak valid: {str(e)}', 'danger')
                return redirect(url_for('upload_database'))
            
            # Backup current database
            backup_path = None
            if os.path.exists(app.config['DATABASE_PATH']):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_filename = f'pbo_database_backup_{timestamp}.db'
                backup_path = os.path.join(app.config['BACKUP_FOLDER'], backup_filename)
                shutil.copy2(app.config['DATABASE_PATH'], backup_path)
            
            # Import data from Excel
            import_stats = import_excel_to_database(upload_path, db)
            
            # Clean up uploaded file
            os.remove(upload_path)
            
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
                                 total_operations=len(db.get_all_operations()),
                                 total_doctors=db.count_doctors(),
                                 total_tindakan=db.count_tindakan_items(),
                                 backup_path=backup_path)
            
        except Exception as e:
            flash(f'Terjadi kesalahan saat upload: {str(e)}', 'danger')
            return redirect(url_for('upload_database'))
    
    # GET request - show upload form
    return render_template('upload_database.html')

def import_excel_to_database(excel_path, db):
    """Import data from Excel file to database"""
    stats = {
        'operations_imported': 0,
        'operations_skipped': 0,
        'doctors_imported': 0,
        'doctors_duplicates': 0,
        'doctors_skipped': 0,
        'tindakan_imported': 0,
        'tindakan_skipped': 0
    }
    
    try:
        wb = openpyxl.load_workbook(excel_path)
        
        # Import operations
        if 'db table operasi' in wb.sheetnames:
            ws = wb['db table operasi']
            
            # Clear existing operations
            db.delete_all_operations()
            
            # Import new operations
            for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    if not any(row):
                        continue
                    
                    fee_operator = row[1] if len(row) > 1 else None
                    kelas = row[2] if len(row) > 2 else None
                    harga_operator = row[3] if len(row) > 3 else None
                    harga_anestesi = row[4] if len(row) > 4 else None
                    
                    if not fee_operator or not kelas:
                        stats['operations_skipped'] += 1
                        continue
                    
                    fee_operator = str(fee_operator).strip()
                    kelas = str(kelas).strip()
                    
                    try:
                        harga_operator = float(harga_operator) if harga_operator else 0
                    except (ValueError, TypeError):
                        harga_operator = 0
                    
                    try:
                        harga_anestesi = float(harga_anestesi) if harga_anestesi else 0
                    except (ValueError, TypeError):
                        harga_anestesi = 0
                    
                    kode = f"OP{row_num:06d}"
                    
                    db.add_operation(
                        kode=kode,
                        nama_tindakan=fee_operator,
                        kelas=kelas,
                        biaya_dokter=harga_operator,
                        biaya_rs=harga_anestesi
                    )
                    
                    stats['operations_imported'] += 1
                    
                except Exception:
                    stats['operations_skipped'] += 1
                    continue
        
        # Import doctors
        if 'db nama dokter' in wb.sheetnames:
            ws = wb['db nama dokter']
            
            # Clear existing doctors
            db.delete_all_doctors()
            
            # Import new doctors
            for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    if not any(row):
                        continue
                    
                    nama_dokter = row[1] if len(row) > 1 else None
                    
                    if not nama_dokter:
                        stats['doctors_skipped'] += 1
                        continue
                    
                    nama_dokter = str(nama_dokter).strip()
                    
                    if not nama_dokter:
                        stats['doctors_skipped'] += 1
                        continue
                    
                    result = db.add_doctor(nama_dokter)
                    
                    if result:
                        stats['doctors_imported'] += 1
                    else:
                        stats['doctors_duplicates'] += 1
                    
                except Exception:
                    stats['doctors_skipped'] += 1
                    continue
        
        # Import tindakan items
        if 'db nama tindakan' in wb.sheetnames:
            ws = wb['db nama tindakan']
            
            # Clear existing tindakan items
            db.delete_all_tindakan_items()
            
            # Import new tindakan items
            for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    if not any(row):
                        continue
                    
                    nama_tindakan = row[1] if len(row) > 1 else None
                    kelas = row[2] if len(row) > 2 else None
                    kategory = row[3] if len(row) > 3 else None
                    sales_item_type = row[4] if len(row) > 4 else None
                    amount = row[5] if len(row) > 5 else None
                    
                    if not nama_tindakan:
                        stats['tindakan_skipped'] += 1
                        continue
                    
                    nama_tindakan = str(nama_tindakan).strip()
                    kelas = str(kelas).strip() if kelas else ''
                    kategory = str(kategory).strip() if kategory else ''
                    sales_item_type = str(sales_item_type).strip() if sales_item_type else ''
                    
                    try:
                        amount = float(amount) if amount else 0
                    except (ValueError, TypeError):
                        amount = 0
                    
                    db.add_tindakan_item(
                        nama_tindakan=nama_tindakan,
                        kelas=kelas,
                        kategory=kategory,
                        sales_item_type=sales_item_type,
                        amount=amount
                    )
                    
                    stats['tindakan_imported'] += 1
                    
                except Exception:
                    stats['tindakan_skipped'] += 1
                    continue
        
        wb.close()
        
    except Exception as e:
        raise Exception(f"Error importing data: {str(e)}")
    
    return stats

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
