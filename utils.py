from config import Config

class PBOCalculator:
    """Business logic for PBO calculations"""
    
    @staticmethod
    def get_room_rate(kelas):
        """Get room rate based on class"""
        return Config.ROOM_RATES.get(kelas, 0)
    
    @staticmethod
    def get_surcharge_rate(sifat_operasi):
        """Get surcharge rate based on operation type"""
        return Config.SURCHARGE_RATES.get(sifat_operasi, 1.0)
    
    @staticmethod
    def calculate_surgery_fees(operations_data, sifat_operasi, db):
        """
        Calculate surgeon and anesthesi fees
        
        Args:
            operations_data: List of dicts with keys: kode, persentase
            sifat_operasi: Type of operation (Elektif, CITO, Penyulit)
            db: Database instance
        
        Returns:
            dict with surgeon, anesthesi, ot_room_charge
        """
        surgeon_fee = 0
        anesthesi_fee = 0
        
        # Calculate base fees from operation tables
        for op_data in operations_data:
            kode = op_data.get('kode', '').strip()
            
            # Skip if operation code is empty
            if not kode:
                continue
                
            # Extract operation code (remove description if present)
            kode = kode.split(' - ')[0].strip()
            
            # Get operation details from database
            operation = db.get_operation_by_code(kode)
            
            if operation:
                biaya_dokter = operation['biaya_dokter']
                biaya_rs = operation['biaya_rs']
                
                # Get percentage - handle both decimal (0.5, 1.0) and integer (50, 100) formats
                persentase = op_data.get('persentase', 100)
                try:
                    persentase = float(persentase)
                    # If percentage is > 1, assume it's in integer format (50, 100), convert to decimal
                    if persentase > 1:
                        persentase = persentase / 100
                except (ValueError, TypeError):
                    persentase = 1.0  # Default to 100%
                
                surgeon_fee += biaya_dokter * persentase
                anesthesi_fee += biaya_rs * persentase
        
        # Apply surcharge based on operation type
        surcharge = PBOCalculator.get_surcharge_rate(sifat_operasi)
        surgeon_fee *= surcharge
        anesthesi_fee *= surcharge
        
        # Calculate OT Room Charge (30% of surgeon fee with surcharge)
        ot_room_charge = surgeon_fee * Config.OT_ROOM_CHARGE_PERCENTAGE
        
        return {
            'surgeon': round(surgeon_fee),
            'anesthesi': round(anesthesi_fee),
            'ot_room_charge': round(ot_room_charge)
        }
    
    @staticmethod
    def calculate_total(cost_items):
        """
        Calculate total cost from all items
        
        Args:
            cost_items: dict with all cost components
        
        Returns:
            total cost (rounded)
        """
        total = 0
        
        # List of all cost fields
        cost_fields = [
            'konsultasi_pre_tindakan',
            'diagnostic_pre_tindakan',
            'surgeon',
            'anesthesi',
            'ot_room_charge',
            'recovery_room_charge',
            'alat',
            'diagnostic',
            'medical_equipment',
            'obat_dan_alkes',
            'tarif_kamar'
        ]
        
        for field in cost_fields:
            value = cost_items.get(field, 0)
            try:
                total += float(value) if value else 0
            except (ValueError, TypeError):
                continue
        
        return round(total)
    
    @staticmethod
    def format_currency(amount):
        """Format number as Indonesian Rupiah"""
        try:
            amount = int(float(amount))
            return f"Rp {amount:,}".replace(',', '.')
        except (ValueError, TypeError):
            return "Rp 0"
    
    @staticmethod
    def parse_currency(currency_string):
        """Parse Indonesian Rupiah string to number"""
        try:
            # Remove 'Rp', spaces, and dots
            cleaned = currency_string.replace('Rp', '').replace(' ', '').replace('.', '')
            return float(cleaned)
        except (ValueError, AttributeError):
            return 0


