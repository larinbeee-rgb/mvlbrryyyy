import unittest
import os
import tempfile
import tkinter as tk
from movie_library import MovieLibrary

class TestMovieLibrary(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        import movie_library
        self.original_data_file = movie_library.DATA_FILE
        movie_library.DATA_FILE = os.path.join(self.temp_dir.name, "test.json")
        self.root = tk.Tk()
        self.app = MovieLibrary(self.root)

    def tearDown(self):
        self.root.destroy()
        self.temp_dir.cleanup()
        import movie_library
        movie_library.DATA_FILE = self.original_data_file

    def test_validate_year_valid(self):
        result = self.app.validate_year("1994")
        self.assertEqual(result, 1994)

    def test_validate_year_too_old(self):
        result = self.app.validate_year("1800")
        self.assertIsNone(result)

    def test_validate_year_future(self):
        result = self.app.validate_year("2100")
        self.assertIsNone(result)

    def test_validate_year_not_number(self):
        result = self.app.validate_year("абв")
        self.assertIsNone(result)

    def test_validate_rating_valid(self):
        result = self.app.validate_rating("7.5")
        self.assertEqual(result, 7.5)

    def test_validate_rating_too_low(self):
        result = self.app.validate_rating("-1")
        self.assertIsNone(result)

    def test_validate_rating_too_high(self):
        result = self.app.validate_rating("11")
        self.assertIsNone(result)

    def test_validate_rating_not_number(self):
        result = self.app.validate_rating("отлично")
        self.assertIsNone(result)

    def test_add_movie_success(self):
        self.app.title_var.set("Форрест Гамп")
        self.app.genre_var.set("Драма")
        self.app.year_var.set("1994")
        self.app.rating_var.set("9.5")
        self.app.add_movie()
        self.assertEqual(len(self.app.movies), 1)
        self.assertEqual(self.app.movies[0]["title"], "Форрест Гамп")

    def test_filter_by_genre(self):
        self.app.movies = [
            {"id": 1, "title": "А", "genre": "Драма", "year": 2000, "rating": 8},
            {"id": 2, "title": "Б", "genre": "Комедия", "year": 2000, "rating": 7}
        ]
        self.app.refresh_table()
        self.app.filter_genre_var.set("Драма")
        self.app.apply_filter()
        items = self.app.tree.get_children()
        self.assertEqual(len(items), 1)

    def test_filter_by_year(self):
        self.app.movies = [
            {"id": 1, "title": "А", "genre": "Драма", "year": 1999, "rating": 8},
            {"id": 2, "title": "Б", "genre": "Драма", "year": 2000, "rating": 7}
        ]
        self.app.refresh_table()
        self.app.filter_year_var.set("2000")
        self.app.apply_filter()
        items = self.app.tree.get_children()
        self.assertEqual(len(items), 1)

    def test_stats_calculation(self):
        self.app.movies = [
            {"id": 1, "title": "Фильм 1", "genre": "А", "year": 2000, "rating": 10},
            {"id": 2, "title": "Фильм 2", "genre": "Б", "year": 2001, "rating": 5}
        ]
        total = len(self.app.movies)
        avg = sum(m["rating"] for m in self.app.movies) / total
        self.assertEqual(total, 2)
        self.assertEqual(avg, 7.5)

if __name__ == "__main__":
    unittest.main()