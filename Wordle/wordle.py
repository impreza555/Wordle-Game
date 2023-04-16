import os
import random
import requests
from typing import Callable, Tuple, Dict, List
from colorama import init, Fore, Back, Style

URL = 'https://raw.githubusercontent.com/LussRus/Rus_words/master/UTF8/txt/nouns/summary.txt'
FILE_NAME = 'dictionary.txt'

green: Callable[[str], str] = lambda x: f'{Fore.GREEN}{Back.WHITE}{x.upper()}{Style.RESET_ALL}'
yellow: Callable[[str], str] = lambda x: f'{Fore.YELLOW}{Back.WHITE}{x.upper()}{Style.RESET_ALL}'
black: Callable[[str], str] = lambda x: f'{Fore.BLACK}{Back.WHITE}{x.upper()}{Style.RESET_ALL}'

display = []
for i in range(6):
    temp = ''
    for j in ' _ _ _ _ _ ':
        temp += black(j)
    display.append(temp)


def rules() -> None:
    """
    Функция выводит правила игры.
    :return: None
    """
    rules = f'{"***Игра 5 букв***":^58}\n{"Ваша задача за 6 попыток отгадать слово из пяти букв.":^58}\n' \
            f'{"Игра подсказывает какие буквы в слове вы отгадали.":^58}\n' \
            f'{"Желтым помечается буква, если она присутствует в слове.":^58}\n' \
            f'{"Зелёным - если присутствует и находится на верной позиции.":^58}\n'
    print(rules)


def dictionary_preparation(url: str, file_name: str) -> None:
    """
    Функция для подготовки словаря. Проверяет, есть ли в корневой директории файл словаря.
    Если нет, то загружает данные по указанной ссылке и создает его, отфильтровывая только слова,
    длинна которых == 5 букв.
    :param url: str - ссылка на файл словаря
    :param file_name: str - имя файла словаря
    :return: None
    """
    if not os.path.isfile(file_name):
        response = requests.get(url)
        with open(file_name, 'w', encoding='utf-8') as f_write:
            for line in response.text.split('\n'):
                if len(line) == 5 and line.isalpha():
                    f_write.write((line + '\n').upper())


def random_word(file_name: str) -> Tuple[str, Dict[int, str], Dict[str, int]]:
    """
    Функция выбирает из файла - словаря случайное слово
    и возвращает слово, индексы букв и количество вхождений каждой буквы в слове.
    :param file_name: str - имя файла словаря
    :return: tuple - кортеж: слово, индексы букв и количество вхождений
    """
    with open(file_name, 'r', encoding='utf-8') as f_read:
        lines = f_read.readlines()
    word = random.choice(lines).strip()
    letter_indices = {ch: vl for ch, vl in enumerate(word)}
    number_of_letters = {}
    for lt in word:
        number_of_letters[lt] = number_of_letters.get(lt, 0) + 1
    return word, letter_indices, number_of_letters


def print_display(disp: List[str]) -> None:
    """
    Функция выводит на экран игровое поле.
    :param disp: list - игровое поле
    :return: None
    """
    for el in disp:
        print(f'||{el:>194} ||')


def main(user_word: str, g_data: tuple, disp: list, att_number: int) -> list:
    """
    Главная функция. Реализует логику игры.
    :param user_word: str - пользовательское слово.
    :param g_data: tuple - кортеж: индексы букв и количество вхождений каждой буквы в слове.
    :param disp: list - игровое поле.
    :param att_number: int - номер текущей попытки.
    :return: list - изменённое игровое поле.
    """
    temp_string = black(' ')
    letters_in_right_place = {}
    for idx, val in enumerate(user_word):
        if val not in g_data[0].values():
            temp_string += (black(val) + black(' '))
            continue
        if val in g_data[0].values() and val == g_data[0][idx]:
            letters_in_right_place[val] = letters_in_right_place.get(val, 0) + 1
            temp_string += (green(val) + black(' '))
            continue
        if val in g_data[0].values() and val != g_data[0][idx]:
            if val in letters_in_right_place.keys() and letters_in_right_place[val] < g_data[1][val]:
                temp_string += (yellow(val) + black(' '))
                continue
            else:
                temp_string += (black(val) + black(' '))
                continue
    disp[att_number] = temp_string
    return disp


def main_loop()-> None:
    """
    Функция главного цикла игры.
    :return: None
    """
    dictionary_preparation(URL, FILE_NAME)
    rules()
    init(autoreset=True)
    word, *game_data = random_word(FILE_NAME)
    attempt = 0
    while True:
        if attempt > 5:
            print(f'Игра закончена. Вы проиграли!\nБыло загадано слово: {word}.')
            break
        user_input = input('Введите слово из 5 букв. Выйти - введите "В":\n').upper()
        if user_input == 'В':
            print('Игра закончена. Спасибо за игру!')
            break
        if user_input == word:
            print_display(main(user_input, game_data, display, attempt))
            print('Вы выиграли! Поздравляем!')
            break
        if len(user_input) != 5:
            print('Вы должны ввести слово из 5 букв!')
            continue
        with open('dictionary.txt', 'r+', encoding='utf-8') as file:
            if user_input not in file.read():
                print(
                    f'Такого слова нет в словаре.\n'
                    f'Если уверены, что слово существует,\n'
                    f'вы можете добавить его в словарь'
                )
                choice = input('Добавить в словарь? Д/Н: ').upper()
                if choice == 'Д':
                    file.seek(0, 2)
                    file.write(user_input.upper() + '\n')
                    print('Слово добавлено в словарь!')
                continue
            else:
                print_display(main(user_input, game_data, display, attempt))
                attempt += 1
                continue


if __name__ == '__main__':
    main_loop()
# TODO доработать, логику игры, устранить мелкие недочёты и возможные ошибки в программе.
# TODO попробовать найти в интернете другую БД слов, т.к. данная БД просто ужасна.
# TODO вместо текстового файла использовать СУБД, например SQLite.
# TODO ну и наконец, попробовать прикрутить GUI.
