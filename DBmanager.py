import psycopg2


class DBManager:

    conn = None

    @classmethod
    def get_companies_and_vacancies_count(cls):
        while True:
            db_name = input("Введите название БД для подключения (без пробелов, используйте '_'): ")
            try:
                with psycopg2.connect(dbname=db_name, host='localhost', user='postgres', password='12345',
                                      port='5432') as cls.conn:
                    with cls.conn.cursor() as cur:
                        cur.execute("""SELECT employers.employer_name, COUNT(vacancy_id) 
                        AS number_of_vacancies FROM vacancies
                        FULL JOIN employers USING(employer_id)
                        GROUP BY employers.employer_name""")
                        rows = cur.fetchall()
                        for row in rows:
                            print(f"{row[0]} - {row[1]} вакансий.")
                        break
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if cls.conn is not None:
                    cls.conn.close()

    @classmethod
    def get_all_vacancies(cls):
        while True:
            db_name = input("Введите название БД для подключения (без пробелов, используйте '_'): ")
            try:
                with psycopg2.connect(dbname=db_name,host='localhost',user='postgres',password= '12345', port= '5432') as cls.conn:
                    with cls.conn.cursor() as cur:
                        cur.execute("""SELECT employers.employer_name, vacancy_name, salary.start_salary, salary.end_salary, salary.currency, url FROM vacancies
                                    FULL JOIN employers USING(employer_id)
                                    FULL JOIN salary USING(vacancy_id)""")
                        rows = cur.fetchall()
                        for row in rows:
                            print(f"Компания {row[0]}, вакансия {row[1]}, зарплата от: {row[2]}, зарплата до: {row[3]}, валюта: {row[4]}, ссылка на вакансию: {row[5]}")
                        break
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if cls.conn is not None:
                    cls.conn.close()
    @classmethod
    def get_avg_salary(cls):
        while True:
            db_name = input("Введите название БД для подключения (без пробелов, используйте '_'): ")
            try:
                with psycopg2.connect(dbname=db_name,host='localhost',user='postgres',password= '12345', port= '5432') as cls.conn:
                    with cls.conn.cursor() as cur:
                        cur.execute("""SELECT AVG((start_salary+end_salary)/2) AS avg_salary FROM salary 
                                    WHERE currency = ' RUR' 
                                    AND ((start_salary > 0 AND end_salary > 0) OR start_salary > 0 OR end_salary > 0)""")
                        rows = cur.fetchall()
                        for row in rows:
                            print(f"Средняя зарплата по всем вакансиям {round(row[0], 2)}")
                        break
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if cls.conn is not None:
                    cls.conn.close()

    @classmethod
    def get_vacancies_with_higher_salary(cls):
        while True:
            db_name = input("Введите название БД для подключения (без пробелов, используйте '_'): ")
            try:
                with psycopg2.connect(dbname=db_name,host='localhost',user='postgres',password= '12345', port= '5432') as cls.conn:
                    with cls.conn.cursor() as cur:
                        cur.execute("""SELECT vacancies.vacancy_id, employers.employer_name, vacancies.vacancy_name, 
                        salary.start_salary, salary.end_salary, salary.currency
                        FROM vacancies
                        JOIN salary ON vacancies.vacancy_id = salary.vacancy_id
                        JOIN employers ON vacancies.employer_id = employers.employer_id
                        WHERE (currency = ' RUR' AND ((salary.start_salary + salary.end_salary) / 2) >
                        (SELECT AVG((start_salary + end_salary) / 2) FROM salary
                        WHERE currency = ' RUR' 
                        AND ((start_salary > 0 AND end_salary > 0) 
                        OR start_salary > 0 OR end_salary > 0)));""")
                        rows = cur.fetchall()
                        for row in rows:
                            print(f"Компания{row[1]}, вакансия{row[2]}, з/п от {row[3]}, з/п до {row[4]}, валюта{row[5]}")
                        break
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if cls.conn is not None:
                    cls.conn.close()

    @classmethod
    def get_vacancies_with_keyword(cls):
        while True:
            db_name = input("Введите название БД для подключения (без пробелов, используйте '_'): ")
            try:
                with psycopg2.connect(dbname=db_name,host='localhost',user='postgres',password= '12345', port= '5432') as cls.conn:
                    with cls.conn.cursor() as cur:
                        finder = input("Введите данные для поиска профессии...")
                        cur.execute(f"""SELECT vacancies.vacancy_name, vacancies.city, vacancies.url, employers.employer_name, salary.start_salary, salary.end_salary, salary.currency 
                        FROM vacancies
                        JOIN salary ON vacancies.vacancy_id = salary.vacancy_id
                        LEFT JOIN employers ON vacancies.employer_id = employers.employer_id
                        WHERE vacancies.vacancy_name ILIKE '%{finder}%'""")
                        rows = cur.fetchall()
                        for row in rows:
                            print(f"Компания{row[3]}, вакансия{row[0]}, город{row[1]}, сайт вакансии{row[2]}, з/п от {row[4]}, з/п до {row[5]}, валюта{row[6]}")
                        break
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if cls.conn is not None:
                    cls.conn.close()


a = DBManager
#a.get_companies_and_vacancies_count()
#a.get_all_vacancies()
#a.get_avg_salary()
#a.get_vacancies_with_higher_salary()
a.get_vacancies_with_keyword()