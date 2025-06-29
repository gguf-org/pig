
from gguf_connector.extractor import GGUFExtractorApp
import tkinter as tk

def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = GGUFExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
