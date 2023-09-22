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
    def change_date(self):
        """
        Период за который пользователь хочет просмотреть вакансии
        """
        pass

    @abstractmethod
    def add_words(self):
        pass

    @abstractmethod
    def add_area(self):
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
        'per_page': 100
    }

    def __init__(self):
        self.param = copy.deepcopy(self.param_zero)

    def get_vacancies(self):

        response = requests.get(self.HH_API_URL, self.param)
        return response.json()['items']

    def change_date(self, days):
        self.param['period'] = days

    def add_words(self, words):
        self.param['text'] = words

    def add_area(self, name_city):
        self.params['area'] = name_city

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
                        areas[k['areas'][i]['areas'][j]['name']] = k['areas'][i]['areas'][j]['id']
                else:
                    areas[k['areas'][i]['name']] = k['areas'][i]['id']
        return areas


class SuperJobAPI(API):
    """
    Класс получения информации из API SuperJob
    """
    SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
    SJ_API_URL_AREAS = 'https://api.superjob.ru/2.0/towns/'
    SJ_TOKEN = 'v3.r.137830907.7bd4bf332a04f4e6b69d45dec1b8fdd6779c0150.c06d4a6682fc41b8ddb8dc91b010da8eb63caf4b'
    headers = {'X-Api-App-Id':SJ_TOKEN}
    param_zero = {
        'count': 100
    }

    def __init__(self):
        self.param = copy.deepcopy(self.param_zero)

    def get_vacancies(self):
        response = requests.get(self.SJ_API_URL, headers=self.headers, params=self.param)
        return response.json()['objects']

    def change_date(self, days):
        self.param['period'] = days

    def add_words(self, words):
        self.param['keyword'] = words

    def add_area(self, name_city):
        self.param['town'] = name_city

    def get_all_areas(self):
        result = {}
        response = requests.get(self.SJ_API_URL_AREAS, headers=self.headers,
                                params={'id_country': 1, 'all': 1}).json()
        for area in response['objects']:
            result[area["title"].lower()] = area["id"]
        return result


