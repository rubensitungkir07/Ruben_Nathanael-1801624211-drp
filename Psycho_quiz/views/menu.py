import os

class QuizAppMenu:
    def __init__(self, user_repo, quiz_service):
        # Menu ini butuh data user dan logika kuis yang dikirim dari luar
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
            print("1. Mulai Kuis Psikologi Baru")
            print("2. Lihat Riwayat Hasil Kuis (Leaderboard)")
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
        
        print(f"\nHalo {nama}, kuis dimulai!")
        input("Tekan Enter untuk memunculkan soal..."); self.clear_screen()

        questions = self.quiz_service.get_questions()
        user_answers = []

        for q in questions:
            print(f"\n[Soal] {q['pertanyaan']}")
            for opsi, teks_opsi in q['opsi'].items():
                print(f"  {opsi}. {teks_opsi}")
            
            jawaban = input("Jawaban kamu (A/B): ").upper()
            user_answers.append(jawaban)
            self.clear_screen()

        int_score, ext_score, tipe = self.quiz_service.analyze_personality(user_answers)
        self.quiz_service.save_quiz_result(nama, int_score, ext_score, tipe)

        print("🎉 KUIS SELESAI! 🎉")
        print(f"Nama             : {nama}")
        print(f"Tipe Psikologi   : {tipe}")
        input("\nTekan Enter untuk kembali ke menu...")

    def menu_lihat_hasil(self):
        self.clear_screen()
        print("=== 📊 RIWAYAT HASIL KUIS ===")
        results = self.quiz_service.get_leaderboard()
        for idx, r in enumerate(results, 1):
            print(f"{idx}. {r['nama']} -> {r['tipe_kepribadian']}")
        input("\nTekan Enter...")

    def menu_daftar_user(self):
        self.clear_screen()
        print("=== 👥 DAFTAR USER ===")
        users = self.user_repo.find_all_users()
        for idx, u in enumerate(users, 1):
            print(f"{idx}. {u['nama']} ({u['umur']} tahun)")
        input("\nTekan Enter...")