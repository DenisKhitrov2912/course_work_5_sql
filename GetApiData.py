import requests


class GetApiData:
    """Класс данных по api HeadHunter"""

    api = 'https://api.hh.ru/vacancies'
    employers = ['Yandex', 'ОАО Российские железные дороги', 'Московский метрополитен', 'М.Видео-Эльдорадо. Розница', 'Вкусно — и точка', 'ВкусВилл. Магазины', 'WILDBERRIES', 'ПАО Аэрофлот', 'ПАО «Газпром нефть» Рабочие позиции', 'ЛУКОЙЛ', 'Skyeng']

    @classmethod
    def __repr__(cls):
        return f"GetApiData: {cls.api, cls.employers}"

    @classmethod
    def get_api_data(cls) -> list[list]:
        list_vac = []
        for employer in cls.employers:
            response = requests.get(cls.api,
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
                                salary = "0"
                                salary_to = '0'
                                salary_currency = 'н/д'
                            else:
                                if v['salary']['from'] is None:
                                    salary = '0'
                                else:
                                    salary = f"{v['salary']['from']}"
                                if v['salary']['to'] is None:
                                    salary_to = '0'
                                else:
                                    salary_to = f"{v['salary']['to']}"
                                salary_currency = v['salary']['currency']
                            if v["address"] is None:
                                city_address = "н/д"
                            elif v["address"]["city"] is None:
                                city_address = "н/д"
                            else:
                                city_address = v["address"]["city"]
                            v['employer']['name'] = employer
                            link = f'https://hh.ru/vacancy/{v["id"]}'
                            key = f"{v['id']}|  {v['name']}|  {salary}|  {salary_to}|  {salary_currency}|  {city_address}|  {employer}|  {link}"
                            list_vac.append(key)
                    else:
                        break
            else:
                print(f"Доступ к сайту не получен! Код ошибки: {response.status_code}")
        list_vacancies = []
        for vac in list_vac:
            list_vacancies.append(vac.split("| "))
        return list_vacancies


f = GetApiData()
f.get_api_data()
