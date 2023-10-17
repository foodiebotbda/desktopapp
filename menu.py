import tkinter as tk
import subprocess

class FoodApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x600+300+200")
        self.root.title("Aplikasi Input Makanan dan Kategori")
        self.root.config(bg="#06283D")

        self.create_menu_buttons()
        self.create_menu_kategori_makanan_buttons()


    def create_menu_buttons(self):
        btn_input_makanan = tk.Button(self.root, text="Input Makanan", command=self.run_input_makanan_script)
        btn_input_makanan.pack(pady=20)

    def create_menu_kategori_makanan_buttons(self):
        btn_input_kategori = tk.Button(self.root, text="Input Kategori", command=self.run_input_kategori_makanan_script)
        btn_input_kategori.pack(pady=40)

    def run_input_makanan_script(self):
        try:
            # Buka file main.py dalam jendela Tkinter yang sudah ada
            with open("main.py", "r") as main_file:
                exec(main_file.read(), globals(), locals())
        except Exception as e:
            print("Error:", str(e))

    def run_input_kategori_makanan_script(self):
        try:
            # Buka file main.py dalam jendela Tkinter yang sudah ada
            with open("kategori.py", "r") as main_file:
                exec(main_file.read(), globals(), locals())
        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodApp(root)
    root.mainloop()

