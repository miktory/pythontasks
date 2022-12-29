import doctest
import main
from main import *
from unittest import TestCase

def load_tests(loader,tests,ignore):
    tests.addTests(doctest.DocTestSuite(main))
    return tests


class TestReport(TestCase):
    # Проверка на соответствие результатов отчёта и образца из задания
    def test_years_salary(self):
        self.dataset = DataSet('vacancies_test.csv', 'Аналитик')
        self.years_salary_dic = self.dataset.get_info()[0]
        self.assertTrue(all(item in self.years_salary_dic.items() for item in {2007: 38916, 2008: 43646, 2009: 42492, 2010: 43846, 2011: 47451, 2012: 48243, 2013: 51510, 2014: 50658}.items()))

    def test_years_count(self):
        self.dataset = DataSet('vacancies_test.csv', 'Аналитик')
        self.years_count_dic = self.dataset.get_info()[1]
        self.assertTrue(all(item in self.years_count_dic.items() for item in {2007: 2196, 2008: 17549, 2009: 17709, 2010: 29093, 2011: 36700, 2012: 44153, 2013: 59954, 2014: 66837}.items()))


class TestDataSet(TestCase):
    def test_csv_read_yield(self):   # Проверка парсинга на ленивость
        self.dataset = DataSet('vacancies_test.csv', 'Аналитик')
        self.list = []
        self.count = 0
        for vacancy_dictionary in self.dataset.read_csv():
            if self.count == 2:
                break
            self.count += 1
            self.list.append(vacancy_dictionary)
        self.assertTrue(list[0] != list[1])

    def test_add_create_value(self):  # Проверка метода для добавления элемента в словарь
        self.dataset = DataSet('vacancies_test.csv', 'Аналитик')
        self.dictionary = {}
        self.dataset.add(self.dictionary, 'test', 5)
        self.assertTrue(self.dictionary['test'] == 5)

    def test_add_increment_value(self):  # Проверка того же метода на увеличение значения
        self.dataset = DataSet('vacancies_test.csv', 'Аналитик')
        self.dictionary = {}
        self.dataset.add(self.dictionary, 'test', 5)
        self.dataset.add(self.dictionary, 'test', 5)
        self.assertTrue(self.dictionary['test'] == 10)








