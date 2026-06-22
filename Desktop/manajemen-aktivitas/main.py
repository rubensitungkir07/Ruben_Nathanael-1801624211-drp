import sqlite3
from datetime import datetime

# ====================================================================
# DATABASE SETUP (Inisialisasi SQLite)
# ====================================================================
def inisialisasi_db():
    conn = sqlite3.connect('manajemen_aktivitas.db')
    cursor = conn.cursor()
    # MEMPERBAIKI SYNTAX: Mengubah TEXT NOT EXISTS menjadi TEXT NOT NULL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aktivitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_aktivitas TEXT NOT NULL,
            kategori TEXT,
            prioritas TEXT,
            waktu_input TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ====================================================================
# FUNGSI CRUD (Create, Read, Update, Delete)
# ====================================================================

# 1. CREATE: Menambah Aktivitas Baru
def tambah_aktivitas():
    print("\n--- TAMBAH AKTIVITAS BARU (CREATE) ---")
    nama = input("Masukkan nama aktivitas: ").strip()
    kategori = input("Masukkan kategori (sarapan/kerja/lainnya): ").strip().lower()
    prioritas = input("Masukkan prioritas (Tinggi/Sedang/Rendah): ").strip()
    
    # Logic otomatis sesuai catatan PDF: Generate waktu sekarang tanpa input user
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect('manajemen_aktivitas.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO aktivitas (nama_aktivitas, kategori, prioritas, waktu_input)
        VALUES (?, ?, ?, ?)
    ''', (nama, kategori, prioritas, waktu_sekarang))
    conn.commit()
    conn.close()
    print("[SUKSES] Aktivitas berhasil disimpan ke database SQLite!")

# 2. READ: Menampilkan Semua Aktivitas
def tampilkan_aktivitas():
    print("\n--- DAFTAR AKTIVITAS TERDATA (READ) ---")
    conn = sqlite3.connect('manajemen_aktivitas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM aktivitas')
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("Belum ada aktivitas yang terdaftar.")
        return False
        
    print(f"{'ID':<4} | {'Nama Aktivitas':<25} | {'Kategori':<12} | {'Prioritas':<10} | {'Waktu Input':<20}")
    print("-" * 80)
    for row in rows:
        print(f"{row[0]:<4} | {row[1]:<25} | {row[2]:<12} | {row[3]:<10} | {row[4]:<20}")
    return True

# 3. UPDATE: Mengubah Data Aktivitas
def ubah_aktivitas():
    print("\n--- UBAH DATA AKTIVITAS (UPDATE) ---")
    if not tampilkan_aktivitas():
        return
        
    id_target = input("\nMasukkan ID Aktivitas yang ingin diubah: ").strip()
    nama_baru = input("Masukkan nama aktivitas baru: ").strip()
    kategori_baru = input("Masukkan kategori baru: ").strip().lower()
    prioritas_baru = input("Masukkan prioritas baru: ").strip()
    waktu_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Otomatis update waktu
    
    conn = sqlite3.connect('manajemen_aktivitas.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE aktivitas 
        SET nama_aktivitas = ?, kategori = ?, prioritas = ?, waktu_input = ?
        WHERE id = ?
    ''', (nama_baru, kategori_baru, prioritas_baru, waktu_update, id_target))
    conn.commit()
    conn.close()
    print(f"[SUKSES] Data ID {id_target} berhasil diperbarui!")

# 4. DELETE: Menghapus Aktivitas
def hapus_aktivitas():
    print("\n--- HAPUS AKTIVITAS (DELETE) ---")
    if not tampilkan_aktivitas():
        return
        
    id_target = input("\nMasukkan ID Aktivitas yang ingin dihapus: ").strip()
    
    conn = sqlite3.connect('manajemen_aktivitas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM aktivitas WHERE id = ?', (id_target,))
    conn.commit()
    conn.close()
    print(f"[SUKSES] Aktivitas dengan ID {id_target} telah dihapus dari database.")

# ====================================================================
# PROGRAM UTAMA / MENU INTERFASE
# ====================================================================
def main():
    inisialisasi_db()
    while True:
        print("\n" + "="*20 + " APLIKASI CRUD SQLITE AKTIVITAS " + "="*20)
        print("1. Tambah Aktivitas (Create)")
        print("2. Lihat Semua Aktivitas (Read)")
        print("3. Edit Data Aktivitas (Update)")
        print("4. Hapus Aktivitas (Delete)")
        print("5. Keluar")
        
        pilihan = input("Pilih menu (1-5): ").strip()
        
        if pilihan == '1':
            tambah_aktivitas()
        elif pilihan == '2':
            tampilkan_aktivitas()
        elif pilihan == '3':
            ubah_aktivitas()
        elif pilihan == '4':
            hapus_aktivitas()
        elif pilihan == '5':
            print("Terima kasih! Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()