import os

class QuizAppMenu:
    def __init__(self, user_repo, quiz_service):
        self.user_repo = user_repo
        self.quiz_service = quiz_service

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show(self):
        while True:
            self.clear_screen()
            print("=============================================")
            print("   🧠 PSYCHO-GROUND: LIVE QUIZ APP CLI 🧠   ")
            print("=============================================")
            print("1. Mulai Kuis Materi Akademik Psikologi")
            print("2. Lihat Riwayat Hasil Ujian (Leaderboard)")
            print("3. Lihat Daftar Peserta")
            print("4. Keluar")
            print("=============================================")
            
            pilihan = input("Pilih menu (1-4): ")

            if pilihan == '1':
                self.menu_mulai_kuis()
            elif pilihan == '2':
                self.menu_lihat_hasil()
            elif pilihan == '3':
                self.menu_daftar_user()
            elif pilihan == '4':
                print("\nSampai jumpa!")
                break

    def menu_mulai_kuis(self):
        self.clear_screen()
        print("=== 📝 REGISTRASI PESERTA ===")
        nama = input("Masukkan nama: ")
        umur = input("Masukkan umur: ")
        
        self.user_repo.register_user(nama, umur)
        
        print(f"\nHalo {nama}, ujian materi psikologi dimulai!")
        input("Tekan Enter untuk memunculkan soal..."); self.clear_screen()

        questions = self.quiz_service.get_questions()
        user_answers = []

        for q in questions:
            print(f"\n[Soal] {q['pertanyaan']}")
            for opsi, teks_opsi in q['opsi'].items():
                print(f"  {opsi}. {teks_opsi}")
            
            # Validasi agar inputan wajib berkisar huruf A sampai D
            while True:
                jawaban = input("Jawaban kamu (A/B/C/D): ").upper()
                if jawaban in ['A', 'B', 'C', 'D']:
                    break
                print("Pilihan tidak valid! Tolong ketik A, B, C, atau D.")
                
            user_answers.append(jawaban)
            self.clear_screen()

        # Panggil logika penghitungan skor akademik terbaru
        skor_total, status_kelulusan = self.quiz_service.calculate_score(user_answers)
        self.quiz_service.save_quiz_result(nama, skor_total, status_kelulusan)

        print("🎉 UJIAN SELESAI! 🎉")
        print(f"Nama             : {nama}")
        print(f"Total Nilai      : {skor_total} / 100")
        print(f"Status           : {status_kelulusan.upper()}")
        input("\nTekan Enter untuk kembali ke menu...")

    def menu_lihat_hasil(self):
        self.clear_screen()
        print("=== 📊 RIWAYAT HASIL UJIAN ===")
        results = self.quiz_service.get_leaderboard()
        for idx, r in enumerate(results, 1):
            # Menampilkan data skor_total dan status kelulusan baru dari DB
            print(f"{idx}. {r['nama']} -> Nilai: {r['skor_total']} ({r['status']})")
        input("\nTekan Enter...")

    def menu_daftar_user(self):
        self.clear_screen()
        print("=== 👥 DAFTAR USER ===")
        users = self.user_repo.find_all_users()
        for idx, u in enumerate(users, 1):
            print(f"{idx}. {u['nama']} ({u['umur']} tahun)")
        input("\nTekan Enter...")