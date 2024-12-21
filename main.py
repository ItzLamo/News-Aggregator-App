import tkinter as tk
from src.gui import NewsAggregatorGUI
import requests

def main():
    root = tk.Tk()
    app = NewsAggregatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
