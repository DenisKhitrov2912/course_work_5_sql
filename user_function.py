from Classes.CreateDB import CreateDB
from Classes.DBmanager import DBManager
import psycopg2


def user_func():
    """Функция взаимодействия с пользователем"""
    print("Поиск вакансий по заданным 11-ти компаниям, создание БД.")
    while True:
        user_input = input("Нажмите '1' для создания БД и '0' для выхода. ")
        if user_input == '1':
            db_new = CreateDB()
            db_new.main_func()
            break
        elif user_input == '0':
            print("Программа завершена.")
            quit()
        else:
            print("Введите '1' или '0'!")
            continue
    while True:
        user_input = input("""Что сделать с созданной БД? 
'1' - получить список всех компаний и количество вакансий у каждой компании, 
'2' - получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию, 
'3' - получить среднюю зарплату по вакансиям, 
'4' - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям, 
'5' - получает список всех вакансий с поиском по ключевому слову, 
'0' - выход.
""")
        try:
            with psycopg2.connect(dbname=DBManager.return_db_name(db_new), host='localhost', user='postgres', password='12345',
                                  port='5432') as conn:
                with conn.cursor() as cur:
                    if user_input == '1':
                        DBManager.get_companies_and_vacancies_count(cur)
                        continue
                    elif user_input == '2':
                        DBManager.get_all_vacancies(cur)
                        continue
                    elif user_input == '3':
                        DBManager.get_avg_salary(cur)
                        continue
                    elif user_input == '4':
                        DBManager.get_vacancies_with_higher_salary(cur)
                        continue
                    elif user_input == '5':
                        DBManager.get_vacancies_with_keyword(cur)
                        continue
                    elif user_input == '0':
                        print("Программа завершена.")
                        break
                    else:
                        print("Ведите указанные числа!")
                        continue
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
