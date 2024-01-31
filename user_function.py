from Classes.CreateDB import CreateDB
from Classes.DBmanager import DBManager


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
    manage_db = DBManager()
    while True:
        user_input = input("""Что сделать с созданной БД? 
'1' - получить список всех компаний и количество вакансий у каждой компании, 
'2' - получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию, 
'3' - получить среднюю зарплату по вакансиям, 
'4' - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям, 
'5' - получает список всех вакансий с поиском по ключевому слову, 
'0' - выход.
""")
        if user_input == '1':
            manage_db.get_companies_and_vacancies_count()
            continue
        elif user_input == '2':
            manage_db.get_all_vacancies()
            continue
        elif user_input == '3':
            manage_db.get_avg_salary()
            continue
        elif user_input == '4':
            manage_db.get_vacancies_with_higher_salary()
            continue
        elif user_input == '5':
            manage_db.get_vacancies_with_keyword()
            continue
        elif user_input == '0':
            print("Программа завершена.")
            quit()
        else:
            print("Ведите указанные числа!")
            continue
