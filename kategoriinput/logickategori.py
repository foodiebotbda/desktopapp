import mysql.connector
from mysql.connector import Error

class FoodAppBackendKategori:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3308,
            password="maria",
            database="FoodAppDatabase"
        )

    def save_kategori(self, deskripsi):
        try:
            cursor = self.conn.cursor()

            query = "INSERT INTO Kategori (deskripsi_makanan) VALUES (%s)"
            values = (deskripsi,)

            cursor.execute(query, values)
            self.conn.commit()

            return True
        except Error as e:
            print(f"Terjadi kesalahan: {e}")
            return False
        finally:
            if self.conn.is_connected():
                cursor.close()

    def __del__(self):
        if self.conn.is_connected():
            self.conn.close()
