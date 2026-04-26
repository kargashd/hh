import requests
from typing import List, Dict, Any


class HHApi:
    """Класс для работы с API hh.ru"""

    BASE_URL = "https://api.hh.ru"

    def __init__(self):
        """Конструктор класса HHApi"""
        self.session = requests.Session()

    def get_employer(self, employer_id: int) -> Dict[str, Any]:
        """Получает информацию о работодателе по ID"""
        url = f"{self.BASE_URL}/employers/{employer_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_vacancies_by_employer(self, employer_id: int, per_page: int = 100) -> List[Dict[str, Any]]:
        """Получает список вакансий работодателя"""
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
        """Получает данные о работодателях и их вакансиях."""
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
