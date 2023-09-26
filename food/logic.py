
import json
import sqlite3
import mysql.connector
class FoodAppBackend:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3308,
            password="maria",
            database="FoodAppDatabase"
        )
        self.cursor = self.conn.cursor()
    # def save_makanan(self, nama, tempat, gambar, harga):
    #     try:
    #         self.cursor.execute("INSERT INTO Makanan (nama_makanan, tempat, gambar, harga) VALUES (?, ?, ?, ?)",
    #                             (nama, tempat, gambar, harga))
    #         self.conn.commit()  # Simpan perubahan ke database
    #         return True
    #     except Exception as e:
    #         print("Error:", str(e))
    #         return False

    # def save_kategori(self, id_makanan, deskripsi_makanan_list):
    #     try:
    #         # Mengonversi list deskripsi menjadi format JSON
    #         deskripsi_makanan_json = json.dumps(deskripsi_makanan_list)
    #         self.cursor.execute("INSERT INTO Kategori (id_makanan, deskripsi_makanan) VALUES (?, ?)",
    #                             (id_makanan, deskripsi_makanan_json))
    #         self.conn.commit()  # Simpan perubahan ke database
    #         return True
    #     except Exception as e:
    #         print("Error saat menyimpan data kategori:", str(e))
    #         return False
    def save_makanan(self, nama, tempat, gambar, harga):
        try:
            self.cursor.execute("INSERT INTO Makanan (nama_makanan, tempat, gambar, harga) VALUES (%s, %s, %s, %s)",
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
            self.cursor.execute("INSERT INTO Kategori (id_makanan, deskripsi_makanan) VALUES (%s, %s)",
                                (id_makanan, deskripsi_makanan_json))
            self.conn.commit()  # Simpan perubahan ke database
            return True
        except Exception as e:
            print("Error saat menyimpan data kategori:", str(e))
            return False
