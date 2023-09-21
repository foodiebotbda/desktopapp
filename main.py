import tkinter as tk
from guipy import FoodAppGUI
from logic import FoodAppBackend

if __name__ == "__main__":
    root = tk.Tk()
    backend = FoodAppBackend()
    app =FoodAppGUI(root, backend)
    root.mainloop()     