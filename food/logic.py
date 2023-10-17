from flask import Flask, request, jsonify
import mysql.connector
import hashlib
import os
import shutil

app = Flask(__name__)

class FoodAppBackend:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3306,
            password="12345",
            database="FoodAppDatabase"
        )
        self.cursor = self.conn.cursor()

    def hash_gambar(self, image_binary):
        # Menghitung hash dari gambar_binary
        return hashlib.md5(image_binary).hexdigest()

    def save_makanan(self, nama, tempat, image_binary, harga, kategori_ids, image_path):
        try:
            # Menghitung hash dari gambar
            hash_gambar = self.hash_gambar(image_binary)

            # Menyimpan data bersama dengan hash gambar
            self.cursor.execute("INSERT INTO Makanan (nama_makanan, tempat, gambar, harga) VALUES (%s, %s, %s, %s)",
                                (nama, tempat, hash_gambar, harga))
            self.conn.commit()
            id_makanan = self.cursor.lastrowid

            # Menyimpan hubungan antara makanan dan kategori di tabel Kategori_Makanan
            for id_kategori in kategori_ids:
                self.cursor.execute("INSERT INTO Kategori_Makanan (id_kategori, id_makanan) VALUES (%s, %s)",
                                    (id_kategori, id_makanan))
                self.conn.commit()

            # Menyalin gambar ke direktori yang ditentukan dengan nama file berdasarkan nama makanan
            image_directory = "../gambar"
            image_filename = f"{nama}.png"
            image_destination = os.path.join(image_directory, image_filename)

            if not os.path.exists(image_destination):
                shutil.copy(image_path, image_destination)
            else:
                # Membuat nama unik jika makanan dengan nama yang sama sudah ada
                base_name, ext = os.path.splitext(image_filename)
                counter = 1
                while os.path.exists(image_destination):
                    image_filename = f"{base_name}_{counter}{ext}"
                    image_destination = os.path.join(image_directory, image_filename)
                    counter += 1
                shutil.copy(image_path, image_destination)

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

# Create an instance of FoodAppBackend
food_app = FoodAppBackend()

@app.route('/save_makanan', methods=['POST'])
def save_makanan():
    try:
        nama = request.form['nama']
        tempat = request.form['tempat']
        image_binary = request.files['gambar'].read()
        harga = request.form['harga']
        kategori_ids = request.form.getlist('kategori_ids[]')
        image_path = request.files['gambar'].filename

        # Call the save_makanan method of FoodAppBackend
        success = food_app.save_makanan(nama, tempat, image_binary, harga, kategori_ids, image_path)

        if success:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Failed to save makanan"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/kategori_options', methods=['GET'])
def get_kategori_options():
    kategori_options = food_app.get_kategori_options()
    return jsonify({"kategori_options": kategori_options})

@app.route('/kategori_id', methods=['GET'])
def get_kategori_id():
    description = request.args.get('description')
    id_kategori = food_app.get_kategori_id_by_description(description)
    return jsonify({"id_kategori": id_kategori})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
