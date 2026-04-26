import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from src.db_manager import DBManager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestDBManager:

    @patch("src.db_manager.psycopg2.connect")
    def test_get_companies_and_vacancies_count(self, mock_connect):
        """Тест получения количества вакансий по компаниям."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("Яндекс", 15), ("Google", 23)]
        mock_connect.return_value = mock_conn

        db = DBManager()
        result = db.get_companies_and_vacancies_count()

        assert result == [("Яндекс", 15), ("Google", 23)]
        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("src.db_manager.psycopg2.connect")
    def test_get_all_vacancies(self, mock_connect):
        """Тест получения всех вакансий."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ("Яндекс", "Python dev", 100000, 150000, "RUR", "https://hh.ru/1"),
            ("Google", "Java dev", 120000, 180000, "RUR", "https://hh.ru/2")
        ]
        mock_connect.return_value = mock_conn

        db = DBManager()
        result = db.get_all_vacancies()

        assert len(result) == 2
        assert result[0][0] == "Яндекс"
        assert result[0][1] == "Python dev"
        mock_cursor.execute.assert_called_once()

    @patch("src.db_manager.psycopg2.connect")
    def test_get_avg_salary(self, mock_connect):
        """Тест получения средней зарплаты."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (125000.0,)
        mock_connect.return_value = mock_conn

        db = DBManager()
        result = db.get_avg_salary()

        assert result == 125000.0
        mock_cursor.execute.assert_called_once()

    @patch("src.db_manager.psycopg2.connect")
    def test_get_avg_salary_none(self, mock_connect):
        """Тест получения средней зарплаты при отсутствии данных."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (None,)
        mock_connect.return_value = mock_conn

        db = DBManager()
        result = db.get_avg_salary()

        assert result == 0.0

    @patch("src.db_manager.psycopg2.connect")
    def test_get_vacancies_with_higher_salary(self, mock_connect):
        """Тест получения вакансий с зарплатой выше средней."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ("Яндекс", "Senior Python dev", 200000, 250000, "RUR", "https://hh.ru/3")
        ]
        mock_connect.return_value = mock_conn

        db = DBManager()
        result = db.get_vacancies_with_higher_salary()

        assert len(result) == 1
        assert result[0][0] == "Яндекс"
        assert result[0][1] == "Senior Python dev"
