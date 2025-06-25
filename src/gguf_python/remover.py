
from gguf_connector.remover import GGUFRemoverApp
import tkinter as tk

def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = GGUFRemoverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
