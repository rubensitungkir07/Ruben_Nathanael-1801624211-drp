# ====================================================================
# SOAL 1: Layout Catur Menggunakan For Statement
# ====================================================================
print("=== SOAL 1: LAYOUT PAPAN CATUR ===")

ukuran = 8

for baris in range(ukuran):
    baris_catur = ""
    for kolom in range(ukuran):
        if (baris + kolom) % 2 == 0:
            baris_catur += "⬛"  # Emoji Hitam
        else:
            baris_catur += "⬜"  # Emoji Putih
    print(baris_catur)

print("\n" + "="*40 + "\n")


# ====================================================================
# SOAL 2: Program Manajemen Aktivitas (Versi Improvisasi Komplit)
# ====================================================================
print("=== SOAL 2: PROGRAM MANAJEMEN AKTIVITAS ===")

list_aktivitas = []

while True:
    print("-" * 30)
    nama_aktivitas = input("Masukkan nama aktivitas: ").strip()
    waktu_aktivitas = input("Masukkan waktu pelaksanaan (misal: 08:00): ").strip()
    prioritas = input("Masukkan tingkat prioritas (Tinggi/Sedang/Rendah): ").strip()
    
    data_input = {
        "aktivitas": nama_aktivitas,
        "waktu": waktu_aktivitas,
        "prioritas": prioritas
    }
    
    list_aktivitas.append(data_input)
    
    lanjut = input("\nIngin menambah aktivitas lain? (y/n): ").lower().strip()
    if lanjut != 'y':
        break

print("\n" + "="*15 + " HASIL TERDATA " + "="*15)
print(f"{'No':<4} | {'Nama Aktivitas':<25} | {'Waktu':<10} | {'Prioritas':<10}")
print("-" * 60)

for indeks, item in enumerate(list_aktivitas, start=1):
    print(f"{indeks:<4} | {item['aktivitas']:<25} | {item['waktu']:<10} | {item['prioritas']:<10}")

print("=" * 45)
print("Sistem Berhasil Menyimpan Semua Data.")