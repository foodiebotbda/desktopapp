import tkinter as tk
import sys
sys.path.append('category')
from category.guikategori import FoodAppGUIKategori
from category.logickategori import FoodAppBackendKategori


if __name__ == "__main__":
    root = tk.Tk()
    backend = FoodAppBackendKategori()
    app = FoodAppGUIKategori(root, backend)
    app.run()
