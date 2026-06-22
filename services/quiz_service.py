class QuizService:
    def __init__(self, quiz_repo):
        self.quiz_repo = quiz_repo

    def get_questions(self):
        return self.quiz_repo.get_all_questions()

    def calculate_score(self, answers):
        questions = self.get_questions()
        total_soal = len(questions)
        jawaban_benar_count = 0

        for idx, q in enumerate(questions):
            if idx < len(answers) and answers[idx] == q['jawaban_benar']:
                jawaban_benar_count += 1
        
        skor_total = int((jawaban_benar_count / total_soal) * 100) if total_soal > 0 else 0
        status_kelulusan = "Lulus" if skor_total >= 70 else "Tidak Lulus"
        
        return skor_total, status_kelulusan

    def save_quiz_result(self, nama, skor_total, status_kelulusan):
        self.quiz_repo.save_result(nama, skor_total, status_kelulusan)

    def get_leaderboard(self):
        return self.quiz_repo.get_all_results()

    def get_users(self):
        return self.quiz_repo.get_all_users()

    def register_new_user(self, nama, umur):
        self.quiz_repo.register_user(nama, umur)

    def update_soal(self, id_quiz, jawaban_baru):
        self.quiz_repo.update_quiz_answer(id_quiz, jawaban_baru)

    def reset_leaderboard(self):
        self.quiz_repo.delete_all_results()