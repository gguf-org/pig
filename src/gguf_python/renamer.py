
from gguf_connector.renamer import GGUFEditorApp
import tkinter as tk

def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = GGUFEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
