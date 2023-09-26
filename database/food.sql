

CREATE DATABASE IF NOT EXISTS FoodAppDatabase;
   
-- Gunakan database yang telah dibuat
USE FoodAppDatabase;

CREATE TABLE IF NOT EXISTS Makanan (
    id_makanan INT AUTO_INCREMENT PRIMARY KEY,
    nama_makanan VARCHAR(255),
    tempat VARCHAR(255),
    gambar LONGBLOB,
    harga DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS Kategori (
    id_kategori INT AUTO_INCREMENT PRIMARY KEY,
    deskripsi_makanan JSON,
    id_makanan INT,
    FOREIGN KEY (id_makanan) REFERENCES Makanan (id_makanan)
);
