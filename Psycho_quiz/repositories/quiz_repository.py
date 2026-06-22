import sqlite3
import json
from datetime import datetime

class QuizRepository:
    def __init__(self):
        self.db_name = "psycho_quiz.db"
        self._create_tables()
        self._seed_quiz_if_empty()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    umur INTEGER NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quizzes (
                    id_quiz INTEGER PRIMARY KEY AUTOINCREMENT,
                    pertanyaan TEXT NOT NULL,
                    opsi_A TEXT NOT NULL,
                    opsi_B TEXT NOT NULL,
                    opsi_C TEXT NOT NULL,
                    opsi_D TEXT NOT NULL,
                    jawaban_benar TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id_result INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_peserta TEXT NOT NULL,
                    skor_total INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    waktu_ujian TEXT NOT NULL
                )
            ''')
            conn.commit()

    def _seed_quiz_if_empty(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM quizzes")
            if cursor.fetchone()[0] == 0:
                dummy_questions = [
                    ("Dalam teori psikoanalisis Freud, struktur yang beroperasi berdasarkan prinsip kesenangan adalah...", "Id", "Ego", "Superego", "Altered Ego", "A"),
                    ("Siapakah tokoh psikologi yang terkenal sebagai Bapak Behaviorisme?", "Wilhelm Wundt", "John B. Watson", "B.F. Skinner", "Ivan Pavlov", "B"),
                    ("Cabang ilmu psikologi yang mempelajari perkembangan manusia dari konsepsi hingga lansia adalah...", "Klinis", "Sosial", "Perkembangan", "Kognitif", "C")
                ]
                cursor.executemany('''
                    INSERT INTO quizzes (pertanyaan, opsi_A, opsi_B, opsi_C, opsi_D, jawaban_benar)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', dummy_questions)
                conn.commit()

    def get_all_questions(self):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM quizzes")
            return [dict(row) for row in cursor.fetchall()]

    def save_result(self, nama, skor_total, status_kelulusan):
        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO results (nama_peserta, skor_total, status, waktu_ujian)
                VALUES (?, ?, ?, ?)
            ''', (nama, skor_total, status_kelulusan, waktu_sekarang))
            conn.commit()

    def get_all_results(self):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM results ORDER BY skor_total DESC")
            return [dict(row) for row in cursor.fetchall()]

    def register_user(self, nama, umur):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (nama, umur) VALUES (?, ?)", (nama, umur))
            conn.commit()

    def get_all_users(self):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            return [dict(row) for row in cursor.fetchall()]

    def update_quiz_answer(self, id_quiz, jawaban_baru):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE quizzes SET jawaban_benar = ? WHERE id_quiz = ?", (jawaban_baru, id_quiz))
            conn.commit()

    def delete_all_results(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM results")
            conn.commit()

    def export_results_to_json(self, file_path):
        data_nilai = self.get_all_results()
        with open(file_path, 'w') as json_file:
            json.dump(data_nilai, json_file, indent=4)

    def import_results_from_json(self, file_path):
        with open(file_path, 'r') as json_file:
            data_imported = json.load(json_file)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for r in data_imported:
                cursor.execute('''
                    INSERT INTO results (nama_peserta, skor_total, status, waktu_ujian)
                    VALUES (?, ?, ?, ?)
                ''', (r['nama_peserta'], r['skor_total'], r['status'], r['waktu_ujian']))
            conn.commit()

    # ==================== FITUR BARU TUGAS 13: PENGOLAHAN DATA STATISTIK ====================
    def calculate_quiz_statistics(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Hitung total peserta yang sudah ujian
            cursor.execute("SELECT COUNT(*) FROM results")
            total_peserta = cursor.fetchone()[0]
            
            if total_peserta == 0:
                return None
                
            # 2. Hitung rata-rata skor nilai ujian (Komputasi Matematika)
            cursor.execute("SELECT AVG(skor_total) FROM results")
            rata_rata_skor = round(cursor.fetchone()[0], 2)
            
            # 3. Hitung jumlah peserta yang berstatus Lulus
            cursor.execute("SELECT COUNT(*) FROM results WHERE status = 'Lulus'")
            total_lulus = cursor.fetchone()[0]
            
            # 4. Hitung persentase kelulusan kelas
            persentase_lulus = round((total_lulus / total_peserta) * 100, 2)
            
            return {
                "total_peserta": total_peserta,
                "rata_rata_skor": rata_rata_skor,
                "total_lulus": total_lulus,
                "total_tidak_lulus": total_peserta - total_lulus,
                "persentase_lulus": persentase_lulus
            }