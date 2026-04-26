import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from src.db_creator import DBCreator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestDBCreator:

    @patch("src.db_creator.psycopg2.connect")
    def test_create_database_called(self, mock_connect):
        """Тест: метод create_database вызывает psycopg2.connect."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        creator = DBCreator()
        creator.create_database()

        assert mock_connect.called

    @patch("src.db_creator.psycopg2.connect")
    def test_create_tables_called(self, mock_connect):
        """Тест: метод create_tables выполняет SQL запросы."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        creator = DBCreator()
        creator.create_tables()

        assert mock_cursor.execute.call_count >= 2

    @patch("src.db_creator.psycopg2.connect")
    def test_run_calls_both_methods(self, mock_connect):
        """Тест: метод run вызывает create_database и create_tables."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        creator = DBCreator()

        with patch.object(creator, "create_database") as mock_db:
            with patch.object(creator, "create_tables") as mock_tables:
                creator.run()

                mock_db.assert_called_once()
                mock_tables.assert_called_once()
