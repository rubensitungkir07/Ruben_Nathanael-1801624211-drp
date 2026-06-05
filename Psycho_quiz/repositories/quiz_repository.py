class QuizRepository:
    def __init__(self, db):
        self.quiz_collection = db['quizzes']
        self.result_collection = db['results']
        self._seed_quiz_if_empty()

    def _seed_quiz_if_empty(self):
        # Mengisi soal otomatis materi perkuliahan psikologi jika database kosong
        if len(self.quiz_collection) == 0:
            dummy_questions = [
                {
                    "id": 1,
                    "pertanyaan": "Dalam teori psikoanalisis Sigmund Freud, struktur kepribadian yang beroperasi berdasarkan 'prinsip kesenangan' (pleasure principle) adalah...",
                    "opsi": {"A": "Id", "B": "Ego", "C": "Superego", "D": "Altered Ego"},
                    "jawaban_benar": "A"
                },
                {
                    "id": 2,
                    "pertanyaan": "Siapakah tokoh psikologi yang terkenal sebagai Bapak Behaviorisme dan melakukan eksperimen 'Little Albert'?",
                    "opsi": {"A": "Wilhelm Wundt", "B": "John B. Watson", "C": "B.F. Skinner", "D": "Ivan Pavlov"},
                    "jawaban_benar": "B"
                },
                {
                    "id": 3,
                    "pertanyaan": "Cabang ilmu psikologi yang mempelajari perkembangan manusia dari masa konsepsi hingga lansia disebut psikologi...",
                    "opsi": {"A": "Klinis", "B": "Sosial", "C": "Perkembangan", "D": "Kognitif"},
                    "jawaban_benar": "C"
                }
            ]
            self.quiz_collection.extend(dummy_questions)

    def get_all_questions(self):
        return self.quiz_collection

    def save_result(self, nama, skor_total, status_kelulusan):
        # Menyimpan hasil ujian materi psikologi dengan skema nilai baru
        result_data = {
            "nama": nama,
            "skor_total": skor_total,          # Berisi nilai angka (misal: 70, 100)
            "status": status_kelulusan          # Berisi teks "Lulus" atau "Tidak Lulus"
        }
        self.result_collection.append(result_data)

    def get_all_results(self):
        return self.result_collection