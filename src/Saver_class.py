import json

from src.Vacancy_class import Vacancy


class SaverJSON:

    def __init__(self):
        self.vacancy = Vacancy
        self.vacancy_list = []

    def add_vacancy(self, vacancy):
        """
        Функция добавления вакансии
        :return:
        """
        self.vacancy_list.append(vacancy)

    def get_save_json(self, vacancy_list):
        """
        Функция сохраняет список вакансий
        """
        with open('vacancy.json', "w", encoding='utf-8') as file:
            json.dump(vacancy_list, file)

    def get_vacancies_by_salary(self):
        """
        Функция сортировки вакансий в списке по средней зарплате
        :return:
        """
        vacancy_sort = sorted(self.vacancy_list, reverse=True, key=lambda x: x.salary_vacancy)
        vacancy_top_10 = []
        for i in range(10):
            vacancy_top_10.append(vacancy_sort[i])
        return vacancy_top_10

    def delete_vacancy(self):
        """
        Функция удаляет вакансии
        """
        if self.vacancy in self.vacancy_list:
            self.vacancy_list.remove(self.vacancy)
        else:
            pass
