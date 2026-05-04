import tkinter as tk
from movie_library import MovieLibrary

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()