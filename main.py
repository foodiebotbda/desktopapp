import tkinter as tk
import sys
sys.path.append('food')
from food.guipy import FoodAppGUI
from food.logic import FoodAppBackend

if __name__ == "__main__":
    root = tk.Tk()
    backend = FoodAppBackend()
    app = FoodAppGUI(root, backend)
    root.mainloop()
