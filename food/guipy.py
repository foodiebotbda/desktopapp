
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from logic import FoodAppBackend
import io

class FoodAppGUI:
    def __init__(self, root, backend):
        self.root = root
        self.root.title("Food Entry")
        self.root.geometry("700x600+300+200")
        self.root.config(bg="#06283D")
        self.backend = backend
        self.deskripsi_makanan_entries = []  # List untuk menyimpan 7 deskripsi makanan

        self.nama_label = tk.Label(root, text="Nama Makanan", font=("Arial", 12), bg="#06283D", fg="#fff")
        self.nama_label.place(x=50, y=90)

        self.nama_entry = tk.Entry(root, font=("Arial", 12))
        self.nama_entry.place(x=200, y=90)

        self.tempat_label = tk.Label(root, text="Tempat", font=("Arial", 12), bg="#06283D", fg="#fff")
        self.tempat_label.place(x=50, y=130)

        self.tempat_entry = tk.Entry(root, font=("Arial", 12))
        self.tempat_entry.place(x=200, y=130)

        self.harga_label = tk.Label(root, text="Harga", font=("Arial", 12), bg="#06283D", fg="#fff")
        self.harga_label.place(x=50, y=170)

        self.harga_entry = tk.Entry(root, font=("Arial", 12))
        self.harga_entry.place(x=200, y=170)

        self.gambar_label = tk.Label(root, text="Gambar", font=("Arial", 12), bg="#06283D", fg="#fff")
        self.gambar_label.place(x=50, y=210)

        self.gambar_button = tk.Button(root, text="Pilih Gambar", font=("Arial", 12), command=self.import_gambar)
        self.gambar_button.place(x=200, y=210)

        self.kategori_label = tk.Label(root, text="Kategori", font=("Arial", 12), bg="#06283D", fg="#fff")
        self.kategori_label.place(x=50, y=250)

        for i in range(10):
            deskripsi_entry = tk.Entry(root, font=("Arial", 12))
            deskripsi_entry.place(x=200, y=250 + (i * 40))
            self.deskripsi_makanan_entries.append(deskripsi_entry)
        for i in range(10):
            deskripsi_entry = tk.Entry(root, font=("Arial", 12))
            deskripsi_entry.place(x=400, y=250 + (i * 40))
            self.deskripsi_makanan_entries.append(deskripsi_entry)

        self.simpan_button = tk.Button(root, text="Simpan", font=("Arial", 12), command=self.simpan_data)
        self.simpan_button.place(x=200, y=650)

    def import_gambar(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.gambar = Image.open(file_path)
            self.gambar_label.config(text="Gambar Terpilih")

    def simpan_data(self):
        nama = self.nama_entry.get()
        tempat = self.tempat_entry.get()
        harga = float(self.harga_entry.get())
        deskripsi_makanan_list = [entry.get() for entry in self.deskripsi_makanan_entries if entry.get()]

        if hasattr(self, 'gambar'):
            try:
                image_bytes = io.BytesIO()
                self.gambar.save(image_bytes, format='PNG')
                image_binary = image_bytes.getvalue()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengonversi gambar: {str(e)}")
                return

            if self.backend.save_makanan(nama, tempat, image_binary, harga):
                id_makanan = self.backend.cursor.lastrowid  # Ambil ID makanan yang baru saja disimpan

                # Simpan setiap deskripsi makanan ke database
                for deskripsi in deskripsi_makanan_list:
                    self.backend.save_kategori(id_makanan, deskripsi)

                messagebox.showinfo("Sukses", "Data makanan dan kategori berhasil disimpan.")
                self.nama_entry.delete(0, tk.END)
                self.tempat_entry.delete(0, tk.END)
                self.harga_entry.delete(0, tk.END)
                for deskripsi_entry in self.deskripsi_makanan_entries:
                    deskripsi_entry.delete(0, tk.END)
                self.gambar_label.config(text="")  # Reset label gambar
            else:
                messagebox.showerror("Error", "Gagal menyimpan data makanan.")
        else:
            messagebox.showerror("Error", "Harap pilih gambar terlebih dahulu.")


if __name__ == "__main__":
    root = tk.Tk()
    backend = FoodAppBackend()
    app = FoodAppGUI(root, backend)
    root.mainloop()

