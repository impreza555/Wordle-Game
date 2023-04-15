import os
import random
import requests
from typing import Callable, Tuple, Dict, List

URL = 'https://raw.githubusercontent.com/LussRus/Rus_words/master/UTF8/txt/nouns/summary.txt'
FILE_NAME = 'dictionary.txt'

green: Callable[[str], str] = lambda x: f'\033[01;38;05;64;48;05;253m{x.upper()}\033[0m'
yellow: Callable[[str], str] = lambda x: f'\033[01;38;05;214;48;05;253m{x.upper()}\033[0m'
black: Callable[[str], str] = lambda x: f'\033[01;38;05;238;48;05;253m{x.upper()}\033[0m'

display = [black(' _ _ _ _ _ ') for i in range(6)]


def rules() -> None:
	"""
	Функция выводит правила игры.
	:return: None
	"""
	rules = '''
	Игра 5 букв
	Ваша задача за 6 попыток отгадать слово из пяти букв.
	Игра подсказывает какие буквы в слове вы отгадали.
	Желтым помечается буква, если она присутствует в слове.
	Зелёным - если присутствует и находится на верной позиции'''
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
				if len(line) == 5:
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
	letter_indices = {i: v for i, v in enumerate(word)}
	number_of_letters = {}
	for i in word:
		number_of_letters[i] = number_of_letters.get(i, 0) + 1
	return word, letter_indices, number_of_letters


def print_display(disp: List[str]) -> None:
	"""
	Функция выводит на экран игровое поле.
	:param disp: list - игровое поле
	:return: None
	"""
	for i in disp:
		print(f'{i:>50}')


game_data = random_word(FILE_NAME)
attempt = 0
while True:
	if attempt > 5:
		print(f'Игра закончена. Вы проиграли!\nБыло загадано слово: {game_data[0]}.')
		break
	user_input = input('Введите слово из 5 букв. Выйти - введите "В":\n').upper()
	if user_input == 'В':
		print('Игра закончена. Спасибо за игру!')
		break
	if user_input == game_data[0]:
		print('Вы выиграли! Поздравляем!')
		break
	if len(user_input) != 5:
		print('Вы должны ввести слово из 5 букв!')
		continue
	with open('dictionary.txt', 'r+', encoding='utf-8') as file:
		if user_input not in file.read():
			print(
				'Такого слова нет в словаре.\nЕсли уверены, что слово существует,\nвы можете добавить его в словарь')
			choice = input('Добавить в словарь? Д/Н: ').upper()
			if choice == 'Д':
				file.seek(0, 2)  # перемещение курсора в конец файла
				file.write(user_input.upper() + '\n')
				print('Слово добавлено в словарь!')
			continue
		else:
			print("Продолжаем игру!")
			attempt += 1
			continue

# if __name__ == '__main__':
# 	dictionary_preparation(URL, FILE_NAME)
# 	print(random_word(FILE_NAME))
# 	for ch in 'привет':
# 		print(green(ch), end='')
# 		print(yellow(ch), end='')
# 		print(black(ch), end='')
# 	rules()
# 	for i in range(3):
# 		a = input()
# 		print_display(display)
