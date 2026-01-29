-- PBO Database Backup
-- Backup Date: 2026-01-29 11:29:05
-- Database: pbo_db
-- Charset: utf8mb4


-- Table: doctors
DROP TABLE IF EXISTS doctors;
CREATE TABLE `doctors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_dokter` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nama_dokter` (`nama_dokter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table: operation_tables
DROP TABLE IF EXISTS operation_tables;
CREATE TABLE `operation_tables` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kode` varchar(50) NOT NULL,
  `nama_tindakan` varchar(255) DEFAULT NULL,
  `kelas` varchar(50) DEFAULT NULL,
  `biaya_dokter` decimal(15,2) DEFAULT '0.00',
  `biaya_rs` decimal(15,2) DEFAULT '0.00',
  `total_biaya` decimal(15,2) DEFAULT '0.00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `kode` (`kode`),
  KEY `idx_kode` (`kode`),
  KEY `idx_kelas` (`kelas`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

-- Inserting 3 records into operation_tables
INSERT INTO operation_tables (id, kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya) VALUES (1, '4199999994', 'DOCTORS PROCEDURE TABLE 3', 'ODC', '4934000.00', '0.00', '4934000.00');
INSERT INTO operation_tables (id, kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya) VALUES (2, '4199999995', 'DOCTORS PROCEDURE TABLE 1', 'ODC', '1125000.00', '0.00', '1125000.00');
INSERT INTO operation_tables (id, kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya) VALUES (3, '4199999996', 'DOCTORS PROCEDURE TABLE 2', 'ODC', '2368000.00', '0.00', '2368000.00');


-- Table: paket_tindakan
DROP TABLE IF EXISTS paket_tindakan;
CREATE TABLE `paket_tindakan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pbo_id` int(11) NOT NULL,
  `tindakan_id` int(11) DEFAULT NULL,
  `nama_tindakan` varchar(255) DEFAULT NULL,
  `kategory` varchar(100) DEFAULT NULL,
  `harga` decimal(15,2) DEFAULT '0.00',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_pbo_id` (`pbo_id`),
  KEY `idx_tindakan_id` (`tindakan_id`),
  CONSTRAINT `fk_paket_pbo` FOREIGN KEY (`pbo_id`) REFERENCES `pbo_data` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_paket_tindakan` FOREIGN KEY (`tindakan_id`) REFERENCES `tindakan_items` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table: pbo_data
DROP TABLE IF EXISTS pbo_data;
CREATE TABLE `pbo_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `diagnosa` varchar(255) DEFAULT NULL,
  `nama_operasi` varchar(255) DEFAULT NULL,
  `sifat_operasi` varchar(100) DEFAULT NULL,
  `nama_dokter` varchar(255) DEFAULT NULL,
  `kelas` varchar(50) DEFAULT NULL,
  `tabel_operasi1` varchar(50) DEFAULT NULL,
  `tabel_operasi2` varchar(50) DEFAULT NULL,
  `tabel_operasi3` varchar(50) DEFAULT NULL,
  `tabel_operasi4` varchar(50) DEFAULT NULL,
  `persentase_operasi1` float DEFAULT '1',
  `persentase_operasi2` float DEFAULT '1',
  `persentase_operasi3` float DEFAULT '1',
  `persentase_operasi4` float DEFAULT '1',
  `konsultasi_pre_tindakan` decimal(15,2) DEFAULT '0.00',
  `diagnostic_pre_tindakan` decimal(15,2) DEFAULT '0.00',
  `surgeon` decimal(15,2) DEFAULT '0.00',
  `anesthesi` decimal(15,2) DEFAULT '0.00',
  `ot_room_charge` decimal(15,2) DEFAULT '0.00',
  `recovery_room_charge` decimal(15,2) DEFAULT '0.00',
  `alat` decimal(15,2) DEFAULT '0.00',
  `diagnostic` decimal(15,2) DEFAULT '0.00',
  `medical_equipment` decimal(15,2) DEFAULT '0.00',
  `obat_dan_alkes` decimal(15,2) DEFAULT '0.00',
  `tarif_kamar` decimal(15,2) DEFAULT '0.00',
  `total` decimal(15,2) DEFAULT '0.00',
  `catatan` text,
  `keterangan` text,
  `tanggal` date DEFAULT NULL,
  `nama_pasien` varchar(255) DEFAULT NULL,
  `hubungan_dengan_pasien` varchar(100) DEFAULT NULL,
  `petugas_front_office` varchar(255) DEFAULT NULL,
  `perusahaan_asuransi` varchar(255) DEFAULT NULL,
  `tindakan_tambahan` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `version_number` int(11) DEFAULT '1',
  `parent_id` int(11) DEFAULT NULL,
  `is_latest` int(11) DEFAULT '1',
  `edited_by` varchar(255) DEFAULT NULL,
  `edited_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table: room_types
DROP TABLE IF EXISTS room_types;
CREATE TABLE `room_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_kamar` varchar(100) NOT NULL,
  `harga_per_hari` decimal(15,2) NOT NULL,
  `deskripsi` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nama_kamar` (`nama_kamar`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

-- Inserting 7 records into room_types
INSERT INTO room_types (id, nama_kamar, harga_per_hari, deskripsi, created_at, updated_at) VALUES (1, 'Basic', '350000.00', 'Ruang rawat dengan fasilitas dasar', '2026-01-29 11:20:24', '2026-01-29 11:20:24');
INSERT INTO room_types (id, nama_kamar, harga_per_hari, deskripsi, created_at, updated_at) VALUES (2, 'Standard', '750000.00', 'Ruang rawat standar', '2026-01-29 11:20:24', '2026-01-29 11:20:24');
INSERT INTO room_types (id, nama_kamar, harga_per_hari, deskripsi, created_at, updated_at) VALUES (3, 'Deluxe', '950000.00', 'Ruang rawat premium', '2026-01-29 11:20:24', '2026-01-29 11:20:24');
INSERT INTO room_types (id, nama_kamar, harga_per_hari, deskripsi, created_at, updated_at) VALUES (4, 'VIP', '1900000.00', 'Ruang rawat VIP', '2026-01-29 11:20:24', '2026-01-29 11:20:24');
INSERT INTO room_types (id, nama_kamar, harga_per_hari, deskripsi, created_at, updated_at) VALUES (5, 'VVIP', '2000000.00', 'Ruang rawat VVIP', '2026-01-29 11:20:24', '2026-01-29 11:20:24');
INSERT INTO room_types (id, nama_kamar, harga_per_hari, deskripsi, created_at, updated_at) VALUES (6, 'Suite', '5000000.00', 'Ruang suite', '2026-01-29 11:20:24', '2026-01-29 11:20:24');
INSERT INTO room_types (id, nama_kamar, harga_per_hari, deskripsi, created_at, updated_at) VALUES (7, 'Presidential Suite', '7500000.00', 'Presidential suite', '2026-01-29 11:20:24', '2026-01-29 11:20:24');


-- Table: tindakan_items
DROP TABLE IF EXISTS tindakan_items;
CREATE TABLE `tindakan_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_tindakan` varchar(255) DEFAULT NULL,
  `kelas` varchar(50) DEFAULT NULL,
  `kategory` varchar(100) DEFAULT NULL,
  `sales_item_type` varchar(100) DEFAULT NULL,
  `amount` decimal(15,2) DEFAULT '0.00',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_nama_tindakan` (`nama_tindakan`(191)),
  KEY `idx_kelas` (`kelas`),
  KEY `idx_kategory` (`kategory`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table: users
DROP TABLE IF EXISTS users;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- Inserting 2 records into users
INSERT INTO users (id, username, password, role, created_at) VALUES (1, 'admin', 'admin123', 'admin', '2026-01-29 11:20:24');
INSERT INTO users (id, username, password, role, created_at) VALUES (2, 'user', 'user123', 'user', '2026-01-29 11:20:24');


-- Backup completed
-- Total records: 12
