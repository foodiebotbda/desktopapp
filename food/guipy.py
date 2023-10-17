import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import io
import os
import requests

class FoodAppGUI:
    def get_kategori_options_from_server(self):
        response = requests.get('https://8cjrhv6h-8001.asse.devtunnels.ms/kategori_options')
        if response.status_code == 200:
            kategori_options = response.json()["kategori_options"]
            return kategori_options
        else:
            return []


    def __init__(self, root):
        self.root = root
        self.root.title("Food Entry")
        self.root.geometry("700x600+300+200")
        self.root.config(bg="#06283D")

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

            kategori_options = self.get_kategori_options_from_server()
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
            try:
                self.gambar = Image.open(file_path)
                self.gambar_label.config(text="Gambar Terpilih")

                # Store the file_path for later use
                self.file_path = file_path
            except FileNotFoundError:
                messagebox.showerror("Error", "File gambar tidak ditemukan.")
            except PIL.UnidentifiedImageError:
                messagebox.showerror("Error", "Format gambar tidak dikenali.")
            except Exception as e:
                messagebox.showerror("Error", f"Kesalahan saat membuka gambar: {str(e)}")

    def simpan_data(self):
        nama = self.nama_entry.get()
        tempat = self.tempat_entry.get()
        harga = float(self.harga_entry.get())
        selected_kategori_ids = []

        if hasattr(self, 'gambar'):
            try:
                # Convert gambar to data gambar biner
                image_bytes = io.BytesIO()
                self.gambar.save(image_bytes, format='PNG')
                image_binary = image_bytes.getvalue()

                # Create a directory to save images
                image_directory = "food_images"
                if not os.path.exists(image_directory):
                    os.makedirs(image_directory)

                # Generate a unique filename based on the food name
                image_filename = f"{nama}.png"

                # Save the image to the specified directory
                image_path = os.path.join(image_directory, image_filename)
                self.gambar.save(image_path, format='PNG')

            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengonversi gambar: {str(e)}")
                return

            for selected_kategori, _ in self.kategori_dropdowns:
                selected_kategori_desc = selected_kategori.get()
                if selected_kategori_desc:
                    # Mengganti ini dengan koneksi ke API Flask Anda untuk mendapatkan ID kategori berdasarkan deskripsi
                    # Anda perlu mengganti URL_API dengan URL sesuai dengan implementasi Anda
                    response = requests.get(f'https://8cjrhv6h-8001.asse.devtunnels.ms/kategori_id?description={selected_kategori_desc}')
                    if response.status_code == 200:
                        kategori_id = response.json()["id_kategori"]
                        selected_kategori_ids.append(kategori_id)

            if not selected_kategori_ids:
                messagebox.showerror("Error", "Harap pilih setidaknya satu kategori.")
                return

            # Mengganti ini dengan koneksi ke API Flask Anda untuk menyimpan data makanan
            # Anda perlu mengganti URL_API dengan URL sesuai dengan implementasi Anda
            response = requests.post('https://8cjrhv6h-8001.asse.devtunnels.ms/save_makanan', data={
                "nama": nama,
                "tempat": tempat,
                "harga": harga,
                "kategori_ids[]": selected_kategori_ids,
            }, files={"gambar": open(image_path, 'rb')})

            if response.status_code == 200:
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
    app = FoodAppGUI(root)
    root.mainloop()
