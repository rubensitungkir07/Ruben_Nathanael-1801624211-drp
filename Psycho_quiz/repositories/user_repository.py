class UserRepository:
    def __init__(self, db):
        # db di sini sekarang adalah dictionary tiruan dari file config
        self.collection = db['users']

    def register_user(self, nama, umur):
        user_data = {'nama': nama, 'umur': int(umur)}
        self.collection.append(user_data) # Perintah python biasa untuk menyimpan
        return user_data

    def find_all_users(self):
        return self.collection # Langsung mengembalikan semua list user
    
    def export_data(self, nama_file):
        self.quiz_repo.export_results_to_json(nama_file)

    def import_data(self, nama_file):
        self.quiz_repo.import_results_from_json(nama_file)