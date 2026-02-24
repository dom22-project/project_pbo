import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for Flask application"""

    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Secret key
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-in-production"
    )

    # =========================
    # DATABASE CONFIGURATION
    # =========================

    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

    # Build safe SQLAlchemy URL (handles special characters like @)
    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="mysql+pymysql",
        username=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        database=MYSQL_DATABASE,
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": int(os.getenv("DB_POOL_SIZE", 10)),
        "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", 3600)),
        "pool_pre_ping": True,
        "connect_args": {
            "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", 30)),
        },
    }

    # =========================
    # APPLICATION SETTINGS
    # =========================

    APP_NAME = os.getenv(
        "APP_NAME",
        "Sistem Manajemen PBO - RS Siloam TB Simatupang"
    )

    HOSPITAL_NAME = os.getenv(
        "HOSPITAL_NAME",
        "RS Siloam TB Simatupang"
    )

    HOSPITAL_ADDRESS = os.getenv(
        "HOSPITAL_ADDRESS",
        "Jl. RA Kartini No. 08 Cilandak"
    )

    HOSPITAL_CITY = os.getenv(
        "HOSPITAL_CITY",
        "Jakarta Selatan 12430"
    )

    HOSPITAL_PHONE = os.getenv(
        "HOSPITAL_PHONE",
        "(021) 29531900 Ext. 29790"
    )

    # =========================
    # PAGINATION & LIMITS
    # =========================

    ITEMS_PER_PAGE = int(os.getenv("ITEMS_PER_PAGE", 20))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 500))
    IMPORT_TIMEOUT = int(os.getenv("IMPORT_TIMEOUT", 600))
    QUERY_TIMEOUT = int(os.getenv("QUERY_TIMEOUT", 30))

    # =========================
    # OT ROOM CONFIGURATION
    # =========================

    OT_ROOM_CHARGE_PERCENTAGE = 0.30

    ROOM_RATES = {
        "BASIC": 350000,
        "STANDARD": 650000,
        "DELUXE": 900000,
        "VIP": 1800000,
        "VVIP": 1900000,
        "SUITE": 5000000,
        "PRESIDENTIAL SUITE": 7500000,
        "ODC": 500000,
        "OPD": 633000,
    }

    SURCHARGE_RATES = {
        "Elektif / Tentative": 1.0,
        "CITO": 1.25,
        "Penyulit": 1.30,
    }

    # =========================
    # FILE UPLOAD SETTINGS
    # =========================

    MAX_CONTENT_LENGTH = (
        int(os.getenv("MAX_UPLOAD_SIZE_MB", 16)) * 1024 * 1024
    )

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    ALLOWED_EXTENSIONS = {"xlsx"}

    # =========================
    # BACKUP & FILE STORAGE
    # =========================

    BACKUP_FOLDER = os.path.join(BASE_DIR, "backups")
    DATABASE_PATH = os.path.join(BASE_DIR, "pbo_database.db")

    PDF_FOLDER = os.path.join(BASE_DIR, "static", "pdf")
