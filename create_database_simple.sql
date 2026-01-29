-- MySQL Database Schema untuk PBO Management System
-- RS Siloam TB Simatupang

CREATE DATABASE IF NOT EXISTS pbo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE pbo_db;

-- Table: users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: operation_tables
CREATE TABLE IF NOT EXISTS operation_tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode VARCHAR(50) UNIQUE NOT NULL,
    nama_tindakan VARCHAR(255),
    kelas VARCHAR(50),
    biaya_dokter DECIMAL(15, 2) DEFAULT 0,
    biaya_rs DECIMAL(15, 2) DEFAULT 0,
    total_biaya DECIMAL(15, 2) DEFAULT 0,
    INDEX idx_kode (kode),
    INDEX idx_kelas (kelas)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: doctors
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_dokter VARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nama_dokter (nama_dokter)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: tindakan_items
CREATE TABLE IF NOT EXISTS tindakan_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_tindakan VARCHAR(255),
    kelas VARCHAR(50),
    kategory VARCHAR(100),
    sales_item_type VARCHAR(100),
    amount DECIMAL(15, 2) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nama_tindakan (nama_tindakan),
    INDEX idx_kelas (kelas),
    INDEX idx_kategory (kategory)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: room_types
CREATE TABLE IF NOT EXISTS room_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_kamar VARCHAR(255) UNIQUE NOT NULL,
    harga_per_hari DECIMAL(15, 2) NOT NULL,
    deskripsi TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nama_kamar (nama_kamar)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: database (PBO Data)
CREATE TABLE IF NOT EXISTS database (
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
    edited_at DATETIME,
    INDEX idx_nama_pasien (nama_pasien),
    INDEX idx_tanggal (tanggal),
    INDEX idx_nama_dokter (nama_dokter),
    INDEX idx_nama_operasi (nama_operasi),
    INDEX idx_created_at (created_at),
    INDEX idx_is_latest (is_latest)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: paket_tindakan
CREATE TABLE IF NOT EXISTS paket_tindakan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pbo_id INT NOT NULL,
    tindakan_id INT,
    nama_tindakan VARCHAR(255),
    kategory VARCHAR(100),
    harga DECIMAL(15, 2) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_pbo_id (pbo_id),
    INDEX idx_tindakan_id (tindakan_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default users
INSERT IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin');
INSERT IGNORE INTO users (username, password, role) VALUES ('user', 'user123', 'user');

-- Insert default room types
INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('Basic', 350000, 'Ruang rawat dengan fasilitas dasar');
INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('Standard', 750000, 'Ruang rawat standar dengan fasilitas lengkap');
INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('Deluxe', 950000, 'Ruang rawat dengan fasilitas premium');
INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('VIP', 1900000, 'Ruang rawat VIP dengan fasilitas mewah');
INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('VVIP', 2000000, 'Ruang rawat VVIP dengan fasilitas eksklusif');
INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('Suite', 5000000, 'Ruang suite dengan private facilities');
INSERT IGNORE INTO room_types (nama_kamar, harga_per_hari, deskripsi) VALUES ('Presidential Suite', 7500000, 'Presidential suite dengan fasilitas tertinggi');

-- Insert default operations
INSERT IGNORE INTO operation_tables (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya) VALUES ('4199999994', 'DOCTORS PROCEDURE TABLE 3', 'ODC', 4934000, 0, 4934000);
INSERT IGNORE INTO operation_tables (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya) VALUES ('4199999995', 'DOCTORS PROCEDURE TABLE 1', 'ODC', 1125000, 0, 1125000);
INSERT IGNORE INTO operation_tables (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya) VALUES ('4199999996', 'DOCTORS PROCEDURE TABLE 2', 'ODC', 2368000, 0, 2368000);
