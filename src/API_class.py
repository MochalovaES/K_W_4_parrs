from abc import ABC, abstractmethod
import requests
import copy


class API(ABC):
    @abstractmethod
    def get_vacancies(self):
        """
        Функция получает список вакансий по API сайта
        :return: список вакансий в json файле
         """
        pass

    @abstractmethod
    def get_parssing(self):
        """
        Функция преобразует информауию о вакансиях в удобный формат для сохранения
        """
        pass

    @abstractmethod
    def add_words(self, words):
        pass

    @abstractmethod
    def add_area(self, name_city):
        pass

    @abstractmethod
    def get_all_areas(self):
        """
        Функция получает все города поиска по API сайта
        :return: список городов
        """
        pass


class HeadHunterAPI(API):
    """
    Класс получения информации из API HeadHunter
    """
    HH_API_URL = 'https://api.hh.ru/vacancies'
    HH_API_URL_AREAS = 'https://api.hh.ru/areas'
    param_zero = {
        'period': 14,
        'per_page': 100
    }

    def __init__(self):
        self.param = copy.deepcopy(self.param_zero)

    def get_vacancies(self):
        response = requests.get(self.HH_API_URL, self.param)
        json_list = response.json()['items']
        return json_list

    def get_parssing(self, json_list):
        vacancy_list = []
        for item in json_list:
            name_vacancy = item['name']
            url_vacancy = 'Нет информации'
            if 'vacancies_url' == item['employer']:
                url_vacancy = item['employer']['vacancies_url']
            salary_vacancy_min = 0
            salary_vacancy_max = 0
            if item['salary'] is not None:
                if item['salary']['from'] is not None:
                    salary_vacancy_min = int(item['salary']['from'])
                if item['salary']['to'] is not None:
                    salary_vacancy_max = int(item['salary']['to'])
            salary_vacancy = 0
            if salary_vacancy_min != 0 and salary_vacancy_max != 0:
                salary_vacancy = round((salary_vacancy_min+salary_vacancy_max)/2)
            elif salary_vacancy_min == 0:
                salary_vacancy = salary_vacancy_max
            elif salary_vacancy_max == 0:
                salary_vacancy = salary_vacancy_min
            info_vacancy = ''
            if item['snippet']['responsibility'] is not None:
                info_vacancy += "Обязанности:" + item['snippet']['responsibility'] + "\n"
            if item['snippet']['requirement'] is not None:
                info_vacancy += "Требования:" + item['snippet']['requirement']
            vacancy = [name_vacancy, url_vacancy, salary_vacancy, info_vacancy]
            vacancy_list.append(vacancy)
        return vacancy_list

    def add_words(self, words):
        self.param['text'] = words

    def add_area(self, name_city):
        self.param['area'] = name_city.keys()

    def get_all_areas(self):
        """
        Функция получает все города поиска в HeadHunter
        :return: список городов
        """
        req = requests.get(HeadHunterAPI.HH_API_URL_AREAS).json()
        areas = {}
        for k in req:
            for i in range(len(k['areas'])):
                if len(k['areas'][i]['areas']) != 0:
                    for j in range(len(k['areas'][i]['areas'])):
                        areas[k['areas'][i]['areas'][j]['id']] = k['areas'][i]['areas'][j]['name']
                else:
                    areas[k['areas'][i]['id']] = k['areas'][i]['name']
        return areas


class SuperJobAPI(API):
    """
    Класс получения информации из API SuperJob
    """
    SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
    SJ_API_URL_AREAS = 'https://api.superjob.ru/2.0/towns/'
    SJ_TOKEN = 'v3.r.137830907.7bd4bf332a04f4e6b69d45dec1b8fdd6779c0150.c06d4a6682fc41b8ddb8dc91b010da8eb63caf4b'
    headers = {'X-Api-App-Id': SJ_TOKEN}
    param_zero = {
        'period': 14,
        'count': 100
    }

    def __init__(self):
        self.param = copy.deepcopy(self.param_zero)

    def get_vacancies(self):
        response = requests.get(self.SJ_API_URL, headers=self.headers, params=self.param)
        json_list = response.json()['objects']
        return json_list

    def get_parssing(self, json_list):
        vacancy_list = []
        for item in json_list:
            name_vacancy = item['profession']
            url_vacancy = 'Нет информации'
            if 'link' == item:
                url_vacancy = item['link']
            salary_vacancy_min = 0
            salary_vacancy_max = 0
            if 'payment_from' in item:
                salary_vacancy_min = 0
                if item['payment_from'] is not None:
                    salary_vacancy_min = int(item['payment_from'])
            if 'payment_to' in item:
                salary_vacancy_min = 0
                if item['payment_to'] is not None:
                    salary_vacancy_max = int(item['payment_to'])
            salary_vacancy = 0
            if salary_vacancy_min != 0 and salary_vacancy_max != 0:
                salary_vacancy = round((salary_vacancy_min + salary_vacancy_max) / 2)
            elif salary_vacancy_min == 0:
                salary_vacancy = salary_vacancy_max
            elif salary_vacancy_max == 0:
                salary_vacancy = salary_vacancy_min
            info_vacancy = item['vacancyRichText']
            vacancy = [name_vacancy, url_vacancy, salary_vacancy, info_vacancy]
            vacancy_list.append(vacancy)
        return vacancy_list

    def add_words(self, words):
        self.param['keyword'] = words

    def add_area(self, name_city):
        self.param['town'] = name_city.values()

    def get_all_areas(self):
        result = {}
        response = requests.get(self.SJ_API_URL_AREAS, headers=self.headers,
                                params={'id_country': 1, 'all': 1}).json()
        for area in response['objects']:
            result[area["id"]] = area["title"]
        return result


