import tkinter as tk
from tkinter import messagebox
from logickategori import FoodAppBackendKategori

class FoodAppGUIKategori:
    def __init__(self, root, backend):
        self.root = root
        self.root.title("Food Entry - Kategori")
        self.root.geometry("700x600+300+200")
        self.root.config(bg="#06283D")

        self.backend = backend

        self.deskripsi_entry = tk.Entry(self.root, font=("Arial", 12))
        self.deskripsi_entry.place(x=200, y=250)

        submit_button = tk.Button(self.root, text="Submit", command=self.tambah_data)
        submit_button.place(x=350, y=300)

    def tambah_data(self):
        deskripsi = self.deskripsi_entry.get()

        if deskripsi:
            if self.backend.save_kategori(deskripsi):
                messagebox.showinfo("Sukses", "Data berhasil ditambahkan ke tabel Kategori!")
                self.deskripsi_entry.delete(0, 'end')  # Mengosongkan input setelah submit
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")
        else:
            messagebox.showerror("Error", "Deskripsi makanan tidak boleh kosong.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    backend = FoodAppBackendKategori()
    app = FoodAppGUIKategori(root, backend)
    app.run()
