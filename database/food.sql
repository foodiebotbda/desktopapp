-- Tabel Makanan
CREATE TABLE IF NOT EXISTS Makanan (
    id_makanan INTEGER PRIMARY KEY,
    nama_makanan TEXT,
    tempat TEXT,
    gambar BLOB,
    harga REAL
);

-- Tabel Kategori
CREATE TABLE IF NOT EXISTS Kategori (
    id_kategori INTEGER PRIMARY KEY,
    deskripsi_makanan JSON,
    id_makanan INTEGER,
    FOREIGN KEY(id_makanan) REFERENCES Makanan(id_makanan)
);
