class QuizService:
    def __init__(self, quiz_repo):
        # Menerima repository kuis dari luar
        self.quiz_repo = quiz_repo

    def get_questions(self):
        return self.quiz_repo.get_all_questions()

    def analyze_personality(self, answers):
        # Logika sederhana: Hitung jumlah jawaban
        introvert_point = answers.count('B')
        extrovert_point = answers.count('A')
        
        if introvert_point > extrovert_point:
            tipe = "Introvert (Kekuatan dalam ketenangan)"
        elif extrovert_point > introvert_point:
            tipe = "Extrovert (Kekuatan dalam interaksi)"
        else:
            tipe = "Ambivert (Seimbang)"
            
        return introvert_point, extrovert_point, tipe

    def save_quiz_result(self, nama, introvert, extrovert, tipe):
        self.quiz_repo.save_result(nama, introvert, extrovert, tipe)

    def get_leaderboard(self):
        return self.quiz_repo.get_all_results()