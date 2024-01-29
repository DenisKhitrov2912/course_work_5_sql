import requests


class GetApiData:
    """Класс данных по api HeadHunter"""

    def __init__(self):
        self.api = 'https://api.hh.ru/vacancies'
        self.json_file = 'vacancies_data.json'
        self.employers = ['Yandex', 'ОАО Российские железные дороги', 'Московский метрополитен', 'М.Видео-Эльдорадо. Розница', 'Вкусно — и точка', 'ВкусВилл. Магазины', 'WILDBERRIES', 'ПАО Аэрофлот', 'ПАО «Газпром нефть» Рабочие позиции', 'ЛУКОЙЛ']

    def __repr__(self):
        return f"GetApiData: {self.api, self.employers}"

    def get_api_data(self):
        list_vac = []
        for employer in self.employers:
            response = requests.get(self.api,
                                    params={'text': employer, 'search_field': 'company_name'})
            if response.status_code == 200:
                data = response.json()
                keys = ["items"]
                filtered_data = {k: data[k] for k in keys}
                counter = 0
                limit = 10000
                while True:
                    for v in filtered_data["items"]:
                        if counter < limit:
                            counter += 1
                            if v['salary'] is None:
                                salary = "Зарплата не указана"
                                salary_to = ''
                                salary_currency = ''
                            else:
                                if v['salary']['from'] is None:
                                    salary = ''
                                else:
                                    salary = f"от {v['salary']['from']}"
                                if v['salary']['to'] is None:
                                    salary_to = ''
                                else:
                                    salary_to = f"до {v['salary']['to']}"
                                salary_currency = v['salary']['currency']
                            if v["address"] is None:
                                city_address = "Город не указан"
                            else:
                                city_address = v["address"]["city"]
                            v['employer']['name'] = employer
                            link = f'https://hh.ru/vacancy/{v["id"]}'
                            key = f"{v['id']},  {v['name']},  {salary},  {salary_to},  {salary_currency},  {city_address},  {v['employer']['name']},  {link}"
                            list_vac.append(key)
                    else:
                        break
            else:
                print(f"Доступ к сайту не получен! Код ошибки: {response.status_code}")
        list_vacancies = []
        for vac in list_vac:
            list_vacancies.append(vac.split(", "))
        return list_vacancies


f = GetApiData()
f.get_api_data()
