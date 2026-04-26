import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch, MagicMock
from src.api import HHApi


class TestHHApi:

    @patch("src.api.requests.Session.get")
    def test_get_employer_success(self, mock_get):
        """Тест успешного получения информации о работодателе."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 123, "name": "Test Company"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api = HHApi()
        result = api.get_employer(123)

        assert result["id"] == 123
        assert result["name"] == "Test Company"
        mock_get.assert_called_once()

    @patch("src.api.requests.Session.get")
    def test_get_employer_error(self, mock_get):
        """Тест ошибки при получении работодателя."""
        mock_get.side_effect = Exception("API error")

        api = HHApi()

        with pytest.raises(Exception):
            api.get_employer(123)

    @patch("src.api.requests.Session.get")
    def test_get_vacancies_by_employer_success(self, mock_get):
        """Тест успешного получения вакансий работодателя."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [
                {"id": 456, "name": "Python Developer", "salary": None}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api = HHApi()
        result = api.get_vacancies_by_employer(123)

        assert len(result) == 1
        assert result[0]["id"] == 456
        assert result[0]["name"] == "Python Developer"
        mock_get.assert_called_once()
