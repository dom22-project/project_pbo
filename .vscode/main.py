import sys
import sqlite3
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QTabWidget, QMessageBox, QGroupBox, QGridLayout,
                             QDateEdit, QTextEdit, QHeaderView)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QDoubleValidator

class PBOForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Manajemen PBO - RS Sumber Hidup")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize database
        self.init_db()
        
        # Create main widget and layout
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create tabs
        self.input_tab = QWidget()
        self.search_tab = QWidget()
        
        self.central_widget.addTab(self.input_tab, "Input Data PBO")
        self.central_widget.addTab(self.search_tab, "Cari Data PBO")
        
        # Setup tabs
        self.setup_input_tab()
        self.setup_search_tab()
        
    def init_db(self):
        # Create database directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
            
        self.conn = sqlite3.connect('data/pbo_database.db')
        self.cursor = self.conn.cursor()
        
        # Create table if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pbo_data (
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
                perusahaan_asuransi TEXT
            )
        ''')
        self.conn.commit()
    
    def setup_input_tab(self):
        layout = QVBoxLayout()
        
        # Header section
        header_group = QGroupBox("Informasi Rumah Sakit")
        header_layout = QVBoxLayout()
        
        header_info = QLabel("Jl. RA Kartini No. 08 Cilandak\nJakarta Selatan 12430\nTelp. (021) 29531900 Ext. 29790")
        header_info.setAlignment(Qt.AlignCenter)
        header_info.setFont(QFont("Arial", 10, QFont.Bold))
        
        title = QLabel("PERKIRAAN BIAYA OPERASI")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 12, QFont.Bold))
        
        header_layout.addWidget(header_info)
        header_layout.addWidget(title)
        header_group.setLayout(header_layout)
        
        # Form section
        form_group = QGroupBox("Data PBO")
        form_layout = QGridLayout()
        
        # Form fields
        self.fields = {}
        labels = [
            "Diagnosa", "Nama Operasi", "Sifat Operasi", "Nama Dokter", 
            "Kelas", "Tabel Operasi 1", "Tabel Operasi 2", "Tabel Operasi 3", 
            "Tabel Operasi 4", "Konsultasi Pre Tindakan", "Diagnostic Pre Tindakan",
            "Surgeon", "Anesthesi", "OT Room Charge", "Recovery Room Charge",
            "Alat", "Diagnostic", "Medical Equipment", "Obat dan Alkes",
            "Tarif Kamar per Hari", "Total", "Catatan", "Keterangan",
            "Tanggal", "Nama Pasien", "Hubungan dengan Pasien",
            "Petugas Front Office", "Perusahaan/Asuransi Penanggung"
        ]
        
        # Validator for numeric fields
        double_validator = QDoubleValidator()
        
        for i, label in enumerate(labels):
            form_layout.addWidget(QLabel(label), i, 0)
            if label == "Sifat Operasi":
                field = QComboBox()
                field.addItems(["Elektif", "CITO", "Penyulit"])
            elif label == "Kelas":
                field = QComboBox()
                field.addItems(["BASIC", "STANDARD", "DELUXE", "VIP", "VVIP", "SUITE", "PRESIDENTIAL SUITE", "ODC"])
            elif label == "Tanggal":
                field = QDateEdit()
                field.setDate(QDate.currentDate())
                field.setCalendarPopup(True)
            elif label in ["Catatan", "Keterangan"]:
                field = QTextEdit()
                field.setMaximumHeight(100)
            elif label in ["Konsultasi Pre Tindakan", "Diagnostic Pre Tindakan",
                          "Surgeon", "Anesthesi", "OT Room Charge", "Recovery Room Charge",
                          "Alat", "Diagnostic", "Medical Equipment", "Obat dan Alkes",
                          "Tarif Kamar per Hari", "Total"]:
                field = QLineEdit()
                field.setValidator(double_validator)
                field.setText("0")
            else:
                field = QLineEdit()
            
            self.fields[label] = field
            form_layout.addWidget(field, i, 1)
        
        form_group.setLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Simpan Data")
        save_button.clicked.connect(self.save_data)
        save_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        
        clear_button = QPushButton("Bersihkan Form")
        clear_button.clicked.connect(self.clear_form)
        clear_button.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        
        calculate_button = QPushButton("Hitung Total")
        calculate_button.clicked.connect(self.calculate_total)
        calculate_button.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(calculate_button)
        
        # Add all to main layout
        layout.addWidget(header_group)
        layout.addWidget(form_group)
        layout.addLayout(button_layout)
        
        self.input_tab.setLayout(layout)
    
    def setup_search_tab(self):
        layout = QVBoxLayout()
        
        # Search section
        search_group = QGroupBox("Pencarian Data")
        search_layout = QGridLayout()
        
        search_layout.addWidget(QLabel("Cari berdasarkan:"), 0, 0)
        self.search_field = QComboBox()
        self.search_field.addItems(["Nama Pasien", "Nama Operasi", "Tanggal", "Diagnosa", "Nama Dokter"])
        search_layout.addWidget(self.search_field, 0, 1)
        
        search_layout.addWidget(QLabel("Kata kunci:"), 1, 0)
        self.search_input = QLineEdit()
        search_layout.addWidget(self.search_input, 1, 1)
        
        search_button = QPushButton("Cari")
        search_button.clicked.connect(self.search_data)
        search_button.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        search_layout.addWidget(search_button, 1, 2)
        
        search_group.setLayout(search_layout)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(8)
        self.results_table.setHorizontalHeaderLabels(["ID", "Nama Pasien", "Nama Operasi", "Diagnosa", "Dokter", "Kelas", "Tanggal", "Total Biaya"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.doubleClicked.connect(self.load_selected_data)
        
        # Buttons for search tab
        button_layout = QHBoxLayout()
        delete_button = QPushButton("Hapus Data Terpilih")
        delete_button.clicked.connect(self.delete_data)
        delete_button.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        
        export_button = QPushButton("Ekspor ke Excel")
        export_button.clicked.connect(self.export_to_excel)
        export_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        
        button_layout.addWidget(delete_button)
        button_layout.addWidget(export_button)
        
        layout.addWidget(search_group)
        layout.addWidget(self.results_table)
        layout.addLayout(button_layout)
        
        self.search_tab.setLayout(layout)
    
    def calculate_total(self):
        try:
            # Get all numeric values
            values = [
                float(self.fields["Konsultasi Pre Tindakan"].text() or 0),
                float(self.fields["Diagnostic Pre Tindakan"].text() or 0),
                float(self.fields["Surgeon"].text() or 0),
                float(self.fields["Anesthesi"].text() or 0),
                float(self.fields["OT Room Charge"].text() or 0),
                float(self.fields["Recovery Room Charge"].text() or 0),
                float(self.fields["Alat"].text() or 0),
                float(self.fields["Diagnostic"].text() or 0),
                float(self.fields["Medical Equipment"].text() or 0),
                float(self.fields["Obat dan Alkes"].text() or 0),
                float(self.fields["Tarif Kamar per Hari"].text() or 0)
            ]
            
            # Calculate total
            total = sum(values)
            self.fields["Total"].setText(str(total))
            
        except ValueError:
            QMessageBox.warning(self, "Peringatan", "Pastikan semua nilai biaya adalah angka yang valid.")
    
    def save_data(self):
        try:
            # Calculate total first
            self.calculate_total()
            
            # Collect data from form fields
            data = (
                self.fields["Diagnosa"].text(),
                self.fields["Nama Operasi"].text(),
                self.fields["Sifat Operasi"].currentText(),
                self.fields["Nama Dokter"].text(),
                self.fields["Kelas"].currentText(),
                self.fields["Tabel Operasi 1"].text(),
                self.fields["Tabel Operasi 2"].text(),
                self.fields["Tabel Operasi 3"].text(),
                self.fields["Tabel Operasi 4"].text(),
                float(self.fields["Konsultasi Pre Tindakan"].text() or 0),
                float(self.fields["Diagnostic Pre Tindakan"].text() or 0),
                float(self.fields["Surgeon"].text() or 0),
                float(self.fields["Anesthesi"].text() or 0),
                float(self.fields["OT Room Charge"].text() or 0),
                float(self.fields["Recovery Room Charge"].text() or 0),
                float(self.fields["Alat"].text() or 0),
                float(self.fields["Diagnostic"].text() or 0),
                float(self.fields["Medical Equipment"].text() or 0),
                float(self.fields["Obat dan Alkes"].text() or 0),
                float(self.fields["Tarif Kamar per Hari"].text() or 0),
                float(self.fields["Total"].text() or 0),
                self.fields["Catatan"].toPlainText(),
                self.fields["Keterangan"].toPlainText(),
                self.fields["Tanggal"].date().toString("yyyy-MM-dd"),
                self.fields["Nama Pasien"].text(),
                self.fields["Hubungan dengan Pasien"].text(),
                self.fields["Petugas Front Office"].text(),
                self.fields["Perusahaan/Asuransi Penanggung"].text()
            )
            
            # Insert into database
            self.cursor.execute('''
                INSERT INTO pbo_data (
                    diagnosa, nama_operasi, sifat_operasi, nama_dokter, kelas,
                    tabel_operasi1, tabel_operasi2, tabel_operasi3, tabel_operasi4,
                    konsultasi_pre_tindakan, diagnostic_pre_tindakan, surgeon,
                    anesthesi, ot_room_charge, recovery_room_charge, alat,
                    diagnostic, medical_equipment, obat_dan_alkes, tarif_kamar,
                    total, catatan, keterangan, tanggal, nama_pasien,
                    hubungan_dengan_pasien, petugas_front_office, perusahaan_asuransi
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)
            
            self.conn.commit()
            
            QMessageBox.information(self, "Sukses", "Data berhasil disimpan!")
            self.clear_form()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")
    
    def search_data(self):
        search_by = self.search_field.currentText()
        search_value = self.search_input.text()
        
        query = "SELECT id, nama_pasien, nama_operasi, diagnosa, nama_dokter, kelas, tanggal, total FROM pbo_data"
        
        if search_value:
            if search_by == "Nama Pasien":
                query += " WHERE nama_pasien LIKE ?"
                params = (f'%{search_value}%',)
            elif search_by == "Nama Operasi":
                query += " WHERE nama_operasi LIKE ?"
                params = (f'%{search_value}%',)
            elif search_by == "Tanggal":
                query += " WHERE tanggal = ?"
                params = (search_value,)
            elif search_by == "Diagnosa":
                query += " WHERE diagnosa LIKE ?"
                params = (f'%{search_value}%',)
            elif search_by == "Nama Dokter":
                query += " WHERE nama_dokter LIKE ?"
                params = (f'%{search_value}%',)
        else:
            # If no search value, show all records
            query += " ORDER BY id DESC LIMIT 100"
            params = ()
        
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        
        # Display results in table
        self.results_table.setRowCount(len(results))
        for row_idx, row_data in enumerate(results):
            for col_idx, col_data in enumerate(row_data):
                self.results_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        
        if not results:
            QMessageBox.information(self, "Pencarian", "Tidak ditemukan data yang sesuai.")
    
    def load_selected_data(self):
        selected_row = self.results_table.currentRow()
        if selected_row >= 0:
            record_id = self.results_table.item(selected_row, 0).text()
            
            # Fetch complete record
            self.cursor.execute("SELECT * FROM pbo_data WHERE id = ?", (record_id,))
            record = self.cursor.fetchone()
            
            # Populate form with the record
            if record:
                # Switch to input tab
                self.central_widget.setCurrentIndex(0)
                
                # Map record to form fields
                fields_mapping = [
                    "Diagnosa", "Nama Operasi", "Sifat Operasi", "Nama Dokter", 
                    "Kelas", "Tabel Operasi 1", "Tabel Operasi 2", "Tabel Operasi 3", 
                    "Tabel Operasi 4", "Konsultasi Pre Tindakan", "Diagnostic Pre Tindakan",
                    "Surgeon", "Anesthesi", "OT Room Charge", "Recovery Room Charge",
                    "Alat", "Diagnostic", "Medical Equipment", "Obat dan Alkes",
                    "Tarif Kamar per Hari", "Total", "Catatan", "Keterangan",
                    "Tanggal", "Nama Pasien", "Hubungan dengan Pasien",
                    "Petugas Front Office", "Perusahaan/Asuransi Penanggung"
                ]
                
                for i, field_name in enumerate(fields_mapping):
                    if field_name == "Sifat Operasi":
                        index = self.fields[field_name].findText(record[i+1])
                        if index >= 0:
                            self.fields[field_name].setCurrentIndex(index)
                    elif field_name == "Kelas":
                        index = self.fields[field_name].findText(record[i+1])
                        if index >= 0:
                            self.fields[field_name].setCurrentIndex(index)
                    elif field_name == "Tanggal":
                        date = QDate.fromString(record[i+1], "yyyy-MM-dd")
                        self.fields[field_name].setDate(date)
                    elif field_name in ["Catatan", "Keterangan"]:
                        self.fields[field_name].setText(record[i+1])
                    else:
                        self.fields[field_name].setText(str(record[i+1]))
    
    def delete_data(self):
        selected_row = self.results_table.currentRow()
        if selected_row >= 0:
            record_id = self.results_table.item(selected_row, 0).text()
            record_name = self.results_table.item(selected_row, 1).text()
            
            reply = QMessageBox.question(self, "Konfirmasi", 
                                        f"Apakah Anda yakin ingin menghapus data untuk {record_name}?",
                                        QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.cursor.execute("DELETE FROM pbo_data WHERE id = ?", (record_id,))
                self.conn.commit()
                
                QMessageBox.information(self, "Sukses", "Data berhasil dihapus!")
                self.search_data()  # Refresh the table
    
    def export_to_excel(self):
        QMessageBox.information(self, "Info", "Fitur ekspor ke Excel akan segera tersedia.")
    
    def clear_form(self):
        for field_name, field_widget in self.fields.items():
            if isinstance(field_widget, QComboBox):
                field_widget.setCurrentIndex(0)
            elif isinstance(field_widget, QDateEdit):
                field_widget.setDate(QDate.currentDate())
            elif isinstance(field_widget, QTextEdit):
                field_widget.clear()
            elif field_name in ["Konsultasi Pre Tindakan", "Diagnostic Pre Tindakan",
                              "Surgeon", "Anesthesi", "OT Room Charge", "Recovery Room Charge",
                              "Alat", "Diagnostic", "Medical Equipment", "Obat dan Alkes",
                              "Tarif Kamar per Hari", "Total"]:
                field_widget.setText("0")
            else:
                field_widget.clear()
    
    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PBOForm()
    window.show()
    sys.exit(app.exec_())