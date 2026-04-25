import psycopg2
from src.config import Config


class DBCreator:
    """Класс для создания базы данных и таблиц"""

    def __init__(self):
        """Конструктор класса DBCreator"""
        self.db_params = Config.get_db_params()

    def create_database(self) -> None:
        """Создаёт базу данных, если она не существует"""
        params = self.db_params.copy()
        db_name = params.pop('dbname')

        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f"CREATE DATABASE {db_name}")

        cur.close()
        conn.close()

    def create_tables(self) -> None:
        """Создаёт таблицы employers и vacancies"""

        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
            employer_id INTEGER PRIMARY KEY,
            employer_name VARCHAR(255) NOT NULL,
            employer_url VARCHAR(255),
            vacancies_url VARCHAR(255)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id INTEGER PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(employer_id),
            vacancy_name VARCHAR(255) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            salary_currency VARCHAR(10),
            vacancy_url VARCHAR(255)
            )
        """)

        conn.commit()
        cur.close()
        conn.close()

    def run(self) -> None:
        """Запускает создание БД и таблиц"""
        self.create_database()
        self.create_tables()
