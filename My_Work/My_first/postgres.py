# -*- coding: utf-8 -*-
import re
import string
from pprint import pprint

import psycopg2
from psycopg2 import Error
import csv
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# try:
#     # TODO создание или Подключение к существующей базе данных
#     connection = psycopg2.connect(user="postgres",
#                                   # пароль, который указали при установке PostgreSQL
#                                   password="Vfrcvfrc1",
#                                   host="127.0.0.1",
#                                   port="5432")
#     connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     # Курсор для выполнения операций с базой данных
#     cursor = connection.cursor()
#     sql_create_database = 'create database postgres_db_test'
#     cursor.execute(sql_create_database)
# except (Exception, Error) as error:
#     print("Ошибка при работе с PostgreSQL", error)
# finally:
#     if connection:
#         cursor.close()
    #         connection.close()
    #         print("Соединение с PostgreSQL закрыто")

    #     TODO инфо
    # try:
    # #  Подключение к существующей базе данных
    #     connection = psycopg2.connect(user="postgres",
    #                                   #  пароль, который указали при установке PostgreSQL
    #                                   password="Vfrcvfrc1",
    #                                   host="127.0.0.1",
    #                                   port="5432",
    #                                   database="postgres_db")
    #
    #     # TODO Курсор для выполнения операций с базой данных
    #     cursor = connection.cursor()
    #     # TODO Распечатать сведения о PostgreSQL
    #     print("Информация о сервере PostgreSQL")
    #     print(connection.get_dsn_parameters(), "\n")
    #     # TODO Выполнение SQL-запроса
    #     cursor.execute("SELECT version();")
    #     # TODO Получить результат
    #     record = cursor.fetchone()
    #     print("Вы подключены к - ", record, "\n")
    #
    # except (Exception, Error) as error:
    #     print("Ошибка при работе с PostgreSQL", error)
    # finally:
    #     if connection:
    #         cursor.close()
    #         connection.close()
    #         print("Соединение с PostgreSQL закрыто")

    # TODO создание новой таблицы
    # try:
    #     # Подключиться к существующей базе данных
#     connection = psycopg2.connect(user="postgres",
#                                   # пароль, который указали при установке PostgreSQL
#                                   password="Vfrcvfrc1",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="postgres_db_test")
#
#     # Создайте курсор для выполнения операций с базой данных
# cursor = connection.cursor()
# SQL-запрос для создания новой таблицы
#     create_table_query = '''CREATE TABLE mobile_3
#                           (ID INT PRIMARY KEY     NOT NULL,
#                           НМЦК       TEXT,
#                           ТЕНДЕРА        TEXT,
#                           ИНН TEXT); '''
#     # Выполнение команды: это создает новую таблицу
#     cursor.execute(create_table_query)
#     connection.commit()
#     print("Таблица успешно создана в PostgreSQL")
# #
# except (Exception, Error) as error:
#     print("Ошибка при работе с PostgreSQL", error)
# finally:
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Соединение с PostgreSQL закрыто")

#

# try:
#     # TODO Подключиться к существующей базе данных
#     connection = psycopg2.connect(user="postgres",
#                                   # TODO пароль, который указали при установке PostgreSQL
#                                   password="Vfrcvfrc1",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="general_lids")
#
#     cursor = connection.cursor()
# # TODO  Вставка отдельных данных в таблицу
# path_normalized = os.path.abspath('file_base.csv')
# with open(path_normalized, 'r', newline='', encoding='utf-8') as file:
#     reader = csv.DictReader(file, delimiter=';')
#     count = 1
#     for line in reader:
#         x=line['Номер тендера'], y = line['ИНН']
#         count += 1
#         cursor.execute("INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s, %s, %s)", (count, x,
#                                                                                          y))
# insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (2, 'Iphone122', 11200)"""
    # cursor.execute(insert_query)
# connection.commit()
# print("1 запись успешно вставлена")

# cursor.execute("SELECT * from lids")
# # TODO Получить результат записи
# record = cursor.fetchall()
# print("Результат", record)
# TODO Получить результат простого запроса
# print("Результат", cursor.fetchall())
# print(connection.get_dsn_parameters(), "\n")
# TODO записать в файл результат выборки с заголовками
# sql = "COPY(SELECT inn_company FROM no_validate_lids) TO STDOUT WITH (FORMAT CSV, HEADER, DELIMITER ';')"
# with open("table.csv", "w") as file:
#     cursor.copy_expert(sql, file)
# TODO Получить список таблиц в базе
# cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
# for i in cursor:
#     print(i)
#

