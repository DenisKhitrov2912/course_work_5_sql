import os
import psycopg2

from Classes.GetApiData import GetApiData
from other_files.config import config


class CreateDB:
    def __init__(self):
        self.script_file = os.path.join('other_files', 'create_table.sql')
        self.data = GetApiData.get_api_data
        while True:
            self.db_name = input("Введите название БД (без пробелов, используйте '_'): ").lower()
            if " " in self.db_name or self.db_name == '':
                print("Введите любое название без пробелов!")
            else:
                break
        self.params = config()
        self.conn = None

    def __repr__(self):
        return f'CreateDB: {self.db_name}, {self.params}'

    def main_func(self):
        """Главная функция работы в классе."""
        self.create_database()
        print(f"БД {self.db_name} успешно создана")
        self.params.update({'dbname': self.db_name})
        try:
            with psycopg2.connect(**self.params) as self.conn:
                with self.conn.cursor() as cur:
                    self.execute_sql_script(cur)
                    print(f"В БД {self.db_name} таблицы успешно созданы")
                    self.insert_suppliers_data(cur)
                    print("Данныe успешно добавлены")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def create_database(self) -> None:
        """Создает новую базу данных."""
        self.conn = psycopg2.connect(dbname='postgres', **self.params)
        self.conn.autocommit = True
        cur = self.conn.cursor()
        try:
            cur.execute(f"CREATE DATABASE {self.db_name}")
        except (Exception, psycopg2.DatabaseError):
            cur.execute(f"DROP DATABASE {self.db_name}")
            cur.execute(f"CREATE DATABASE {self.db_name}")
        self.conn.close()

    def execute_sql_script(self, cur) -> None:
        """Выполняет скрипт из файла для вставки таблиц в БД."""
        with open(self.script_file, 'r') as file:
            create_db_script = file.read()
        cur.execute(create_db_script)

    def insert_suppliers_data(self, cur) -> None:
        """Добавляет данные из data в таблицы."""
        for dat in self.data():
            cur.execute("""
            INSERT INTO employers (employer_name) 
            SELECT %s
            WHERE NOT EXISTS (
                SELECT 1 
                FROM employers 
                WHERE employer_name = %s
            )""", (dat[6], dat[6]))

            cur.execute("""
            SELECT employer_id
            FROM employers
            ORDER BY employer_id DESC
            LIMIT 1""")
            employer_id = cur.fetchone()[0]

            cur.execute("""
            INSERT INTO vacancies (vacancy_number, vacancy_name, city, url, employer_id)
            VALUES (%s, %s, %s, %s, %s)""", (dat[0], dat[1], dat[5], dat[7], employer_id))

            cur.execute("""
            SELECT vacancy_id
            FROM vacancies
            ORDER BY vacancy_id DESC
            LIMIT 1""")
            vacancy_id = cur.fetchone()[0]

            cur.execute("""
            INSERT INTO salary (vacancy_id, start_salary, end_salary, currency, vacancy_url)
            VALUES (%s, %s, %s, %s, %s)""", (vacancy_id, dat[2], dat[3], dat[4], dat[7]))
