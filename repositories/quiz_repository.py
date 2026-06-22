import sqlite3
from datetime import datetime

class QuizRepository:
    def __init__(self):
        # Membuat otomatis file database SQLite lokal
        self.db_name = "psycho_quiz.db"
        self._create_tables()
        self._seed_quiz_if_empty()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        # Membuat tabel USERS, QUIZZES, dan RESULTS sesuai ERD Tugas 10
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Tabel Users
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    umur INTEGER NOT NULL
                )
            ''')
            
            # 2. Tabel Quizzes
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
            
            # 3. Tabel Results (Ditambah kolom waktu_ujian otomatis)
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
        # C - CREATE (Mempersiapkan Bank Soal Otomatis)
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

    # ==================== OPERATIONS (CRUD) ====================

    # 1. READ: Ambil Semua Soal
    def get_all_questions(self):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM quizzes")
            return [dict(row) for row in cursor.fetchall()]

    # 2. CREATE: Simpan Hasil Ujian (Menggunakan datetime otomatis)
    def save_result(self, nama, skor_total, status_kelulusan):
        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Logic otomatis sesuai petunjuk tugas!
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO results (nama_peserta, skor_total, status, waktu_ujian)
                VALUES (?, ?, ?, ?)
            ''', (nama, skor_total, status_kelulusan, waktu_sekarang))
            conn.commit()

    # 3. READ: Ambil Semua Hasil (Leaderboard)
    def get_all_results(self):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM results ORDER BY skor_total DESC")
            return [dict(row) for row in cursor.fetchall()]

    # 4. CREATE: Registrasi User Baru
    def register_user(self, nama, umur):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (nama, umur) VALUES (?, ?)", (nama, umur))
            conn.commit()

    # 5. READ: Ambil Semua User
    def get_all_users(self):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            return [dict(row) for row in cursor.fetchall()]

    # 6. UPDATE: Mengubah Kunci Jawaban Soal (Fitur Koreksi Admin)
    def update_quiz_answer(self, id_quiz, jawaban_baru):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE quizzes SET jawaban_benar = ? WHERE id_quiz = ?", (jawaban_baru, id_quiz))
            conn.commit()

    # 7. DELETE: Reset / Hapus Semua Riwayat Nilai
    def delete_all_results(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM results")
            conn.commit()