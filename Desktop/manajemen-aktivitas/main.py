from datetime import datetime

def main():
    print("=== APLIKASI MANAJEMEN AKTIVITAS ===")
    print("Pilih kegiatan yang akan dilakukan:")
    print("1. Sarapan")
    print("2. Berangkat Kerja")
    print("3. Lainnya")
    
    # Input kegiatan utama
    kegiatan = input("\nMasukkan pilihan kegiatan Anda (sarapan/berangkat kerja/lainnya): ").strip().lower()
    print("-" * 40)

    # 1. KONDISI JIKA USER HENDAK SARAPAN
    if kegiatan == "sarapan":
        print("Menu yang tersedia di rumah: telur, ikan, nugget.")
        menu = input("Masukkan menu sarapan yang Anda inginkan: ").strip().lower()
        
        # Mengecek ketersediaan bahan
        bahan_tersedia = ["telur", "ikan", "nugget"]
        
        if menu in bahan_tersedia:
            print(f"\n[SISTEM]: Bahan untuk membuat '{menu}' tersedia di lokasi.")
            print(f"[SISTEM]: Silahkan masak terlebih dahulu sebelum menyantapnya!")
        else:
            print(f"\n[SISTEM]: Bahan untuk membuat '{menu}' tidak tersedia di rumah.")
            print(f"[SISTEM]: Anda harus pergi membeli bahannya terlebih dahulu ke toko/pasar.")

    # 2. KONDISI JIKA USER HENDAK BERANGKAT KERJA
    elif kegiatan == "berangkat kerja" or kegiatan == "kerja":
        # Mengambil waktu saat ini dari komputer
        waktu_sekarang = datetime.now()
        jam_sekarang = waktu_sekarang.hour
        menit_sekarang = waktu_sekarang.minute
        
        print(f"[SISTEM]: Waktu komputer saat ini menunjukkan pukul {jam_sekarang:02d}:{menit_sekarang:02d}")
        print("[SISTEM]: Jadwal masuk kerja diasumsikan pukul 08:00")
        print("-" * 40)
        
        # Logika pengecekan keterlambatan (Batas jam 08:00)
        if jam_sekarang < 8:
            print("NOTIFIKASI: Aman! Anda belum terlambat. Masih ada waktu untuk bersiap.")
        elif jam_sekarang == 8 and menit_sekarang == 0:
            print("NOTIFIKASI: Peringatan! Tepat pukul 08:00. Segera lakukan presensi/absensi!")
        else:
            print("NOTIFIKASI: Perhatian! Anda sudah TERLAMBAT masuk kerja.")

    # 3. IMPROVISASI: KONDISI JIKA KEGIATAN LAINNYA / TIDAK DIKENALI
    elif kegiatan == "lainnya":
        aktivitas_lain = input("Aktivitas apa yang ingin Anda lakukan? ")
        print(f"\n[SISTEM]: Aktivitas '{aktivitas_lain}' berhasil dicatat ke dalam agenda hari ini.")
    else:
        print("\n[SISTEM]: Pilihan kegiatan tidak valid. Silakan jalankan ulang program.")

    print("-" * 40)
    print("=== PROGRAM SELESAI ===")

if __name__ == "__main__":
    main()