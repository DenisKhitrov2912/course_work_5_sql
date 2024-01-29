import json

import psycopg2

from config import config

from main import GetApiData


class CreateDB:

    def __init__(self):
        self.script_file = 'create_table.sql'
        self.data = GetApiData.get_api_data
        self.db_name = input('Введите имя базы данных: ')
        self.params = config()
        self.conn = None

    def main(self):

        self.create_database()
        print(f"БД {self.db_name} успешно создана")

        self.params.update({'dbname': self.db_name})
        try:
            with psycopg2.connect(**self.params) as self.conn:
                with self.conn.cursor() as cur:
                    self.execute_sql_script(cur)
                    print(f"В БД {self.db_name} таблицы успешно созданы")

                    #data = self.get_suppliers_data()
                    #self.insert_suppliers_data(cur, data)
                    #print("Данные в suppliers успешно добавлены")
        except(Exception, psycopg2.DatabaseError) as error:
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
        except Exception:
            cur.execute(f"DROP DATABASE {self.db_name}")
            cur.execute(f"CREATE DATABASE {self.db_name}")
        self.conn.close()

    def execute_sql_script(self, cur) -> None:
        """Выполняет скрипт из файла для вставки таблиц в БД."""
        with open(self.script_file, 'r') as file:
            create_db_script = file.read()
        cur.execute(create_db_script)

    def get_suppliers_data(self) -> list[dict]:
        """Извлекает данные из JSON-файла и возвращает список словарей с соответствующей информацией."""
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            return data

    def insert_suppliers_data(self, cur, data: list[dict]) -> None:
        """Добавляет данные из data в таблицы."""
        for dat in data:
            cur.execute("""
            INSERT INTO suppliers (company_name, contact, address, phone, fax, homepage, products)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING supplier_id""",
                        (data["company_name"], data["contact"], data["address"], data["phone"], data["fax"],
                         data["homepage"], data["products"]))

            supplier_id = cur.fetchone()[0]

            for product_one in data['products']:
                cur.execute(
                    """ SELECT product_id FROM products WHERE product_name = %(product)s""", {'product': product_one}
                )

                product_id = cur.fetchone()[0]

                cur.execute(
                    """UPDATE products SET supplier_id = %(suppl)s WHERE product_id= %(prod)s""",
                    {'suppl': supplier_id, 'prod': product_id}
                )
f = CreateDB()
f.main()