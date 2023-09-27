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

        self.kategori_labels = []
        self.kategori_dropdowns = []

        for i in range(1, 11):
            kategori_label = tk.Label(root, text=f"Kategori {i}", font=("Arial", 12), bg="#06283D", fg="#fff")
            kategori_label.place(x=50, y=250 + i * 40)
            self.kategori_labels.append(kategori_label)

            kategori_options = self.backend.get_kategori_descriptions()
            selected_kategori = tk.StringVar(root)
            kategori_dropdown = tk.OptionMenu(root, selected_kategori, *kategori_options)
            kategori_dropdown.config(font=("Arial", 12))
            kategori_dropdown.place(x=200, y=250 + i * 40)
            self.kategori_dropdowns.append((selected_kategori, kategori_dropdown))

        self.simpan_button = tk.Button(root, text="Simpan", font=("Arial", 12), command=self.simpan_data)
        self.simpan_button.place(x=200, y=600)

    def import_gambar(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.gambar = Image.open(file_path)
            self.gambar_label.config(text="Gambar Terpilih")

    def simpan_data(self):
        nama = self.nama_entry.get()
        tempat = self.tempat_entry.get()
        harga = float(self.harga_entry.get())
        selected_kategori_ids = []

        if hasattr(self, 'gambar'):
            try:
                image_bytes = io.BytesIO()
                self.gambar.save(image_bytes, format='PNG')
                image_binary = image_bytes.getvalue()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengonversi gambar: {str(e)}")
                return

            for selected_kategori, _ in self.kategori_dropdowns:
                selected_kategori_desc = selected_kategori.get()
                # Cek apakah dropdown kategori telah dipilih
                if selected_kategori_desc:
                    # Cari ID kategori berdasarkan deskripsi
                    kategori_id = self.backend.get_kategori_id_by_description(selected_kategori_desc)
                    selected_kategori_ids.append(kategori_id)

            # Cek apakah setidaknya satu kategori telah dipilih
            if not selected_kategori_ids:
                messagebox.showerror("Error", "Harap pilih setidaknya satu kategori.")
                return

            if self.backend.save_makanan(nama, tempat, image_binary, harga, selected_kategori_ids):
                messagebox.showinfo("Sukses", "Data makanan berhasil disimpan.")
                self.nama_entry.delete(0, tk.END)
                self.tempat_entry.delete(0, tk.END)
                self.harga_entry.delete(0, tk.END)
                for selected_kategori, _ in self.kategori_dropdowns:
                    selected_kategori.set("")  # Reset dropdown kategori
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
