from repositories.quiz_repository import QuizRepository
from services.quiz_service import QuizService
from views.menu import QuizAppMenu

if __name__ == '__main__':
    try:
        # Inisialisasi Repository SQLite (Tanpa memasukkan parameter db!)
        quiz_repo = QuizRepository()
        quiz_service = QuizService(quiz_repo)
        
        # Jalankan Menu Aplikasi
        app = QuizAppMenu(quiz_service)
        app.show()
        
    except Exception as e:
        print(f"Gagal memuat aplikasi: {e}")