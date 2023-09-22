from abc import ABC, abstractmethod
import requests
import copy


class API(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def change_date(self):
        pass

    @abstractmethod
    def add_words(self):
        pass

    @abstractmethod
    def add_area(self):
        pass

    @abstractmethod
    def load_all_areas(self):
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

    def change_date(self):
        pass

    def add_words(self):
        pass

    def add_area(self):
        pass

    def load_all_areas(self):
        pass


class SuperJobAPI(API):
    """
    Класс получения информации из API SuperJob
    """

    SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
    SJ_API_URL_AREAS = 'https://api.superjob.ru/2.0/towns/'
    SJ_TOKEN = 'v3.r.137830907.7bd4bf332a04f4e6b69d45dec1b8fdd6779c0150.c06d4a6682fc41b8ddb8dc91b010da8eb63caf4b'
    param_zero = {
        'count': 100
    }

    def __init__(self):
        self.param = copy.deepcopy(self.param_zero)

    def get_vacancies(self):
        headers = {
            'X-Api-App-Id': self.SJ_TOKEN
        }
        response = requests.get(self.SJ_API_URL, headers=headers, params=self.param)
        return response.json()['objects']

    def change_date(self):
        pass

    def add_words(self):
        pass

    def add_area(self):
        pass

    def load_all_areas(self):
        pass