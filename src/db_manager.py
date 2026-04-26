import psycopg2
from typing import List, Tuple, Any
from src.config import Config


class DBManager:
    """Класс для работы с данными в БД."""

    def __init__(self):
        """Конструктор класса DBManager."""
        self.params = Config.get_db_params()

    def get_companies_and_vacancies_count(self) -> List[Tuple[Any, ...]]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()

        cur.execute("""
            SELECT e.employer_name, COUNT(v.vacancy_id) as vacancy_count
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.employer_name
            ORDER BY vacancy_count DESC
        """)

        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_all_vacancies(self) -> List[Tuple[Any, ...]]:
        """Получает список всех вакансий с указанием компании, названия, зарплаты и ссылки."""
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()

        cur.execute("""
            SELECT e.employer_name, v.vacancy_name, v.salary_from, v.salary_to, v.salary_currency, v.vacancy_url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
        """)

        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()

        cur.execute("""
            SELECT AVG((v.salary_from + v.salary_to) / 2)
            FROM vacancies v
            WHERE v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL
        """)

        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return result or 0.0

    def get_vacancies_with_higher_salary(self) -> List[Tuple[Any, ...]]:
        """Получает список всех вакансий, у которых зарплата выше средней."""
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()

        cur.execute("""
            SELECT e.employer_name, v.vacancy_name, v.salary_from, v.salary_to, v.salary_currency, v.vacancy_url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE (v.salary_from + v.salary_to) / 2 > (
                SELECT AVG((salary_from + salary_to) / 2)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            )
        """)

        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[Any, ...]]:
        """Получает список всех вакансий, в названии которых содержится ключевое слово."""
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()

        cur.execute("""
            SELECT e.employer_name, v.vacancy_name, v.salary_from, v.salary_to, v.salary_currency, v.vacancy_url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE v.vacancy_name ILIKE %s
        """, (f"%{keyword}%",))

        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
