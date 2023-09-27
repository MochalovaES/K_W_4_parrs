from src.API_class import HeadHunterAPI, SuperJobAPI
from src.Saver_class import SaverJSON
from src.Vacancy_class import Vacancy


def user_interaction():
    api = ''
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
            api = HeadHunterAPI()
            break
        elif user_platform == '2':
            print('Вы выбрали платформу "SuperJob"')
            api = SuperJobAPI()
            break
        else:
            print('Не знаю такой команды! Попробуйте еще раз')

    while True:
        user_input = input('Введите город для поиска: ')
        city = user_input.title()
        city_list = []
        dict_city = api.get_all_areas()
        area = []
        for key, items in dict_city.items():
            if ' ' in items:
                items = items.split(' ')[0]
            if city in items:
                city_list.append(items)
                area.append({key: items})
        if len(area) == 0:
            print('Нет такого города. Попробуйте еще раз')
        elif len(area) > 1:
            print('Выберете номер вашего города')
            number = 0
            for i in range(len(area)):
                number += 1
                print(f"{number}- {list(area[i].values())[0]}")
            number_user = int(input('Номер города:'))
            name_city = area[number_user-1]
            api.add_area(name_city)
            break
        else:
            name_city = area[0]
            api.add_area(name_city)
            break

    print('Введите ключевые слова для поиска через запятую')
    words_user = input('Меня интересует: ')
    words = words_user.split(',')
    api.add_words(words)
    json_list = api.get_parssing(api.get_vacancies())

    sj = SaverJSON()
    for i in json_list:
        vacancy = Vacancy(i[0], i[1], i[2], i[3])
        sj.add_vacancy(vacancy)

    user_vacancy = sj.get_vacancies_by_salary()
    print("Ваши вакансии:")
    for i in user_vacancy:
        print(i)
