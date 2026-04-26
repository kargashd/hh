import psycopg2
from src.db_creator import DBCreator
from src.api import HHApi
from src.db_manager import DBManager


def save_employers_and_vacancies(employer_ids):
    """Получает данные о работодателях и вакансиях и сохраняет в БД."""
    api = HHApi()
    employers_data = api.get_employers_with_vacancies(employer_ids)

    db = DBManager()
    conn = psycopg2.connect(**db.params)
    cur = conn.cursor()

    for employer in employers_data:
        cur.execute("""
            INSERT INTO employers (employer_id, employer_name, employer_url, vacancies_url)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (employer_id) DO NOTHING
        """, (
            employer["employer_id"],
            employer["employer_name"],
            employer["employer_url"],
            employer["vacancies_url"]
        ))

        for vacancy in employer["vacancies"]:
            cur.execute("""
                INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, salary_from, salary_to, salary_currency, vacancy_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (vacancy_id) DO NOTHING
            """, (
                vacancy["vacancy_id"],
                employer["employer_id"],
                vacancy["vacancy_name"],
                vacancy["salary_from"],
                vacancy["salary_to"],
                vacancy["salary_currency"],
                vacancy["vacancy_url"]
            ))

    conn.commit()
    cur.close()
    conn.close()
    print("Данные успешно сохранены в базу данных.")


def user_interaction():
    """Функция взаимодействия с пользователем."""
    print("\n" + "=" * 50)
    print("Программа для работы с вакансиями и компаниями")
    print("=" * 50 + "\n")

    creator = DBCreator()
    creator.run()
    print("База данных и таблицы созданы успешно.\n")

    employer_ids = [
        80,     # Яндекс
        1740,   # Google
        2180,   # Ozon
        3529,   # Сбербанк
        3776,   # МТС
        39305,  # VK
        78638,  # Тинькофф
        87021,  # ВК
        90687,  # Авито
        105119  # Wildberries
    ]

    save_employers_and_vacancies(employer_ids)

    db = DBManager()

    while True:
        print("\n" + "-" * 30)
        print("Выберите действие:")
        print("1. Список компаний и количество вакансий")
        print("2. Список всех вакансий")
        print("3. Средняя зарплата по вакансиям")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("\nВаш выбор: ")

        if choice == "1":
            result = db.get_companies_and_vacancies_count()
            print("\nКомпании и количество вакансий:")
            for row in result:
                print(f"  {row[0]}: {row[1]} вакансий")

        elif choice == "2":
            result = db.get_all_vacancies()
            print("\nСписок всех вакансий:")
            for row in result:
                print(f"  {row[0]} - {row[1]}")

        elif choice == "3":
            result = db.get_avg_salary()
            print(f"\nСредняя зарплата по вакансиям: {result:.2f} руб.")

        elif choice == "4":
            result = db.get_vacancies_with_higher_salary()
            print("\nВакансии с зарплатой выше средней:")
            for row in result:
                print(f"  {row[0]} - {row[1]}")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ")
            result = db.get_vacancies_with_keyword(keyword)
            print(f"\nВакансии, содержащие '{keyword}':")
            for row in result:
                print(f"  {row[0]} - {row[1]}")

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
