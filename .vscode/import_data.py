import sqlite3
import os
import csv

def init_operation_tables():
    """Initialize the operation tables database"""
    if not os.path.exists('data'):
        os.makedirs('data')
        
    conn = sqlite3.connect('data/pbo_database.db')
    cursor = conn.cursor()
    
    # Create operation tables if not exists
    cursor.execute('''
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
    
    conn.commit()
    conn.close()

def add_operation(kode, nama_tindakan, kelas, biaya_dokter, biaya_rs):
    """Add a new operation to the database"""
    conn = sqlite3.connect('data/pbo_database.db')
    cursor = conn.cursor()
    
    total_biaya = biaya_dokter + biaya_rs
    
    cursor.execute('''
        INSERT INTO operation_tables (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya))
    
    conn.commit()
    conn.close()

def import_from_csv(filename):
    """Import data from CSV file to database"""
    try:
        if not os.path.exists(filename):
            print(f"Warning: File {filename} not found. Skipping CSV import.")
            return False
            
        with open(filename, 'r', encoding='utf-8') as file:
            # Skip the first line [file name]
            next(file)
            # Skip the second line [file content begin]
            next(file)
            
            reader = csv.reader(file)
            imported_count = 0
            for row in reader:
                if row:  # Skip empty lines
                    try:
                        # Remove parentheses and split by comma
                        clean_row = row[0].strip().strip('()').split(',')
                        
                        # Extract values (first 5 elements)
                        kode = clean_row[0].strip().strip("'")
                        nama_tindakan = clean_row[1].strip().strip("'")
                        kelas = clean_row[2].strip().strip("'")
                        
                        # Handle potential formatting issues with numbers
                        biaya_dokter = float(clean_row[3].strip())
                        biaya_rs = float(clean_row[4].strip())
                        
                        add_operation(kode, nama_tindakan, kelas, biaya_dokter, biaya_rs)
                        imported_count += 1
                    except Exception as row_error:
                        print(f"Warning: Skipping row due to error: {str(row_error)}")
                        continue
        
        print(f"Successfully imported {imported_count} operations from {filename}.")
        return True
        
    except FileNotFoundError:
        print(f"Warning: File {filename} not found. Skipping CSV import.")
        return False
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return False

def get_all_operations():
    """Get all operations from the database"""
    conn = sqlite3.connect('data/pbo_database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM operation_tables ORDER BY kode")
    operations = cursor.fetchall()
    
    conn.close()
    return operations

def update_operation(operation_id, kode, nama_tindakan, kelas, biaya_dokter, biaya_rs):
    """Update an existing operation"""
    conn = sqlite3.connect('data/pbo_database.db')
    cursor = conn.cursor()
    
    total_biaya = biaya_dokter + biaya_rs
    
    cursor.execute('''
        UPDATE operation_tables 
        SET kode=?, nama_tindakan=?, kelas=?, biaya_dokter=?, biaya_rs=?, total_biaya=?
        WHERE id=?
    ''', (kode, nama_tindakan, kelas, biaya_dokter, biaya_rs, total_biaya, operation_id))
    
    conn.commit()
    conn.close()

def delete_operation(operation_id):
    """Delete an operation from the database"""
    conn = sqlite3.connect('data/pbo_database.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM operation_tables WHERE id=?", (operation_id,))
    
    conn.commit()
    conn.close()

def count_operations():
    """Count number of operations in database"""
    conn = sqlite3.connect('data/pbo_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM operation_tables")
    count = cursor.fetchone()[0]
    conn.close()
    return count

if __name__ == "__main__":
    # Initialize the database
    init_operation_tables()
    
    # Check if database is empty
    if count_operations() == 0:
        # Import data from CSV file
        csv_filename = 'db test1.csv'  # Change this to your actual file name
        import_from_csv(csv_filename)
        
        # Add sample operations as well (optional)
        sample_operations = [
            ('4199999994', 'DOCTORS PROCEDURE TABLE 3', 'ODC', 4934000, 0),
            ('4199999995', 'DOCTORS PROCEDURE TABLE 1', 'ODC', 1125000, 0),
            ('4199999996', 'DOCTORS PROCEDURE TABLE 2', 'ODC', 2368000, 0),
        ]
        
        for op in sample_operations:
            add_operation(*op)
        
        print("Sample operations added to the database.")
        print(f"Total operations in database: {count_operations()}")
    else:
        print(f"Database already contains {count_operations()} operations.")