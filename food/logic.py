
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

    def save_makanan(self, nama, tempat, gambar, harga, kategori_ids):
        try:
            # Simpan data makanan
            self.cursor.execute("INSERT INTO Makanan (nama_makanan, tempat, gambar, harga) VALUES (%s, %s, %s, %s)",
                                (nama, tempat, gambar, harga))
            self.conn.commit()  # Simpan perubahan ke database
            id_makanan = self.cursor.lastrowid  # Ambil ID makanan yang baru saja disimpan

            # Simpan hubungan antara makanan dan kategori di tabel Kategori_Makanan
            for id_kategori in kategori_ids:
                self.cursor.execute("INSERT INTO Kategori_Makanan (id_kategori, id_makanan) VALUES (%s, %s)",
                                    (id_kategori, id_makanan))
                self.conn.commit()

            return True
        except Exception as e:
            print("Error:", str(e))
            return False

    def get_kategori_options(self):
        try:
            self.cursor.execute("SELECT deskripsi_makanan FROM Kategori")
            kategori_records = self.cursor.fetchall()
            kategori_options = [record[0] for record in kategori_records]
            return kategori_options
        except Exception as e:
            print("Error:", str(e))
            return []

    def get_kategori_descriptions(self):
        try:
            self.cursor.execute("SELECT deskripsi_makanan FROM Kategori")
            kategori_records = self.cursor.fetchall()
            kategori_descriptions = [record[0] for record in kategori_records]
            return kategori_descriptions
        except Exception as e:
            print("Error:", str(e))
            return []

    def get_kategori_id_by_description(self, description):
        try:
            self.cursor.execute("SELECT id_kategori FROM Kategori WHERE deskripsi_makanan = %s", (description,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print("Error:", str(e))
            return None

    def __del__(self):
        self.cursor.close()
        self.conn.close()
