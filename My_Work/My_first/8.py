# -*- coding: utf-8 -*-
import collections
import glob
import os
import zipfile
import pandas as pd
from itertools import chain
from collections import Counter
from pprint import pprint
from collections import OrderedDict
from nltk.tokenize import sent_tokenize, word_tokenize
import re
from collections import Counter
from tabulate import tabulate
from prettytable import PrettyTable

# TODO удалить из строки все после определенного символа


x = '4 843 166,00 ₽ (20 %)'
y = x[:x.find('₽')]
print(y)

# file_name = '../../lesson_009/Learning_Scrapy.txt'
# file_name2 = '../../lesson_009/Scrapy.txt'
# # FILE_NAME_WAY = os.path.abspath(file_name)
# # WAY_SORTED = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ap.txt')
# # WAY_SORTED2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ap2.txt')
# list_char = []
# with open(file_name, 'r', encoding='utf8') as file:
#     for line in file:
#         res = line.split()
#         list_char.append(res)
#     e = str(list_char)
#     # list_char2 = []
# list_char3 = []
# w = re.sub(r"[-|;|\d|\t|\n|\f|\s|/|:|#|\\|\[|(|'|)|''|\]|=|\?|_|!|\.]", ",", str(list_char))
#
# res = w.split()
# list_char3.append(''.join(res))
#
# list(list_char3)
# dict_stats = collections.OrderedDict()
# y = [line.title() for line in list_char3]
# list_char4 = str(y).split(',')
# # print(list(list_char4))
#
# for letter in list_char4:
#     if letter in dict_stats:
#         dict_stats[letter] += 1
#     else:
#         dict_stats[letter] = 1
# # pprint(dict_stats)
# print(f'{tabulate(sorted(dict_stats.items(), key=lambda x: x[1], reverse=True), tablefmt="grid", stralign="center")}')
#
# with open(file_name2, 'w', encoding='utf8') as file:
#     for line in dict_stats.items():
#         res = str(line).split()
#         list_char.append(res)
#         e = str(line)
#         file.write(f'{line}''\n')
# # #___________________________________


#  Для красивой записи используйте зарезервированное место для текста.
#  по левому краю зарезервированное 30 символов '|{txt:<30}|'
#  по правому краю зарезервированное 30 символов '|{txt:>30}|'
#  по центру зарезервированное 30 символов '|{txt:^30}|'


# with zipfile.ZipFile('example.zip', ’r') as zf:
# print(zf.namelist())

# file_name = 'voyna-i-mir.zip'
# file_name_way = os.path.abspath(file_name)
# print(file_name_way)
#
# zip_file = zipfile.ZipFile(os.path.abspath(file_name), 'r')
# print(zip_file)
#
# zip_file = zipfile.ZipFile(file_name), 'r'
# print(zip_file)
#
#
# file_name_way = os.path.abspath(file_name)
# z_file = zipfile.ZipFile(file_name_way)
# files_info = z_file.infolist()
# print(files_info)
#
# with zipfile.ZipFile(file_name_way, 'r') as zf:
#     print(zf.namelist())

#
# zip_file.printdir() # нет содержимого в архиве
# print(zip_file.namelist()) # нет содержимого в архиве
# print(zipfile.is_zipfile(file_name))  # видит что это  zip

#
# file_name = 'voyna-i-mir.zip'
# file_name_way = os.path.abspath(file_name)
#
# # x = os.path.filename(file_name_way) test
# # print(x)
#
# #
# zip_file = zipfile.ZipFile(os.path.expanduser(file_name_way), 'r')
# # zip_file.printdir()
# print(zip_file.filename)
# # for file in zip_file.filename:
# zip_file.extract(zip_file.filename)
#
# print(zip_file.getinfo('voyna-i-mir.zip'))
# print(zip_file.getinfo(file_name_way))

# dict_stats = {}
# # os.path.normpath(filename)
# with open(filename, 'r', encoding='cp1251') as file:
#     for line in file:
#         for letter in line:
#             if letter.isalpha():
#                 if letter in dict_stats:
#                     dict_stats[letter] += uu
#                 else:
#                     dict_stats[letter] = uu
# print(dict_stats)


# zip_file = zipfile.ZipFile(file_name_way, 'r')
# print(zip_file.filename)
# _____# TODO -___________________________
# func = lambda x: round(x, uu)
# turnout = [23.56, 45.78, 34.92, 57.34, 56.55, 67.23]
# turnout_r = list(map(func, turnout))
# print(turnout_r)
# TODO - ______________________
# modify_list = [23.56, 45.78, 34.92, 57.34, 56.55, 67.23]
# modify = lambda x: x + uu
# modify_iter = list(map(modify, modify_list))
# # _______________________________________
# # iter=[i + uu for i in modify_list]
# # print(iter)
# _______________________________________________

# TODO - сортиовка словаря и вывод обычно
# for k, v in sorted(self.dict_stats.items(), key=itemgetter(uu), reverse=False):
#     self.v = str(v)

#     print(k + " - " + self.v)

# # TODO  архив 'icons.zip' работает
# file_name2 = 'icons.zip'
# file_name_way2 = os.path.abspath(file_name2)
# zip_file2 = zipfile.ZipFile(os.path.abspath(file_name2), 'r')
# print(zip_file2.filename)# TODO путь до архива
# print(zip_file2.infolist())# TODO  видит
# print(zip_file2.namelist()) # TODO видит
# print(zip_file2.filelist) # TODO  видит
# zip_file2.extractall() # TODO распаковывает


# print(os.path.isfile(file_name_way))
# print(os.path.dirname(file_name_way))
# print(os.path.expandvars(file_name_way))
# print(os.path.expanduser(file_name_way))
# print(os.path.isabs(file_name_way)) # проверка аболютного пути
# print(os.path.split(file_name_way)) # отделяет файл от пути
# print(os.getcwd()) # текущая директория
# print(os.path.splitdrive(file_name_way))
# print(os.path.splitext(file_name_way)) # отделяет от пути расширение файла либо последний элемент
# print(zipfile.is_zipfile(file_name_way))
#
# zip_file = zipfile.ZipFile(file_name_way, 'r')
# print(zip_file.filename)
# zip_file.printdir()


# TODO второй код (нашел метод get(letter, 0)):
# dict_stats = {}
# os.path.normpath(filename)
# with open(filename, 'r', encoding='cp1251') as file:
#     for line in file:
#         for letter in line:
#             if letter.isalpha():
#                 dict_stats[letter] = dict_stats.get(letter, 0) + uu
# pprint(dict_stats)


# _______________________________________
# alpha = 'а'
# test_list = []
# for i in range(uu, 33):
#     test_list.append(alpha.upper())
#     test_list.append(alpha)
#     alpha = chr(ord(alpha) + uu)
# # print(test_list)
#
# test_list2 = test_list*50
# _______________________________________