# TODO Общее количество строк в таблице:
# SELECT count(*) FROM table;

# TODO Выполнение SQL-запроса для обновления таблицы
# update_query = """Update mobile set price = 1500 where id = 1"""
# cursor.execute(update_query)
# connection.commit()
# count = cursor.rowcount
# print(count, "Запись успешно обновлена")
#  TODO Получить результат
# cursor.execute("SELECT adress_company from no_validate_lids where")
# print("Результат", cursor.fetchall())
# #
# TODO Выполнение SQL-запроса для удаления записи
# delete_query = """Delete from mobile where id = 2"""
# cursor.execute(delete_query)
# connection.commit()
# count = cursor.rowcount
# print(count, "Запись успешно удалена")
# TODO обновить запись
# count = 0
# x = "'347909 ОБЛ РОСТОВСКАЯ61 Г ТАГАНРОГ УЛ СОЦИАЛИСТИЧЕСКАЯ'"
# update_query = f"""UPDATE no_validate_lids SET adress_company = {x}  WHERE id = 5"""
#
# cursor.execute(update_query)
# connection.commit()
# count = cursor.rowcount
# print(count, "Запись успешно обновлена")

# TODO в столбик вывод
# cursor.execute("SELECT adress_company from no_validate_lids")
# for i in cursor:
# print(i)
# count += 1
# print("Результат")
# print(f'{count}')
# print()


# except (Exception, Error) as error:
#     print("Ошибка при работе с PostgreSQL", error)
# finally:
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Соединение с PostgreSQL закрыто")


#
# try:
#     # TODO Подключиться к существующей базе данных
#     connection = psycopg2.connect(user="postgres",
#                                   # TODO пароль, который указали при установке PostgreSQL
#                                   password="Vfrcvfrc1",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="postgres_db_2")
#
#     path_normalized = os.path.abspath('file_base.csv')
#     cursor = connection.cursor()
#     with open(path_normalized, 'r', newline='', encoding='utf-8') as file:
#         reader = csv.DictReader(file, delimiter=';')
#         for line in reader:
#
#             # TODO  Выполнение SQL-запроса для вставки данных в таблицу
#
#             cursor.execute("INSERT INTO mobileee (НМЦК, Номер тендера, ИНН) VALUES (%s, %s, %s)", (line['НМЦК'], line['Номер тендера'],
#                                                                                          line['ИНН']))
#             # insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (2, 'Iphone122', 11200)"""
#             # cursor.execute(insert_query)
#             # connection.commit()
#             # print("1 запись успешно вставлена")
#
#             cursor.execute("SELECT PRICE from mobileee")
#             # TODO Получить результат записи
#             # record = cursor.fetchall()
#             # print("Результат", record)
#             # TODO Получить результат простого запроса
#             print("Результат", cursor.fetchall())
#             cursor.execute("SELECT PRICE from mobileee")
#             for i in cursor:
#                 print(i)
# except (Exception, Error) as error:
#     print("Ошибка при работе с PostgreSQL", error)
# finally:
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Соединение с PostgreSQL закрыто")


# TODO Выполнить команду SQL ----------------------------------------------------cursor.execute(),
#  Выполнить команду SQL для списка параметров ----------------------------------cursor.executemany(),
#  Выполнить несколько операторов SQL -------------------------------------------cursor.executescript(),
#  Получить одну строку с результатом запроса -----------------------------------cursor.fetchone(),
#  Получить список из нескольких строк с результатом запроса --------------------cursor.fetchmany(),
#  Получить список всех строк с результатом запроса -----------------------------cursor.fetchall(),
#  Получить ID последней измененной строки --------------------------------------cursor.lastrowid,
#  Получить имена столбцов последнего запроса -----------------------------------cursor.description,
#  Получить количество выбранных строк ------------------------------------------cursor.rowcount,
#  Закрыть курсор ---------------------------------------------------------------cursor.close(),
#  Получить/установить количество строк для метода ------------------------------cursor.fetchmany() cursor.arraysize,
#  Получить объект соединения с базой -------------------------------------------cursor.connection,

