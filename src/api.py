# ВНИМАНИЕ: Реальный API hh.ru в данный момент недоступен (ошибка 403).
# Для демонстрации работы программы используется чтение данных из JSON-файла.
# Полноценная реализация работы с API была написана, но закомментирована.

import os
import json
from typing import List, Dict, Any


class HHApi:
    """Класс для работы с данными о вакансиях (из JSON-файла)."""

    def __init__(self, file_path: str = "data/vacancies_sample.json"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(base_dir, file_path)

    def _load_data(self) -> List[Dict[str, Any]]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_employers_with_vacancies(self, employer_ids: List[int]) -> List[Dict[str, Any]]:
        all_data = self._load_data()
        result = []
        for employer_id in employer_ids:
            found = False
            for employer in all_data:
                if employer["employer_id"] == employer_id:
                    result.append(employer)
                    found = True
                    break
            if not found:
                result.append({
                    "employer_id": employer_id,
                    "employer_name": f"Компания {employer_id}",
                    "employer_url": "",
                    "vacancies_url": "",
                    "vacancies": []
                })
        return result

# Ниже закомментирован код для работы с реальным API hh.ru,
# который недоступен без авторизации (ошибка 403).
""""
import requests
from typing import List, Dict, Any


class HHApi:
    ""Класс для работы с API hh.ru.""

    BASE_URL = "https://api.hh.ru"

    def __init__(self):
        ""Конструктор класса HHApi.""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Accept": "application/json",
        })

    def get_employer(self, employer_id: int) -> Dict[str, Any]:
        ""Получает информацию о работодателе по ID.""
        url = f"{self.BASE_URL}/employers/{employer_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_vacancies_by_employer(self, employer_id: int, per_page: int = 100) -> List[Dict[str, Any]]:
        ""Получает список вакансий работодателя.""
        url = f"{self.BASE_URL}/vacancies"
        params = {
            "employer_id": employer_id,
            "per_page": per_page,
            "only_with_salary": False
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])

    def get_employers_with_vacancies(self, employer_ids: List[int]) -> List[Dict[str, Any]]:
        ""Получает данные о работодателях и их вакансиях.""
        result = []
        for employer_id in employer_ids:
            employer_data = self.get_employer(employer_id)
            vacancies = self.get_vacancies_by_employer(employer_id)

            employer_info = {
                "employer_id": employer_data.get("id"),
                "employer_name": employer_data.get("name"),
                "employer_url": employer_data.get("alternate_url"),
                "vacancies_url": employer_data.get("vacancies_url"),
                "vacancies": []
            }

            for vacancy in vacancies:
                salary = vacancy.get("salary")
                employer_info["vacancies"].append({
                    "vacancy_id": vacancy.get("id"),
                    "vacancy_name": vacancy.get("name"),
                    "salary_from": salary.get("from") if salary else None,
                    "salary_to": salary.get("to") if salary else None,
                    "salary_currency": salary.get("currency") if salary else None,
                    "vacancy_url": vacancy.get("alternate_url")
                })

            result.append(employer_info)

        return result
"""
