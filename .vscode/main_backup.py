import sys
import sqlite3
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QTabWidget, QMessageBox, QGroupBox, QGridLayout,
                             QDateEdit, QTextEdit, QHeaderView)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QDoubleValidator, QIntValidator
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtGui import QTextDocument

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
        
        # Load data for comboboxes
        self.load_operation_tables()
        
    def init_db(self):
        # Create database directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
            
        self.conn = sqlite3.connect('data/pbo_database.db')
        self.cursor = self.conn.cursor()
        
        # Create main table if not exists
        self.cursor.execute('''
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create operation tables if not exists
        self.cursor.execute('''
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
        
        # Insert default operation tables if empty
        self.cursor.execute("SELECT COUNT(*) FROM operation_tables")
        if self.cursor.fetchone()[0] == 0:
            default_operations = [
            ('4199999994','DOCTORS PROCEDURE TABLE 3','ODC',4934000,0),
            ('4199999995','DOCTORS PROCEDURE TABLE 1','ODC',1125000,0),
            ('4199999996','DOCTORS PROCEDURE TABLE 2','ODC',2368000,0),

            ]
            self.cursor.executemany('''
                INSERT INTO operation_tables (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', default_operations)
        
        self.conn.commit()
    
    def load_operation_tables(self):
        # Load operation tables for combobox
        self.cursor.execute("SELECT kode, nama_tindakan FROM operation_tables")
        operations = self.cursor.fetchall()
        self.operation_list = [f"{op[0]} - {op[1]}" for op in operations]
        
        # Set the operation comboboxes
        for i in range(1, 5):
            self.fields[f"Tabel Operasi {i}"].clear()
            self.fields[f"Tabel Operasi {i}"].addItems([""] + self.operation_list)
    
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
        int_validator = QIntValidator()
        
        for i, label in enumerate(labels):
            form_layout.addWidget(QLabel(label), i, 0)
            if label == "Sifat Operasi":
                field = QComboBox()
                field.addItems(["Elektif / Tentative", "CITO", "Penyulit"])
                field.currentTextChanged.connect(self.calculate_surcharge)
            elif label == "Kelas":
                field = QComboBox()
                field.addItems(["", "BASIC", "STANDARD", "DELUXE", "VIP", "VVIP", "SUITE", "PRESIDENTIAL SUITE", "ODC"])
                field.currentTextChanged.connect(self.update_room_rate)
            elif label in ["Tabel Operasi 1", "Tabel Operasi 2", "Tabel Operasi 3", "Tabel Operasi 4"]:
                field = QComboBox()
                field.currentTextChanged.connect(self.calculate_surgery_fees)
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
                if label in ["Surgeon", "Anesthesi", "OT Room Charge", "Total"]:
                    field.setReadOnly(True)
                    field.setStyleSheet("background-color: #f0f0f0;")
            else:
                field = QLineEdit()
            
            self.fields[label] = field
            form_layout.addWidget(field, i, 1)
            
            # Add percentage fields for operation tables
            if label.startswith("Tabel Operasi"):
                op_num = label.split(" ")[2]
                percent_label = QLabel(f"Persentase Operasi {op_num}")
                percent_field = QComboBox()
                percent_field.addItems(["100%", "50%"])
                percent_field.setCurrentText("100%")
                percent_field.currentTextChanged.connect(self.calculate_surgery_fees)
                
                form_layout.addWidget(percent_label, i, 2)
                form_layout.addWidget(percent_field, i, 3)
                self.fields[f"Persentase Operasi {op_num}"] = percent_field
        
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
        
        print_button = QPushButton("Cetak Form")
        print_button.clicked.connect(self.print_form)
        print_button.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(calculate_button)
        button_layout.addWidget(print_button)
        
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
        
        print_button = QPushButton("Cetak Data Terpilih")
        print_button.clicked.connect(self.print_selected_data)
        print_button.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
        
        button_layout.addWidget(delete_button)
        button_layout.addWidget(export_button)
        button_layout.addWidget(print_button)
        
        layout.addWidget(search_group)
        layout.addWidget(self.results_table)
        layout.addLayout(button_layout)
        
        self.search_tab.setLayout(layout)
    
    def update_room_rate(self):
        kelas = self.fields["Kelas"].currentText()
        tarif_kamar = 0
        
        if kelas == "BASIC":
            tarif_kamar = 350000
        elif kelas == "STANDARD":
            tarif_kamar = 650000
        elif kelas == "DELUXE":
            tarif_kamar = 900000
        elif kelas == "VIP":
            tarif_kamar = 1800000
        elif kelas == "VVIP":
            tarif_kamar = 1900000
        elif kelas == "SUITE":
            tarif_kamar = 5000000
        elif kelas == "PRESIDENTIAL SUITE":
            tarif_kamar = 7500000
        elif kelas == "ODC":
            tarif_kamar = 500000
        
        self.fields["Tarif Kamar per Hari"].setText(str(tarif_kamar))
        self.calculate_total()
    
    def calculate_surcharge(self):
        self.calculate_surgery_fees()
    
    def calculate_surgery_fees(self):
        # Reset surgeon and anesthesi fees
        surgeon_fee = 0
        anesthesi_fee = 0
        
        # Calculate fees for each operation table
        for i in range(1, 5):
            op_text = self.fields[f"Tabel Operasi {i}"].currentText()
            if op_text:
                # Extract operation code
                op_code = op_text.split(" - ")[0]
                
                # Get operation details from database
                self.cursor.execute("SELECT biaya_dokter, biaya_rs FROM operation_tables WHERE kode = ?", (op_code,))
                result = self.cursor.fetchone()
                
                if result:
                    biaya_dokter, biaya_rs = result
                    
                    # Apply percentage
                    percentage_text = self.fields[f"Persentase Operasi {i}"].currentText()
                    percentage = 0.5 if percentage_text == "50%" else 1.0
                    
                    surgeon_fee += biaya_dokter * percentage
                    anesthesi_fee += biaya_rs * percentage
        
        # Apply surcharge based on operation type
        sifat_operasi = self.fields["Sifat Operasi"].currentText()
        surcharge = 1.0
        
        if sifat_operasi == "CITO":
            surcharge = 1.25
        elif sifat_operasi == "Penyulit":
            surcharge = 1.30
        
        # Apply surcharge to surgeon and anesthesi fees
        surgeon_fee *= surcharge
        anesthesi_fee *= surcharge
        
        # Update fields
        self.fields["Surgeon"].setText(str(round(surgeon_fee)))
        self.fields["Anesthesi"].setText(str(round(anesthesi_fee)))
        
        # Calculate OT Room Charge (also affected by surcharge)
        ot_room_charge = 0
        if surgeon_fee > 0 or anesthesi_fee > 0:
            # Base OT room charge is 30% of surgeon fee
            ot_room_charge = surgeon_fee * 0.3 * surcharge
        
        self.fields["OT Room Charge"].setText(str(round(ot_room_charge)))
        
        # Calculate total
        self.calculate_total()
    
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
            self.fields["Total"].setText(str(round(total)))
            
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
                self.fields["Tabel Operasi 1"].currentText(),
                self.fields["Tabel Operasi 2"].currentText(),
                self.fields["Tabel Operasi 3"].currentText(),
                self.fields["Tabel Operasi 4"].currentText(),
                float(self.fields["Persentase Operasi 1"].currentText().replace("%", "")) / 100,
                float(self.fields["Persentase Operasi 2"].currentText().replace("%", "")) / 100,
                float(self.fields["Persentase Operasi 3"].currentText().replace("%", "")) / 100,
                float(self.fields["Persentase Operasi 4"].currentText().replace("%", "")) / 100,
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
            
            self.conn.commit()
            
            QMessageBox.information(self, "Sukses", "Data berhasil disimpan!")
            self.clear_form()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")
    
    def search_data(self):
        search_by = self.search_field.currentText()
        search_value = self.search_input.text()
        
        query = "SELECT id, nama_pasien, nama_operasi, diagnosa, nama_dokter, kelas, tanggal, total FROM database"
        
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
            self.cursor.execute("SELECT * FROM database WHERE id = ?", (record_id,))
            record = self.cursor.fetchone()
            
            # Populate form with the record
            if record:
                # Switch to input tab
                self.central_widget.setCurrentIndex(0)
                
                # Map record to form fields
                fields_mapping = [
                    "Diagnosa", "Nama Operasi", "Sifat Operasi", "Nama Dokter", 
                    "Kelas", "Tabel Operasi 1", "Tabel Operasi 2", "Tabel Operasi 3", 
                    "Tabel Operasi 4", "Persentase Operasi 1", "Persentase Operasi 2", 
                    "Persentase Operasi 3", "Persentase Operasi 4", "Konsultasi Pre Tindakan", 
                    "Diagnostic Pre Tindakan", "Surgeon", "Anesthesi", "OT Room Charge", 
                    "Recovery Room Charge", "Alat", "Diagnostic", "Medical Equipment", 
                    "Obat dan Alkes", "Tarif Kamar per Hari", "Total", "Catatan", 
                    "Keterangan", "Tanggal", "Nama Pasien", "Hubungan dengan Pasien",
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
                    elif field_name.startswith("Tabel Operasi"):
                        index = self.fields[field_name].findText(record[i+1])
                        if index >= 0:
                            self.fields[field_name].setCurrentIndex(index)
                    elif field_name.startswith("Persentase Operasi"):
                        percentage = str(int(record[i+1] * 100)) + "%"
                        index = self.fields[field_name].findText(percentage)
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
                self.cursor.execute("DELETE FROM database WHERE id = ?", (record_id,))
                self.conn.commit()
                
                QMessageBox.information(self, "Sukses", "Data berhasil dihapus!")
                self.search_data()  # Refresh the table
    
    def export_to_excel(self):
        QMessageBox.information(self, "Info", "Fitur ekspor ke Excel akan segera tersedia.")
    
    def print_form(self):
        # Create a printer and print dialog
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec_() == QPrintDialog.Accepted:
            # Create a document for printing
            document = QTextDocument()
            
            # Generate HTML content for printing
            html_content = """
            <html>
            <head>
            <style>
                body { font-family: Arial, sans-serif; }
                .header { text-align: center; font-weight: bold; }
                .title { font-size: 16pt; margin-bottom: 20px; }
                .section { margin-bottom: 15px; }
                .label { font-weight: bold; }
                .table { border-collapse: collapse; width: 100%; }
                .table td, .table th { border: 1px solid #ddd; padding: 8px; }
                .table th { background-color: #f2f2f2; }
                .footer { margin-top: 30px; }
            </style>
            </head>
            <body>
            """
            
            # Add header
            html_content += """
            <div class="header">
                <p>Jl. RA Kartini No. 08 Cilandak<br>Jakarta Selatan 12430<br>Telp. (021) 29531900 Ext. 29790</p>
                <p class="title">PERKIRAAN BIAYA OPERASI</p>
            </div>
            """
            
            # Add form data
            html_content += "<div class='section'>"
            html_content += f"<p><span class='label'>Diagnosa:</span> {self.fields['Diagnosa'].text()}</p>"
            html_content += f"<p><span class='label'>Nama Operasi:</span> {self.fields['Nama Operasi'].text()}</p>"
            html_content += f"<p><span class='label'>Sifat Operasi:</span> {self.fields['Sifat Operasi'].currentText()}</p>"
            html_content += f"<p><span class='label'>Nama Dokter:</span> {self.fields['Nama Dokter'].text()}</p>"
            html_content += f"<p><span class='label'>Kelas:</span> {self.fields['Kelas'].currentText()}</p>"
            html_content += "</div>"
            
            # Add operation tables
            html_content += "<div class='section'>"
            html_content += "<p class='label'>Tabel Operasi:</p>"
            html_content += "<table class='table'><tr><th>No</th><th>Tindakan</th><th>Persentase</th></tr>"
            
            for i in range(1, 5):
                op_text = self.fields[f"Tabel Operasi {i}"].currentText()
                if op_text:
                    percentage = self.fields[f"Persentase Operasi {i}"].currentText()
                    html_content += f"<tr><td>{i}</td><td>{op_text}</td><td>{percentage}</td></tr>"
            
            html_content += "</table></div>"
            
            # Add cost details
            html_content += "<div class='section'>"
            html_content += "<p class='label'>Rincian Biaya:</p>"
            html_content += "<table class='table'><tr><th>Item</th><th>Biaya (Rp)</th></tr>"
            
            cost_items = [
                "Konsultasi Pre Tindakan", "Diagnostic Pre Tindakan", "Surgeon", 
                "Anesthesi", "OT Room Charge", "Recovery Room Charge", "Alat", 
                "Diagnostic", "Medical Equipment", "Obat dan Alkes", "Tarif Kamar per Hari"
            ]
            
            for item in cost_items:
                value = self.fields[item].text()
                if value and float(value) > 0:
                    formatted_value = format(int(float(value)), ',d').replace(',', '.')
                    html_content += f"<tr><td>{item}</td><td align='right'>{formatted_value}</td></tr>"
            
            # Add total
            total = self.fields["Total"].text()
            formatted_total = format(int(float(total)), ',d').replace(',', '.')
            html_content += f"<tr><td class='label'>TOTAL</td><td align='right' class='label'>{formatted_total}</td></tr>"
            html_content += "</table></div>"
            
            # Add notes and additional info
            html_content += "<div class='section'>"
            html_content += f"<p><span class='label'>Catatan:</span> {self.fields['Catatan'].toPlainText()}</p>"
            html_content += f"<p><span class='label'>Keterangan:</span> {self.fields['Keterangan'].toPlainText()}</p>"
            html_content += "</div>"
            
            # Add footer with signatures
            html_content += """
            <div class='footer'>
                <table width='100%'>
                    <tr>
                        <td width='50%'>
                            <p>Menyetujui dan memahami,</p>
                            <br><br><br>
                            <p>Nama dan Hubungan dengan Pasien: ________________</p>
                        </td>
                        <td width='50%'>
                            <p>Jakarta, """ + QDate.currentDate().toString("dd/MM/yyyy") + """</p>
                            <br><br><br>
                            <p>Petugas Front Office SHTB: ________________</p>
                        </td>
                    </tr>
                </table>
            </div>
            """
            
            html_content += "</body></html>"
            
            # Set HTML content and print
            document.setHtml(html_content)
            document.print_(printer)
    
    def print_selected_data(self):
        selected_row = self.results_table.currentRow()
        if selected_row >= 0:
            record_id = self.results_table.item(selected_row, 0).text()
            
            # Fetch complete record
            self.cursor.execute("SELECT * FROM database WHERE id = ?", (record_id,))
            record = self.cursor.fetchone()
            
            if record:
                # Create a printer and print dialog
                printer = QPrinter(QPrinter.HighResolution)
                dialog = QPrintDialog(printer, self)
                
                if dialog.exec_() == QPrintDialog.Accepted:
                    # Create a document for printing
                    document = QTextDocument()
                    
                    # Generate HTML content for printing
                    html_content = """
                    <html>
                    <head>
                    <style>
                        body { font-family: Arial, sans-serif; }
                        .header { text-align: center; font-weight: bold; }
                        .title { font-size: 16pt; margin-bottom: 20px; }
                        .section { margin-bottom: 15px; }
                        .label { font-weight: bold; }
                        .table { border-collapse: collapse; width: 100%; }
                        .table td, .table th { border: 1px solid #ddd; padding: 8px; }
                        .table th { background-color: #f2f2f2; }
                        .footer { margin-top: 30px; }
                    </style>
                    </head>
                    <body>
                    """
                    
                    # Add header
                    html_content += """
                    <div class="header">
                        <p>Jl. RA Kartini No. 08 Cilandak<br>Jakarta Selatan 12430<br>Telp. (021) 29531900 Ext. 29790</p>
                        <p class="title">PERKIRAAN BIAYA OPERASI</p>
                    </div>
                    """
                    
                    # Map database fields
                    fields_mapping = [
                        "Diagnosa", "Nama Operasi", "Sifat Operasi", "Nama Dokter", 
                        "Kelas", "Tabel Operasi 1", "Tabel Operasi 2", "Tabel Operasi 3", 
                        "Tabel Operasi 4", "Persentase Operasi 1", "Persentase Operasi 2", 
                        "Persentase Operasi 3", "Persentase Operasi 4", "Konsultasi Pre Tindakan", 
                        "Diagnostic Pre Tindakan", "Surgeon", "Anesthesi", "OT Room Charge", 
                        "Recovery Room Charge", "Alat", "Diagnostic", "Medical Equipment", 
                        "Obat dan Alkes", "Tarif Kamar per Hari", "Total", "Catatan", 
                        "Keterangan", "Tanggal", "Nama Pasien", "Hubungan dengan Pasien",
                        "Petugas Front Office", "Perusahaan/Asuransi Penanggung"
                    ]
                    
                    # Add form data
                    html_content += "<div class='section'>"
                    html_content += f"<p><span class='label'>Diagnosa:</span> {record[1]}</p>"
                    html_content += f"<p><span class='label'>Nama Operasi:</span> {record[2]}</p>"
                    html_content += f"<p><span class='label'>Sifat Operasi:</span> {record[3]}</p>"
                    html_content += f"<p><span class='label'>Nama Dokter:</span> {record[4]}</p>"
                    html_content += f"<p><span class='label'>Kelas:</span> {record[5]}</p>"
                    html_content += "</div>"
                    
                    # Add operation tables
                    html_content += "<div class='section'>"
                    html_content += "<p class='label'>Tabel Operasi:</p>"
                    html_content += "<table class='table'><tr><th>No</th><th>Tindakan</th><th>Persentase</th></tr>"
                    
                    for i in range(1, 5):
                        op_text = record[5 + i]  # tabel_operasi fields
                        if op_text:
                            percentage = str(int(record[9 + i] * 100)) + "%"  # persentase_operasi fields
                            html_content += f"<tr><td>{i}</td><td>{op_text}</td><td>{percentage}</td></tr>"
                    
                    html_content += "</table></div>"
                    
                    # Add cost details
                    html_content += "<div class='section'>"
                    html_content += "<p class='label'>Rincian Biaya:</p>"
                    html_content += "<table class='table'><tr><th>Item</th><th>Biaya (Rp)</th></tr>"
                    
                    cost_items = [
                        "Konsultasi Pre Tindakan", "Diagnostic Pre Tindakan", "Surgeon", 
                        "Anesthesi", "OT Room Charge", "Recovery Room Charge", "Alat", 
                        "Diagnostic", "Medical Equipment", "Obat dan Alkes", "Tarif Kamar per Hari"
                    ]
                    
                    cost_values = record[13:24]  # Cost fields in database
                    
                    for i, item in enumerate(cost_items):
                        value = cost_values[i]
                        if value and float(value) > 0:
                            formatted_value = format(int(float(value)), ',d').replace(',', '.')
                            html_content += f"<tr><td>{item}</td><td align='right'>{formatted_value}</td></tr>"
                    
                    # Add total
                    total = record[24]  # Total field
                    formatted_total = format(int(float(total)), ',d').replace(',', '.')
                    html_content += f"<tr><td class='label'>TOTAL</td><td align='right' class='label'>{formatted_total}</td></tr>"
                    html_content += "</table></div>"
                    
                    # Add notes and additional info
                    html_content += "<div class='section'>"
                    html_content += f"<p><span class='label'>Catatan:</span> {record[25]}</p>"
                    html_content += f"<p><span class='label'>Keterangan:</span> {record[26]}</p>"
                    html_content += "</div>"
                    
                    # Add footer with signatures
                    html_content += f"""
                    <div class='footer'>
                        <table width='100%'>
                            <tr>
                                <td width='50%'>
                                    <p>Menyetujui dan memahami,</p>
                                    <br><br><br>
                                    <p>Nama dan Hubungan dengan Pasien: {record[29]} ({record[30]})</p>
                                </td>
                                <td width='50%'>
                                    <p>Jakarta, {record[27]}</p>
                                    <br><br><br>
                                    <p>Petugas Front Office SHTB: {record[31]}</p>
                                    <p>Perusahaan/Asuransi: {record[32]}</p>
                                </td>
                            </tr>
                        </table>
                    </div>
                    """
                    
                    html_content += "</body></html>"
                    
                    # Set HTML content and print
                    document.setHtml(html_content)
                    document.print_(printer)
    
    def clear_form(self):
        for field_name, field_widget in self.fields.items():
            if isinstance(field_widget, QComboBox):
                if field_name == "Sifat Operasi":
                    field_widget.setCurrentIndex(0)
                elif field_name == "Kelas":
                    field_widget.setCurrentIndex(0)
                elif field_name.startswith("Tabel Operasi"):
                    field_widget.setCurrentIndex(0)
                elif field_name.startswith("Persentase Operasi"):
                    field_widget.setCurrentText("100%")
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
    