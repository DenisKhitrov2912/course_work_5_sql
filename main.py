from abc import ABC, abstractmethod
import requests


class GetApiData(ABC):
    """Абстрактный класс на получение данных по api"""

    @abstractmethod
    def get_api_data(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class GetApiDataHeadHunter(GetApiData):
    """Класс данных по api HeadHunter"""
    api = 'https://api.hh.ru/vacancies'
    employers = ['Yandex', 'ОАО Российские железные дороги', 'Московский метрополитен', 'М.Видео-Эльдорадо. Розница', 'Вкусно — и точка', 'ВкусВилл. Магазины', 'WILDBERRIES', 'ПАО Аэрофлот', 'ПАО «Газпром нефть» Рабочие позиции', 'ЛУКОЙЛ']

    @classmethod
    def __repr__(cls):
        return f"{cls.api}"

    @classmethod
    def get_api_data(cls):
        for employer in GetApiDataHeadHunter.employers:
            response = requests.get(cls.api,
                                    params={'text': employer, 'search_field': 'company_name'})
            if response.status_code == 200:
                data = response.json()
                keys = ["items"]
                filtered_data = {k: data[k] for k in keys}
                counter = 0
                limit = 5
                while True:
                    for v in filtered_data["items"]:
                        if counter < limit:
                            counter += 1
                            if v['salary'] is None:
                                salary = "Зарплата не указана"
                                salary_to = ''
                                salary_currency = ''
                                cls.salary = 0
                            else:
                                if v['salary']['from'] is None:
                                    salary = ''
                                    cls.salary = v['salary']['to']
                                else:
                                    salary = f"от {v['salary']['from']}"
                                    cls.salary = v['salary']['to']
                                if v['salary']['to'] is None:
                                    salary_to = ''
                                    cls.salary = v['salary']['from']
                                else:
                                    salary_to = f"до {v['salary']['to']}"
                                    cls.salary = v['salary']['to']
                                salary_currency = v['salary']['currency']
                            if v["address"] is None:
                                city_address = "Город не указан"
                            else:
                                city_address = v["address"]["city"]
                            v['employer']['name'] = employer
                            link = f'https://hh.ru/vacancy/{v["id"]}'
                            key = f"{v['id']},  {v['name']},  {salary},  {salary_to},  {salary_currency},  {city_address},  {v['employer']['name']},  {link}"
                            print(key)
                    else:
                        break
            else:
                print(f"Доступ к сайту не получен! Код ошибки: {response.status_code}")


f = GetApiDataHeadHunter()
f.get_api_data()
