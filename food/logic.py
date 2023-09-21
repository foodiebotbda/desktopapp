
import json
import sqlite3

class FoodAppBackend:
    def __init__(self):
        self.conn = sqlite3.connect('cobak.db')
        self.cursor = self.conn.cursor()
        self.create_tables()  # Panggil fungsi ini untuk membuat tabel jika belum ada

    def create_tables(self):
        with open('databse.sql', 'r') as sql_file:  # Pastikan nama file dan pathnya sesuai
            sql_script = sql_file.read()
        self.cursor.executescript(sql_script)
        self.conn.commit()  # Simpan perubahan ke database

    def save_makanan(self, nama, tempat, gambar, harga):
        try:
            self.cursor.execute("INSERT INTO Makanan (nama_makanan, tempat, gambar, harga) VALUES (?, ?, ?, ?)",
                                (nama, tempat, gambar, harga))
            self.conn.commit()  # Simpan perubahan ke database
            return True
        except Exception as e:
            print("Error:", str(e))
            return False

    def save_kategori(self, id_makanan, deskripsi_makanan_list):
        try:
            # Mengonversi list deskripsi menjadi format JSON
            deskripsi_makanan_json = json.dumps(deskripsi_makanan_list)
            self.cursor.execute("INSERT INTO Kategori (id_makanan, deskripsi_makanan) VALUES (?, ?)",
                                (id_makanan, deskripsi_makanan_json))
            self.conn.commit()  # Simpan perubahan ke database
            return True
        except Exception as e:
            print("Error saat menyimpan data kategori:", str(e))
            return False
