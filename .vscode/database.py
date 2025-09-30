import sqlite3
import os

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

if __name__ == "__main__":
    # Initialize the database
    init_operation_tables()
    
    # Add some sample operations if the table is empty
    conn = sqlite3.connect('data/pbo_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM operation_tables")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        sample_operations = [
            ('4199999994','DOCTORS PROCEDURE TABLE 3','ODC',4934000,0),
            ('4199999995','DOCTORS PROCEDURE TABLE 1','ODC',1125000,0),
            ('4199999996','DOCTORS PROCEDURE TABLE 2','ODC',2368000,0),
        ]
        
        for op in sample_operations:
            add_operation(*op)
        
        print("Sample operations added to the database.")