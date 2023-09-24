from src.API_class import HeadHunterAPI, SuperJobAPI
from src.Vacancy_class import Vacancy
import copy

class UserInput:
    """
    Класс для взаимодействия с пользователем
    """
    api_platform = ''
    user_param = {}

    def __init__(self):
        self.api = None
        self.city = ''
        self.param = copy.deepcopy(self.user_param)

    def __call__(self):
        print('Привет! Давайте подберем вакансии для Вас!')

        while True:
            print('Выберите платформу для поиска:\n'
                  '0- выход\n'
                  '1- HeadHunter\n'
                  '2- SuperJob\n')
            user_platform = input('Введите номер платформы: ')
            if user_platform == '0':
                print('Всего доброго!')
                break
            elif user_platform == '1':
                print('Вы выбрали платформу "HeadHunter"')
                self.api = HeadHunterAPI()
                break
            elif user_platform == '2':
                print('Вы выбрали платформу "SuperJob"')
                self.api = SuperJobAPI()
                break
            else:
                print('Не знаю такой команды! Попробуйте еще раз')

        while True:
            user_input = input('Введите город для поиска: ')
            city = user_input.title()
            city_list = []
            dict_city = self.api.get_all_areas()
            for items in dict_city.values():
                if ' ' in items:
                    items = items.split(' ')[0]
                if city in items:
                    city_list.append(items)
            if len(city_list) == 0:
                print('Нет такого города. Попробуйте еще раз')
            elif len(city_list) > 1:
                print('Выберете номер вашего города')
                number = 0
                for i in city_list:
                    number += 1
                    print(f'{number}- {i}')
                number_user = int(input('Номер города:'))
                self.city = city_list[number_user-1]
                break
            else:
                self.city = city_list[0]
                break
        print('Введите ключевые слова для поиска')
        words_user = input('Меня интересует: ')



