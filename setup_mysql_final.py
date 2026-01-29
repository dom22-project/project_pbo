#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL Setup - Ultra Simple
Direct statement execution
"""

import mysql.connector
from mysql.connector import Error
import sys

def setup():
    """Direct setup"""
    host = 'localhost'
    user = 'root'
    password = ''
    
    print("\n" + "="*70)
    print("🔧 MySQL Setup")
    print("="*70)
    
    print(f"\n📡 Connecting...")
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        print("✅ Connected")
    except Error as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    cursor = conn.cursor()
    
    # SQL Statements
    statements = [
        # Create database
        "CREATE DATABASE IF NOT EXISTS pbo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci",
        "USE pbo_db",
        
        # Create tables
        """CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        
        """CREATE TABLE IF NOT EXISTS operation_tables (
            id INT AUTO_INCREMENT PRIMARY KEY,
            kode VARCHAR(50) UNIQUE NOT NULL,
            nama_tindakan VARCHAR(255),
            kelas VARCHAR(50),
            biaya_dokter DECIMAL(15, 2) DEFAULT 0,
            biaya_rs DECIMAL(15, 2) DEFAULT 0,
            total_biaya DECIMAL(15, 2) DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        
        """CREATE TABLE IF NOT EXISTS doctors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama_dokter VARCHAR(100) UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        
        """CREATE TABLE IF NOT EXISTS tindakan_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama_tindakan VARCHAR(255),
            kelas VARCHAR(50),
            kategory VARCHAR(100),
            sales_item_type VARCHAR(100),
            amount DECIMAL(15, 2) DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        
        """CREATE TABLE IF NOT EXISTS room_types (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama_kamar VARCHAR(100) UNIQUE NOT NULL,
            harga_per_hari DECIMAL(15, 2) NOT NULL,
            deskripsi TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        
        """CREATE TABLE IF NOT EXISTS pbo_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            diagnosa VARCHAR(255),
            nama_operasi VARCHAR(255),
            sifat_operasi VARCHAR(100),
            nama_dokter VARCHAR(255),
            kelas VARCHAR(50),
            tabel_operasi1 VARCHAR(50),
            tabel_operasi2 VARCHAR(50),
            tabel_operasi3 VARCHAR(50),
            tabel_operasi4 VARCHAR(50),
            persentase_operasi1 FLOAT DEFAULT 1.0,
            persentase_operasi2 FLOAT DEFAULT 1.0,
            persentase_operasi3 FLOAT DEFAULT 1.0,
            persentase_operasi4 FLOAT DEFAULT 1.0,
            konsultasi_pre_tindakan DECIMAL(15, 2) DEFAULT 0,
            diagnostic_pre_tindakan DECIMAL(15, 2) DEFAULT 0,
            surgeon DECIMAL(15, 2) DEFAULT 0,
            anesthesi DECIMAL(15, 2) DEFAULT 0,
            ot_room_charge DECIMAL(15, 2) DEFAULT 0,
            recovery_room_charge DECIMAL(15, 2) DEFAULT 0,
            alat DECIMAL(15, 2) DEFAULT 0,
            diagnostic DECIMAL(15, 2) DEFAULT 0,
            medical_equipment DECIMAL(15, 2) DEFAULT 0,
            obat_dan_alkes DECIMAL(15, 2) DEFAULT 0,
            tarif_kamar DECIMAL(15, 2) DEFAULT 0,
            total DECIMAL(15, 2) DEFAULT 0,
            catatan TEXT,
            keterangan TEXT,
            tanggal DATE,
            nama_pasien VARCHAR(255),
            hubungan_dengan_pasien VARCHAR(100),
            petugas_front_office VARCHAR(255),
            perusahaan_asuransi VARCHAR(255),
            tindakan_tambahan TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            version_number INT DEFAULT 1,
            parent_id INT,
            is_latest INT DEFAULT 1,
            edited_by VARCHAR(255),
            edited_at DATETIME
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        
        """CREATE TABLE IF NOT EXISTS paket_tindakan (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pbo_id INT NOT NULL,
            tindakan_id INT,
            nama_tindakan VARCHAR(255),
            kategory VARCHAR(100),
            harga DECIMAL(15, 2) DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_paket_pbo FOREIGN KEY (pbo_id) REFERENCES pbo_data(id) ON DELETE CASCADE,
            CONSTRAINT fk_paket_tindakan FOREIGN KEY (tindakan_id) REFERENCES tindakan_items(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        
        # Insert users
        "INSERT IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')",
        "INSERT IGNORE INTO users (username, password, role) VALUES ('user', 'user123', 'user')",
        
        # Insert room types
        "INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('Basic', 350000, 'Ruang rawat dengan fasilitas dasar')",
        "INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('Standard', 750000, 'Ruang rawat standar')",
        "INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('Deluxe', 950000, 'Ruang rawat premium')",
        "INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('VIP', 1900000, 'Ruang rawat VIP')",
        "INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('VVIP', 2000000, 'Ruang rawat VVIP')",
        "INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('Suite', 5000000, 'Ruang suite')",
        "INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('Presidential Suite', 7500000, 'Presidential suite')",
        
        # Insert operations
        "INSERT IGNORE INTO operation_tables (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya) VALUES ('4199999994', 'DOCTORS PROCEDURE TABLE 3', 'ODC', 4934000, 0, 4934000)",
        "INSERT IGNORE INTO operation_tables (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya) VALUES ('4199999995', 'DOCTORS PROCEDURE TABLE 1', 'ODC', 1125000, 0, 1125000)",
        "INSERT IGNORE INTO operation_tables (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya) VALUES ('4199999996', 'DOCTORS PROCEDURE TABLE 2', 'ODC', 2368000, 0, 2368000)",
    ]
    
    print("\n📄 Executing SQL...")
    executed = 0
    
    for stmt in statements:
        try:
            cursor.execute(stmt)
            executed += 1
            
            # Show progress
            if 'CREATE TABLE' in stmt.upper():
                # Extract table name
                parts = stmt.split()
                idx = parts.index('IF') + 3  # Skip "IF NOT EXISTS"
                table = parts[idx]
                print(f"   ✅ Table: {table}")
            elif 'INSERT' in stmt.upper():
                pass
            elif 'CREATE DATABASE' in stmt.upper():
                print(f"   ✅ Database: pbo_db")
            elif 'USE' in stmt.upper():
                print(f"   ✅ Selected: pbo_db")
        except Error as e:
            if 'already exists' not in str(e) and 'Duplicate' not in str(e):
                print(f"   ⚠️  Error: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n✅ Setup completed ({executed} statements)")
    return True

if __name__ == '__main__':
    print("\n🚀 MySQL Setup\n")
    if setup():
        print("\n" + "="*70)
        print("✅ SUCCESS!")
        print("="*70)
        print("\nNext steps:")
        print("  python verify_database.py")
        print("  python app.py")
        print("="*70 + "\n")
        sys.exit(0)
    else:
        sys.exit(1)
