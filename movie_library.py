import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "data/movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Movie Library — Личная кинотека")
        self.root.geometry("850x550")
        self.root.resizable(False, False)

        self.movies = []
        self.load_data()

        self.title_var = tk.StringVar()
        self.genre_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.rating_var = tk.StringVar()
        self.filter_genre_var = tk.StringVar()
        self.filter_year_var = tk.StringVar()

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        input_frame = ttk.LabelFrame(self.root, text="➕ Добавить фильм", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry = ttk.Entry(input_frame, textvariable=self.title_var, width=25)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Жанр:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.genre_entry = ttk.Entry(input_frame, textvariable=self.genre_var, width=15)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Год:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.year_entry = ttk.Entry(input_frame, textvariable=self.year_var, width=8)
        self.year_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=0, column=6, padx=5, pady=5, sticky="w")
        self.rating_entry = ttk.Entry(input_frame, textvariable=self.rating_var, width=6)
        self.rating_entry.grid(row=0, column=7, padx=5, pady=5)

        add_btn = ttk.Button(input_frame, text="🎬 Добавить", command=self.add_movie)
        add_btn.grid(row=0, column=8, padx=10, pady=5)

        filter_frame = ttk.LabelFrame(self.root, text="🔍 Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Жанр:").pack(side="left", padx=5)
        self.filter_genre_entry = ttk.Entry(filter_frame, textvariable=self.filter_genre_var, width=15)
        self.filter_genre_entry.pack(side="left", padx=5)

        ttk.Label(filter_frame, text="Год:").pack(side="left", padx=5)
        self.filter_year_entry = ttk.Entry(filter_frame, textvariable=self.filter_year_var, width=8)
        self.filter_year_entry.pack(side="left", padx=5)

        filter_btn = ttk.Button(filter_frame, text="🔍 Применить фильтр", command=self.apply_filter)
        filter_btn.pack(side="left", padx=5)

        reset_btn = ttk.Button(filter_frame, text="❌ Сбросить", command=self.reset_filter)
        reset_btn.pack(side="left", padx=5)

        columns = ("id", "title", "genre", "year", "rating")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=18)
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        self.tree.column("id", width=50)
        self.tree.column("title", width=250)
        self.tree.column("genre", width=150)
        self.tree.column("year", width=80)
        self.tree.column("rating", width=80)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        delete_btn = ttk.Button(btn_frame, text="🗑️ Удалить выбранное", command=self.delete_movie)
        delete_btn.pack(side="left", padx=5)

        stats_btn = ttk.Button(btn_frame, text="📊 Статистика", command=self.show_stats)
        stats_btn.pack(side="left", padx=5)

    def validate_year(self, year_str):
        try:
            year = int(year_str)
            if year < 1888 or year > datetime.now().year + 5:
                raise ValueError(f"Год должен быть от 1888 до {datetime.now().year + 5}")
            return year
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Некорректный год: {e}")
            return None

    def validate_rating(self, rating_str):
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                raise ValueError("Рейтинг должен быть от 0 до 10")
            return round(rating, 1)
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Некорректный рейтинг: {e}")
            return None

    def add_movie(self):
        title = self.title_var.get().strip()
        genre = self.genre_var.get().strip()
        year_str = self.year_var.get().strip()
        rating_str = self.rating_var.get().strip()

        if not title:
            messagebox.showerror("Ошибка", "Введите название фильма")
            return

        if not genre:
            messagebox.showerror("Ошибка", "Введите жанр")
            return

        year = self.validate_year(year_str)
        if year is None:
            return

        rating = self.validate_rating(rating_str)
        if rating is None:
            return

        new_id = max([m["id"] for m in self.movies], default=0) + 1
        movie = {
            "id": new_id,
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        self.movies.append(movie)
        self.save_data()
        self.refresh_table()
        self.title_var.set("")
        self.genre_var.set("")
        self.year_var.set("")
        self.rating_var.set("")
        messagebox.showinfo("Успех", f"Фильм \"{title}\" добавлен!")

    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления")
            return

        item = self.tree.item(selected[0])
        movie_id = item["values"][0]
        movie_title = item["values"][1]

        if messagebox.askyesno("Подтверждение", f"Удалить фильм \"{movie_title}\"?"):
            self.movies = [m for m in self.movies if m["id"] != movie_id]
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Успех", "Фильм удалён")

    def apply_filter(self):
        filter_genre = self.filter_genre_var.get().strip().lower()
        filter_year = self.filter_year_var.get().strip()

        filtered = self.movies.copy()

        if filter_genre:
            filtered = [m for m in filtered if filter_genre in m["genre"].lower()]

        if filter_year:
            try:
                year_int = int(filter_year)
                filtered = [m for m in filtered if m["year"] == year_int]
            except ValueError:
                messagebox.showerror("Ошибка", "Год для фильтрации должен быть числом")
                return

        self.refresh_table(filtered)

    def reset_filter(self):
        self.filter_genre_var.set("")
        self.filter_year_var.set("")
        self.refresh_table()

    def refresh_table(self, data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        if data is None:
            data = self.movies

        for movie in data:
            stars = "⭐" * min(5, int(movie["rating"] // 2))
            rating_display = f"{movie['rating']:.1f} {stars}"
            self.tree.insert("", "end", values=(
                movie["id"],
                movie["title"],
                movie["genre"],
                movie["year"],
                rating_display
            ))

    def show_stats(self):
        if not self.movies:
            messagebox.showinfo("Статистика", "Нет фильмов в библиотеке")
            return

        total = len(self.movies)
        avg_rating = sum(m["rating"] for m in self.movies) / total
        best = max(self.movies, key=lambda x: x["rating"])
        worst = min(self.movies, key=lambda x: x["rating"])

        stats = f"""📊 Статистика кинотеки:

🎬 Всего фильмов: {total}
⭐ Средний рейтинг: {avg_rating:.1f}

🏆 Лучший фильм: {best['title']} (рейтинг: {best['rating']})
💩 Худший фильм: {worst['title']} (рейтинг: {worst['rating']})"""

        messagebox.showinfo("Статистика", stats)

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            self.movies = []
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.movies = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.movies = []

    def save_data(self):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, indent=4, ensure_ascii=False)