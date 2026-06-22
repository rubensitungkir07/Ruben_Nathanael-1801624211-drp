import os

class QuizAppMenu:
    def __init__(self, quiz_service):
        self.quiz_service = quiz_service

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show(self):
        while True:
            self.clear_screen()
            print("=============================================")
            print("  🧠 PSYCHO-GROUND: ADVANCED QUIZ SYSTEM 🧠  ")
            print("=============================================")
            print("1. Mulai Kuis Ujian (Create & Read)")
            print("2. Lihat Riwayat Nilai / Leaderboard (Read)")
            print("3. Lihat Daftar Peserta Terdaftar (Read)")
            print("4. [Admin] Update Jawaban Soal (Update)")
            print("5. [Admin] Reset Semua Hasil Nilai (Delete)")
            print("6. [Tugas 12] Export Riwayat Nilai ke JSON")
            print("7. [Tugas 12] Import Riwayat Nilai dari JSON")
            print("8. [Tugas 13] Tampilkan Analisis Data (Insights)")
            print("9. Keluar")
            print("=============================================")
            
            pilihan = input("Pilih menu (1-9): ")

            if pilihan == '1':
                self.menu_mulai_kuis()
            elif pilihan == '2':
                self.menu_lihat_hasil()
            elif pilihan == '3':
                self.menu_daftar_user()
            elif pilihan == '4':
                self.menu_update_soal()
            elif pilihan == '5':
                self.menu_reset_nilai()
            elif pilihan == '6':
                self.menu_export_json()
            elif pilihan == '7':
                self.menu_import_json()
            elif pilihan == '8':
                self.menu_insights_data()
            elif pilihan == '9':
                print("\nSampai jumpa!")
                break

    def menu_mulai_kuis(self):
        self.clear_screen()
        print("=== 📝 REGISTRASI PESERTA (CREATE) ===")
        nama = input("Masukkan nama: ")
        umur = input("Masukkan umur: ")
        self.quiz_service.register_new_user(nama, umur)
        
        print(f"\nHalo {nama}, ujian dimulai!")
        input("Tekan Enter untuk memunculkan soal..."); self.clear_screen()

        questions = self.quiz_service.get_questions()
        user_answers = []

        for q in questions:
            print(f"\n[Soal] {q['pertanyaan']}")
            print(f"  A. {q['opsi_A']}\n  B. {q['opsi_B']}\n  C. {q['opsi_C']}\n  D. {q['opsi_D']}")
            
            while True:
                jawaban = input("Jawaban kamu (A/B/C/D): ").upper()
                if jawaban in ['A', 'B', 'C', 'D']: break
                print("Ketik A, B, C, atau D!")
                
            user_answers.append(jawaban)
            self.clear_screen()

        skor_total, status_kelulusan = self.quiz_service.calculate_score(user_answers)
        self.quiz_service.save_quiz_result(nama, skor_total, status_kelulusan)

        print("🎉 UJIAN SELESAI! 🎉")
        print(f"Nama             : {nama}")
        print(f"Total Nilai      : {skor_total} / 100")
        print(f"Status           : {status_kelulusan.upper()}")
        input("\nTekan Enter untuk kembali...")

    def menu_lihat_hasil(self):
        self.clear_screen()
        print("=== 📊 RIWAYAT HASIL UJIAN (READ) ===")
        results = self.quiz_service.get_leaderboard()
        if not results:
            print("[Kosong] Belum ada data nilai di database.")
        for idx, r in enumerate(results, 1):
            print(f"{idx}. {r['nama_peserta']} -> Nilai: {r['skor_total']} ({r['status']}) - [{r['waktu_ujian']}]")
        input("\nTekan Enter...")

    def menu_daftar_user(self):
        self.clear_screen()
        print("=== 👥 DAFTAR USER TERDAFTAR (READ) ===")
        users = self.quiz_service.get_users()
        for idx, u in enumerate(users, 1):
            print(f"{idx}. {u['nama']} ({u['umur']} tahun)")
        input("\nTekan Enter...")

    def menu_update_soal(self):
        self.clear_screen()
        print("=== 🔧 UPDATE KUNCI JAWABAN (UPDATE) ===")
        id_soal = input("Masukkan ID Soal yang ingin diubah kuncinya: ")
        kunci_baru = input("Masukkan Kunci Jawaban Baru (A/B/C/D): ").upper()
        self.quiz_service.update_soal(int(id_soal), kunci_baru)
        print("\nKunci jawaban sukses diperbarui!")
        input("\nTekan Enter...")

    def menu_reset_nilai(self):
        self.clear_screen()
        print("=== ⚠️ RESET LEADERBOARD (DELETE) ===")
        yakin = input("Apakah kamu yakin ingin menghapus semua skor? (Y/N): ").upper()
        if yakin == 'Y':
            self.quiz_service.reset_leaderboard()
            print("\nSeluruh data riwayat nilai berhasil dihapus!")
        input("\nTekan Enter...")

    def menu_export_json(self):
        self.clear_screen()
        print("=== 📤 EXPORT DATA KE FILE JSON ===")
        nama_file = input("Masukkan nama file output (contoh: nilai_backup.json): ")
        try:
            self.quiz_service.export_data(nama_file)
            print(f"\nSukses! Data dari SQLite berhasil dicetak menjadi file '{nama_file}'.")
        except Exception as e:
            print(f"\nGagal melakukan export: {e}")
        input("\nTekan Enter...")

    def menu_import_json(self):
        self.clear_screen()
        print("=== 📥 IMPORT DATA DARI FILE JSON ===")
        nama_file = input("Masukkan nama file JSON yang mau di-import: ")
        try:
            self.quiz_service.import_data(nama_file)
            print(f"\nSukses! Data dari file '{nama_file}' berhasil disuntikkan ke SQLite.")
        except Exception as e:
            print(f"\nGagal melakukan import: {e}")
        input("\nTekan Enter...")

    # OUTPUT UTAMA UNTUK TUGAS 13
    def menu_insights_data(self):
        self.clear_screen()
        print("=== 📈 LAPORAN PENGOLAHAN DATA STATISTIK (INSIGHTS) ===")
        stats = self.quiz_service.get_insights()
        
        if stats is None:
            print("[Peringatan] Belum ada data nilai terkumpul untuk diolah.")
            print("Silakan jalankan Menu 1 atau lakukan Import data JSON terlebih dahulu!")
        else:
            print(f"1. Total Responden/Peserta Ujian  : {stats['total_peserta']} Orang")
            print(f"2. Rata-Rata Nilai Kuis Psikologi  : {stats['rata_rata_skor']} / 100")
            print(f"3. Jumlah Peserta Lulus (>= 70)    : {stats['total_lulus']} Orang")
            print(f"4. Jumlah Peserta Tidak Lulus      : {stats['total_tidak_lulus']} Orang")
            print(f"5. Persentase Kelulusan Akademik   : {stats['persentase_lulus']}%")
            print("-------------------------------------------------------")
            print(" Kesimpulan Kelompok:")
            if stats['rata_rata_skor'] >= 70:
                print(" -> Mayoritas mahasiswa sudah memahami materi Akademik Psikologi dengan baik.")
            else:
                print(" -> Tingkat pemahaman materi masih rendah, disarankan melakukan evaluasi modul.")
                
        input("\nTekan Enter untuk kembali...")