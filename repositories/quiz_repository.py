class QuizRepository:
    def __init__(self, db):
        self.quiz_collection = db['quizzes']
        self.result_collection = db['results']
        self._seed_quiz_if_empty()

    def _seed_quiz_if_empty(self):
        # Mengisi soal otomatis di dalam codingan langsung
        if len(self.quiz_collection) == 0:
            dummy_questions = [
                {
                    "id": 1,
                    "pertanyaan": "Saat berada di keramaian atau pesta, apa yang kamu rasakan?",
                    "opsi": {"A": "Sangat berenergi (Extrovert)", "B": "Cepat lelah (Introvert)"}
                },
                {
                    "id": 2,
                    "pertanyaan": "Bagaimana kamu mengambil keputusan penting?",
                    "opsi": {"A": "Menggunakan logika (Thinking)", "B": "Mengikuti kata hati (Feeling)"}
                }
            ]
            self.quiz_collection.extend(dummy_questions)

    def get_all_questions(self):
        return self.quiz_collection

    def save_result(self, nama, skor_introvert, skor_extrovert, tipe):
        result_data = {
            "nama": nama,
            "skor_introvert": skor_introvert,
            "skor_extrovert": skor_extrovert,
            "tipe_kepribadian": tipe
        }
        self.result_collection.append(result_data)

    def get_all_results(self):
        return self.result_collection