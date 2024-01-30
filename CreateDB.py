import psycopg2

from config import config

from GetApiData import GetApiData


class CreateDB:

    script_file = 'create_table.sql'
    data = GetApiData.get_api_data
    while True:
        db_name = input("Введите название БД (без пробелов, используйте '_'): ").lower()
        if " " in db_name or db_name == '':
            print("Введите любое название без пробелов!")
        else:
            break
    params = config()
    conn = None

    @classmethod
    def main(cls):

        cls.create_database()
        print(f"БД {cls.db_name} успешно создана")

        cls.params.update({'dbname': cls.db_name})
        try:
            with psycopg2.connect(**cls.params) as cls.conn:
                with cls.conn.cursor() as cur:
                    cls.execute_sql_script(cur)
                    print(f"В БД {cls.db_name} таблицы успешно созданы")
                    cls.insert_suppliers_data(cur)
                    print("Данныe успешно добавлены")
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if cls.conn is not None:
               cls.conn.close()

    @classmethod
    def create_database(cls) -> None:
        """Создает новую базу данных."""
        cls.conn = psycopg2.connect(dbname='postgres', **cls.params)
        cls.conn.autocommit = True
        cur = cls.conn.cursor()
        try:
            cur.execute(f"CREATE DATABASE {cls.db_name}")
        except Exception:
            cur.execute(f"DROP DATABASE {cls.db_name}")
            cur.execute(f"CREATE DATABASE {cls.db_name}")
        cls.conn.close()

    @classmethod
    def execute_sql_script(cls, cur) -> None:
        """Выполняет скрипт из файла для вставки таблиц в БД."""
        with open(cls.script_file, 'r') as file:
            create_db_script = file.read()
        cur.execute(create_db_script)

    @classmethod
    def insert_suppliers_data(cls, cur) -> None:
        """Добавляет данные из data в таблицы."""
        for dat in cls.data():
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


f = CreateDB()
f.main()
