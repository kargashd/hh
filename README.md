# HH Parser Project

Проект для сбора и анализа вакансий с сайта hh.ru. Получает данные о компаниях и вакансиях, сохраняет их в базу данных PostgreSQL, предоставляет удобный интерфейс для поиска и фильтрации вакансий.

## Содержание
- [Технологии](#технологии)
- [Начало работы](#начало-работы)
- [Структура проекта](#структура-проекта)
- [Тестирование](#тестирование)
- [База данных](#база-данных)
- [Contributing](#contributing)
- [Команда проекта](#команда-проекта)

## Технологии
- Python 3.12+
- PostgreSQL
- psycopg2
- Requests
- Pytest
- Flake8
- Black
- Isort

## Начало работы

### Требования

- Python 3.12 или выше
- PostgreSQL установленный локально

### Установка зависимостей

#### Клонируйте репозиторий:

git clone https://github.com/kargashd/hh.git
cd hh

#### Создайте и активируйте виртуальное окружение:

python -m venv .venv
.venv\Scripts\activate

macOS/Linux
python3 -m venv .venv
source .venv/bin/activate


#### Установите зависимости:

pip install -r requirements.txt

### Настройка базы данных

#### Скопируйте файл .env.example в .env:

cp .env.example .env

#### Отредактируйте .env с вашими параметрами подключения к PostgreSQL:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=hh_parser
DB_USER=postgres
DB_PASSWORD=your_password

### Использование

Запустите проект:python main.py

Программа автоматически:

- Создаст базу данных и таблицы

- Загрузит данные о 10 компаниях и их вакансиях

- Предоставит меню для работы с данными

### Структура проекта

```bash
hh/
├── data/
│   └── vacancies_sample.json    # Тестовые данные (заглушка API)
├── src/
│   ├── config.py                 # Конфигурация БД
│   ├── db_creator.py             # Создание БД и таблиц
│   ├── api.py                    # Класс для работы с API hh.ru
│   ├── db_manager.py             # Класс DBManager
│   └── main.py                   # Точка входа
├── tests/
│   ├── test_api.py               # Тесты для API
│   ├── test_db_creator.py        # Тесты для DBCreator
│   └── test_db_manager.py        # Тесты для DBManager
├── .env.example                  # Шаблон переменных окружения
├── .flake8                       # Конфигурация линтера
├── .gitignore                    # Игнорируемые Git файлы
├── pyproject.toml                # Конфигурация black, isort, mypy, pytest
├── requirements.txt              # Зависимости проекта
└── README.md                     # Документация проекта
```

## База данных

### Таблицы

**employers**

- employer_id INTEGER PRIMARY KEY — ID компании
- employer_name VARCHAR(255) — Название компании
- employer_url VARCHAR(255) — Ссылка на компанию
- vacancies_url VARCHAR(255) — Ссылка на вакансии

**vacancies**

- vacancy_id INTEGER PRIMARY KEY — ID вакансии
- employer_id INTEGER FOREIGN KEY — ID компании
- vacancy_name VARCHAR(255) — Название вакансии
- salary_from INTEGER — Нижняя граница зарплаты
- salary_to INTEGER — Верхняя граница зарплаты
- salary_currency VARCHAR(10) — Валюта
- vacancy_url VARCHAR(255) — Ссылка на вакансию

### Методы DBManager

- get_companies_and_vacancies_count() — Компании и количество вакансий
- get_all_vacancies() — Все вакансии с компанией, зарплатой, ссылкой
- get_avg_salary() — Средняя зарплата по вакансиям
- get_vacancies_with_higher_salary() — Вакансии с зарплатой выше средней
- get_vacancies_with_keyword(keyword) — Поиск по ключевому слову

## Тестирование
Для тестирования всех модулей используется Pytest.
Чтобы протестрировать проект введите команду "pytest" или "pytest --cov=src" в терминале


## Contributing
Сообщайте об ошибках и предлагайте идеи через раздел Issues на GitHub.

Для отправки доработок создайте pull request из ветки feature в develop.

Код должен соответствовать PEP 8 и проходить проверки flake8, black, isort.

### Зачем вы разработали этот проект?
Проект разработан в рамках прохождения курса "Python-разработчик" от Skypro.

## Команда проекта
Daniil Kargashin — разработчик

Email: danilo98.24fevral@yandex.ru

Ссылка на проект: https://github.com/kargashd/bank_utils
