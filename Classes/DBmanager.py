class DBManager:

    @staticmethod
    def return_db_name(ex_crDB_cls):
        db_name = ex_crDB_cls.db_name
        return db_name

    @staticmethod
    def get_companies_and_vacancies_count(cur):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        cur.execute("""SELECT employers.employer_name, COUNT(vacancy_id) 
        AS number_of_vacancies FROM vacancies
        FULL JOIN employers USING(employer_id)
        GROUP BY employers.employer_name""")
        rows = cur.fetchall()
        for row in rows:
            print(f"{row[0]} - {row[1]} вакансий.")

    @staticmethod
    def get_all_vacancies(cur):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        cur.execute("""SELECT employers.employer_name, vacancy_name, salary.start_salary, 
                    salary.end_salary, salary.currency, url FROM vacancies
                    FULL JOIN employers USING(employer_id)
                    FULL JOIN salary USING(vacancy_id)""")
        rows = cur.fetchall()
        for row in rows:
            print(
                f"Компания {row[0]}, вакансия {row[1]}, зарплата от: {row[2]}, зарплата до: {row[3]}, валюта: {row[4]}, ссылка на вакансию: {row[5]}")

    @staticmethod
    def get_avg_salary(cur):
        """Получает среднюю зарплату по вакансиям."""
        cur.execute("""SELECT AVG((start_salary+end_salary)/2) AS avg_salary FROM salary 
                    WHERE currency = ' RUR' 
                    AND ((start_salary > 0 AND end_salary > 0) OR start_salary > 0 
                    OR end_salary > 0)""")
        rows = cur.fetchall()
        for row in rows:
            print(f"Средняя зарплата по всем вакансиям {round(row[0], 2)}")

    @staticmethod
    def get_vacancies_with_higher_salary(cur):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
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
            print(
                f"Компания{row[1]}, вакансия{row[2]}, з/п от {row[3]}, з/п до {row[4]}, валюта{row[5]}")

    @staticmethod
    def get_vacancies_with_keyword(cur):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        finder = input("Введите данные для поиска профессии... ")
        cur.execute(f"""SELECT vacancies.vacancy_name, vacancies.city, vacancies.url, 
                    employers.employer_name, salary.start_salary, salary.end_salary, salary.currency 
                    FROM vacancies
                    JOIN salary ON vacancies.vacancy_id = salary.vacancy_id
                    LEFT JOIN employers ON vacancies.employer_id = employers.employer_id
                    WHERE vacancies.vacancy_name ILIKE '%{finder}%'""")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(
                    f"Компания{row[3]}, вакансия{row[0]}, город{row[1]}, сайт вакансии{row[2]}, з/п от {row[4]}, з/п до {row[5]}, валюта{row[6]}")
        else:
            print("Результатов не нашлось.")
