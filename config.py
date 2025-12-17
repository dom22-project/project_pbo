import os

class Config:
    """Configuration class for Flask application"""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration - menggunakan db_baru.db
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'db_baru.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application settings
    APP_NAME = 'Sistem Manajemen PBO - RS Siloam TB Simatupang'
    HOSPITAL_NAME = 'RS Siloam TB Simatupang'
    HOSPITAL_ADDRESS = 'Jl. RA Kartini No. 08 Cilandak'
    HOSPITAL_CITY = 'Jakarta Selatan 12430'
    HOSPITAL_PHONE = '(021) 29531900 Ext. 29790'
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Room rates mapping
    ROOM_RATES = {
        'BASIC': 350000,
        'STANDARD': 650000,
        'DELUXE': 900000,
        'VIP': 1800000,
        'VVIP': 1900000,
        'SUITE': 5000000,
        'PRESIDENTIAL SUITE': 7500000,
        'ODC': 500000
    }
    
    # Surcharge rates
    SURCHARGE_RATES = {
        'Elektif / Tentative': 1.0,
        'CITO': 1.25,
        'Penyulit': 1.30
    }
    
    # OT Room Charge percentage
    OT_ROOM_CHARGE_PERCENTAGE = 0.30
    
    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'xlsx'}
    
    # Backup settings
    BACKUP_FOLDER = os.path.join(BASE_DIR, 'backups')
    
    # PDF settings
    PDF_FOLDER = os.path.join(BASE_DIR, 'static', 'pdf')
