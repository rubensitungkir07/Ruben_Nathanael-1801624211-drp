class QuizService:
    def __init__(self, quiz_repo):
        self.quiz_repo = quiz_repo

    def get_questions(self):
        return self.quiz_repo.get_all_questions()

    def calculate_score(self, answers):
        # Mengambil semua soal asli dari repository untuk mencocokkan kunci jawaban
        questions = self.get_questions()
        total_soal = len(questions)
        jawaban_benar_count = 0

        # Cocokkan jawaban user berdasarkan ID Soal
        for idx, q in enumerate(questions):
            if idx < len(answers) and answers[idx] == q['jawaban_benar']:
                jawaban_benar_count += 1
        
        # Hitung skor matematika skala 100
        if total_soal > 0:
            skor_total = int((jawaban_benar_count / total_soal) * 100)
        else:
            skor_total = 0

        # Tentukan status kelulusan (Batasan kelulusan KKM: 70)
        status_kelulusan = "Lulus" if skor_total >= 70 else "Tidak Lulus"
        
        return skor_total, status_kelulusan

    def save_quiz_result(self, nama, skor_total, status_kelulusan):
        # Menyambungkan ke parameter repositori baru akademik
        self.quiz_repo.save_result(nama, skor_total, status_kelulusan)

    def get_leaderboard(self):
        return self.quiz_repo.get_all_results()