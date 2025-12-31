"""
Test mapping kelas ke harga kamar
"""
mapping = {
    'ED': 350000,      # Basic
    'OD': 750000,      # Standard
    'ICCU': 950000,    # Deluxe
    'PICU': 1900000,   # VIP
    'HDU': 2000000,    # VVIP
    'ICU': 5000000,    # Suite
    'OR': 7500000      # Presidential Suite
}

print("="*60)
print("MAPPING KELAS KE HARGA KAMAR")
print("="*60)

for kelas, harga in mapping.items():
    print(f"{kelas:10} → Rp {harga:>12,} ({harga//100000 * 100}k)")

print("\n" + "="*60)
print("VERIFIKASI")
print("="*60)

harga_kamar_original = [350000, 750000, 950000, 1900000, 2000000, 5000000, 7500000]
harga_kamar_mapping = list(mapping.values())

print(f"\nTotal original: {len(harga_kamar_original)} harga")
print(f"Total mapping: {len(harga_kamar_mapping)} harga")

if harga_kamar_original == harga_kamar_mapping:
    print("✅ MATCH - Semua harga sesuai!")
else:
    print("❌ MISMATCH")
    print(f"Original: {harga_kamar_original}")
    print(f"Mapping: {harga_kamar_mapping}")

print("\n" + "="*60)
