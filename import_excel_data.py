"""
Script to import data from Excel file (db pbo.xlsx) into the database
This script imports:
1. Operation data from "db table operasi" sheet
2. Doctor names from "db nama dokter" sheet
"""

import openpyxl
import os
from models import Database

def import_operations_from_excel(excel_path, db):
    """Import operation data from Excel sheet 'db table operasi'"""
    try:
        # Load the workbook
        wb = openpyxl.load_workbook(excel_path)
        
        # Get the operations sheet
        if 'db table operasi' not in wb.sheetnames:
            print("Error: Sheet 'db table operasi' not found in Excel file")
            return False
        
        ws = wb['db table operasi']
        
        # Clear existing operations (optional - comment out if you want to keep existing data)
        print("Clearing existing operations...")
        db.delete_all_operations()
        
        imported_count = 0
        skipped_count = 0
        
        # Start from row 2 (skip header row)
        # Expected columns: Fee Operator (B), Kelas (C), Harga Operator (D), Harga Anestesi (E)
        for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            try:
                # Skip empty rows
                if not any(row):
                    continue
                
                # Extract data from columns
                # Column A is empty/None, so we start from index 1
                fee_operator = row[1] if len(row) > 1 else None
                kelas = row[2] if len(row) > 2 else None
                harga_operator = row[3] if len(row) > 3 else None
                harga_anestesi = row[4] if len(row) > 4 else None
                
                # Skip if essential data is missing
                if not fee_operator or not kelas:
                    skipped_count += 1
                    continue
                
                # Clean and validate data
                fee_operator = str(fee_operator).strip()
                kelas = str(kelas).strip()
                
                # Convert prices to float, default to 0 if invalid
                try:
                    harga_operator = float(harga_operator) if harga_operator else 0
                except (ValueError, TypeError):
                    harga_operator = 0
                
                try:
                    harga_anestesi = float(harga_anestesi) if harga_anestesi else 0
                except (ValueError, TypeError):
                    harga_anestesi = 0
                
                # Generate a code for the operation (using row number as unique identifier)
                kode = f"OP{row_num:06d}"
                
                # Add to database
                db.add_operation(
                    kode=kode,
                    nama_tindakan=fee_operator,
                    kelas=kelas,
                    biaya_dokter=harga_operator,
                    biaya_rs=harga_anestesi
                )
                
                imported_count += 1
                
            except Exception as e:
                print(f"Warning: Error processing row {row_num}: {str(e)}")
                skipped_count += 1
                continue
        
        print(f"\nOperation Import Summary:")
        print(f"  - Successfully imported: {imported_count} operations")
        print(f"  - Skipped: {skipped_count} rows")
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Excel file not found at {excel_path}")
        return False
    except Exception as e:
        print(f"Error importing operations: {str(e)}")
        return False

def import_doctors_from_excel(excel_path, db):
    """Import doctor names from Excel sheet 'db nama dokter'"""
    try:
        # Load the workbook
        wb = openpyxl.load_workbook(excel_path)
        
        # Get the doctors sheet
        if 'db nama dokter' not in wb.sheetnames:
            print("Error: Sheet 'db nama dokter' not found in Excel file")
            return False
        
        ws = wb['db nama dokter']
        
        # Clear existing doctors (optional - comment out if you want to keep existing data)
        print("Clearing existing doctors...")
        db.delete_all_doctors()
        
        imported_count = 0
        skipped_count = 0
        duplicate_count = 0
        
        # Start from row 2 (skip header row)
        # Doctor names are in column B (index 1)
        for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            try:
                # Skip empty rows
                if not any(row):
                    continue
                
                # Extract doctor name from column B (index 1)
                nama_dokter = row[1] if len(row) > 1 else None
                
                # Skip if name is missing
                if not nama_dokter:
                    skipped_count += 1
                    continue
                
                # Clean the name
                nama_dokter = str(nama_dokter).strip()
                
                # Skip empty names
                if not nama_dokter:
                    skipped_count += 1
                    continue
                
                # Add to database
                result = db.add_doctor(nama_dokter)
                
                if result:
                    imported_count += 1
                else:
                    # Doctor already exists (duplicate)
                    duplicate_count += 1
                
            except Exception as e:
                print(f"Warning: Error processing row {row_num}: {str(e)}")
                skipped_count += 1
                continue
        
        print(f"\nDoctor Import Summary:")
        print(f"  - Successfully imported: {imported_count} doctors")
        print(f"  - Duplicates skipped: {duplicate_count} doctors")
        print(f"  - Other skipped: {skipped_count} rows")
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Excel file not found at {excel_path}")
        return False
    except Exception as e:
        print(f"Error importing doctors: {str(e)}")
        return False