class FormValidator:
    """Validate form inputs"""
    
    @staticmethod
    def validate_pbo_form(form_data):
        """
        Validate PBO form data
        
        Returns:
            tuple: (is_valid, error_messages)
        """
        errors = []
        
        # Required fields
        required_fields = {
            'nama_pasien': 'Nama Pasien',
            'diagnosa': 'Diagnosa',
            'nama_operasi': 'Nama Operasi',
            'nama_dokter': 'Nama Dokter',
            'kelas': 'Kelas',
            'tanggal': 'Tanggal'
        }
        
        for field, label in required_fields.items():
            if not form_data.get(field):
                errors.append(f"{label} harus diisi")
        
        # Validate numeric fields
        numeric_fields = [
            'konsultasi_pre_tindakan', 'diagnostic_pre_tindakan',
            'recovery_room_charge', 'alat', 'diagnostic',
            'medical_equipment', 'obat_dan_alkes'
        ]
        
        for field in numeric_fields:
            value = form_data.get(field, 0)
            try:
                float(value)
            except (ValueError, TypeError):
                errors.append(f"{field.replace('_', ' ').title()} harus berupa angka")
        
        # Validate percentages - only for operations that are filled
        for i in range(1, 5):
            tabel_operasi = form_data.get(f'tabel_operasi{i}', '').strip()
            
            # Only validate percentage if operation table is filled
            if tabel_operasi:
                persentase = form_data.get(f'persentase_operasi{i}', 1.0)
                try:
                    p = float(persentase)
                    # Accept both decimal (0.5, 1.0) and integer (50, 100) formats
                    if p > 1:  # Integer format
                        if p not in [50, 100]:
                            errors.append(f"Persentase Operasi {i} harus 50% atau 100%")
                    else:  # Decimal format
                        if p not in [0.5, 1.0]:
                            errors.append(f"Persentase Operasi {i} harus 50% atau 100%")
                except (ValueError, TypeError):
                    errors.append(f"Persentase Operasi {i} tidak valid")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def sanitize_input(text):
        """Sanitize text input to prevent XSS"""
        if not text:
            return ""
        
        # Basic sanitization - remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&']
        sanitized = str(text)
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized.strip()


class ReportGenerator:
    """Generate reports and exports"""
    
    @staticmethod
    def generate_pbo_summary(pbo_data):
        """Generate summary data for PBO report"""
        summary = {
            'patient_info': {
                'nama': pbo_data.get('nama_pasien', ''),
                'diagnosa': pbo_data.get('diagnosa', ''),
                'kelas': pbo_data.get('kelas', ''),
                'tanggal': pbo_data.get('tanggal', '')
            },
            'operation_info': {
                'nama_operasi': pbo_data.get('nama_operasi', ''),
                'sifat_operasi': pbo_data.get('sifat_operasi', ''),
                'nama_dokter': pbo_data.get('nama_dokter', '')
            },
            'operation_tables': [],
            'costs': {},
            'total': pbo_data.get('total', 0)
        }
        
        # Add operation tables
        for i in range(1, 5):
            tabel = pbo_data.get(f'tabel_operasi{i}')
            if tabel:
                persentase = pbo_data.get(f'persentase_operasi{i}', 1.0)
                summary['operation_tables'].append({
                    'no': i,
                    'tindakan': tabel,
                    'persentase': f"{int(persentase * 100)}%"
                })
        
        # Add costs
        cost_fields = {
            'konsultasi_pre_tindakan': 'Konsultasi Pre Tindakan',
            'diagnostic_pre_tindakan': 'Diagnostic Pre Tindakan',
            'surgeon': 'Surgeon',
            'anesthesi': 'Anesthesi',
            'ot_room_charge': 'OT Room Charge',
            'recovery_room_charge': 'Recovery Room Charge',
            'alat': 'Alat',
            'diagnostic': 'Diagnostic',
            'medical_equipment': 'Medical Equipment',
            'obat_dan_alkes': 'Obat dan Alkes',
            'tarif_kamar': 'Tarif Kamar per Hari'
        }
        
        for field, label in cost_fields.items():
            value = pbo_data.get(field, 0)
            if value and float(value) > 0:
                summary['costs'][label] = float(value)
        
        return summary
