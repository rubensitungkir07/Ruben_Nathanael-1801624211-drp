from config.database import get_database
from repositories.user_repository import UserRepository
from repositories.quiz_repository import QuizRepository
from services.quiz_service import QuizService
from views.menu import QuizAppMenu

if __name__ == '__main__':
    try:
        # 1. Ambil database
        db = get_database()
        
        # 2. Masukkan db ke dalam repository (Suntik Dependensi)
        user_repo = UserRepository(db)
        quiz_repo = QuizRepository(db)
        
        # 3. Masukkan repository ke dalam service (Suntik Dependensi)
        quiz_service = QuizService(quiz_repo)
        
        # 4. Masukkan semua komponen ke dalam Menu Utama
        app = QuizAppMenu(user_repo, quiz_service)
        
        # 5. Jalankan aplikasi kuis
        app.show()
        
    except Exception as e:
        print(f"Gagal memuat aplikasi: {e}")
        print("Pastikan aplikasi MongoDB Compass/Server kamu sudah dinyalakan!")