def import_tindakan_from_excel(excel_path, db):
    """Import tindakan items from Excel sheet 'db nama tindakan'"""
    try:
        # Load the workbook
        wb = openpyxl.load_workbook(excel_path)
        
        # Get the tindakan sheet
        if 'db nama tindakan' not in wb.sheetnames:
            print("Warning: Sheet 'db nama tindakan' not found in Excel file")
            return False
        
        ws = wb['db nama tindakan']
        
        # Clear existing tindakan items (optional - comment out if you want to keep existing data)
        print("Clearing existing tindakan items...")
        db.delete_all_tindakan_items()
        
        imported_count = 0
        skipped_count = 0
        
        # Start from row 2 (skip header row)
        # Expected columns: nama tindakan (B), kelas (C), kategory (D), Sales Item Type (E), AMOUNT (F)
        for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            try:
                # Skip empty rows
                if not any(row):
                    continue
                
                # Extract data from columns (assuming column A is empty/index, so we start from index 1)
                nama_tindakan = row[1] if len(row) > 1 else None
                kelas = row[2] if len(row) > 2 else None
                kategory = row[3] if len(row) > 3 else None
                sales_item_type = row[4] if len(row) > 4 else None
                amount = row[5] if len(row) > 5 else None
                
                # Skip if essential data is missing
                if not nama_tindakan:
                    skipped_count += 1
                    continue
                
                # Clean and validate data
                nama_tindakan = str(nama_tindakan).strip()
                kelas = str(kelas).strip() if kelas else ''
                kategory = str(kategory).strip() if kategory else ''
                sales_item_type = str(sales_item_type).strip() if sales_item_type else ''
                
                # Convert amount to float, default to 0 if invalid
                try:
                    amount = float(amount) if amount else 0
                except (ValueError, TypeError):
                    amount = 0
                
                # Add to database
                db.add_tindakan_item(
                    nama_tindakan=nama_tindakan,
                    kelas=kelas,
                    kategory=kategory,
                    sales_item_type=sales_item_type,
                    amount=amount
                )
                
                imported_count += 1
                
            except Exception as e:
                print(f"Warning: Error processing row {row_num}: {str(e)}")
                skipped_count += 1
                continue
        
        print(f"\nTindakan Items Import Summary:")
        print(f"  - Successfully imported: {imported_count} items")
        print(f"  - Skipped: {skipped_count} rows")
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Excel file not found at {excel_path}")
        return False
    except Exception as e:
        print(f"Error importing tindakan items: {str(e)}")
        return False

def main():
    """Main function to run the import"""
    print("=" * 60)
    print("Excel Data Import Script")
    print("=" * 60)
    
    # Excel file path
    excel_path = 'data/db pbo.xlsx'
    
    # Check if file exists
    if not os.path.exists(excel_path):
        print(f"\nError: Excel file not found at '{excel_path}'")
        print("Please make sure the file exists in the correct location.")
        return
    
    print(f"\nExcel file found: {excel_path}")
    
    # Initialize database
    print("\nInitializing database...")
    db = Database()
    
    # Import operations
    print("\n" + "=" * 60)
    print("Importing Operations from 'db table operasi' sheet...")
    print("=" * 60)
    operations_success = import_operations_from_excel(excel_path, db)
    
    # Import doctors
    print("\n" + "=" * 60)
    print("Importing Doctors from 'db nama dokter' sheet...")
    print("=" * 60)
    doctors_success = import_doctors_from_excel(excel_path, db)
    
    # Import tindakan items
    print("\n" + "=" * 60)
    print("Importing Tindakan Items from 'db nama tindakan' sheet...")
    print("=" * 60)
    tindakan_success = import_tindakan_from_excel(excel_path, db)
    
    # Final summary
    print("\n" + "=" * 60)
    print("Import Complete!")
    print("=" * 60)
    
    if operations_success and doctors_success and tindakan_success:
        print("\n✓ All data imported successfully!")
        print(f"\nDatabase Statistics:")
        print(f"  - Total operations: {len(db.get_all_operations())}")
        print(f"  - Total doctors: {db.count_doctors()}")
        print(f"  - Total tindakan items: {db.count_tindakan_items()}")
    else:
        print("\n⚠ Some imports failed. Please check the error messages above.")
    
    print("\nYou can now use the application with the imported data.")
    print("=" * 60)

if __name__ == "__main__":
    main()
