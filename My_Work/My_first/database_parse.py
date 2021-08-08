# -*- coding: utf-8 -*-
import psycopg2
from psycopg2 import Error
import csv
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# from My_Work.My_first.test_3 import get_tender_number_code, all_links
import json

# try:
#     # TODO создание или Подключение к существующей базе данных
#     connection = psycopg2.connect(user="postgres",
#                                   # пароль, который указали при установке PostgreSQL
#                                   password="Vfrcvfrc1",
#                                   host="127.0.0.1",
#                                   port="5432")
# connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# # Курсор для выполнения операций с базой данных
# cursor = connection.cursor()
# sql_create_database = 'create database database_parse'
# cursor.execute(sql_create_database)
# except (Exception, Error) as error:
#     print("Ошибка при работе с PostgreSQL", error)
# finally:
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Соединение с PostgreSQL закрыто")

#     TODO инфо
try:
    #  Подключение к существующей базе данных
    connection = psycopg2.connect(user="postgres",
                                  #  пароль, который указали при установке PostgreSQL
                                  password="Vfrcvfrc1",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="database_parse")

    #     #  Курсор для выполнения операций с базой данных
    #     cursor = connection.cursor()
    #     #  Распечатать сведения о PostgreSQL
    #     print("Информация о сервере PostgreSQL")
    #     print(connection.get_dsn_parameters(), "\n")
    #     #  Выполнение SQL-запроса
    #     cursor.execute("SELECT version();")
    #     #  Получить результат
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

    # Создайте курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # SQL-запрос для создания новой таблицы
    create_table_query = '''CREATE TABLE lids
                          (НМЦК NUMERIC(15, 2),
                          Сумма_контракта NUMERIC(15, 2),
                          Снижение NUMERIC(15, 2),
                          Сумма_Бг NUMERIC(15, 2),
                          Победитель TEXT,
                          ИНН TEXT,
                          Телефон TEXT,
                          Часовой_пояс TEXT,
                          Email TEXT,
                          Статус_Тендера TEXT,
                          Номер_тендера TEXT,
                          Ссылка TEXT,
                          Дата_контракта_ЕИС DATE,
                          Дата_протокола TIMESTAMP,
                          Дата_тендера DATE); '''

    # Выполнение команды: это создает новую таблицу
    cursor.execute(create_table_query)
    connection.commit()
    print("Таблица успешно создана в PostgreSQL")

    # cursor.execute("DROP TABLE public.lids;")
    # # TODO Получить результат записи
    # record = cursor.fetchall()
    # print("Результат", record)


except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")

    # cursor = connection.cursor()
    # count = 1
    # for item in all_links:
    #     count += 1
    #     cursor.execute("INSERT INTO lids (ID, НМЦК, Сумма_контракта, Снижение, Сумма_Бг, Победитель, ИНН,"
    #                    " Телефон, Часовой_пояс, Email, Статус_Тендера, Номер_тендера, Ссылка, "
    #                    "Дата_контракта_ЕИС, Дата_протокола, Дата_тендера) VALUES (%s, %s, %s, %s, %s, %s, %s, "
    #                    "%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    #                    (count, item['price_tender'], item['price_contract'], item['demping'], item['sum_bg'],
    #                             item['tender_winner'], item['inn'], item['phone'], item['time_zone'], item['email'],
    #                             item['status_contract'], item['tender_number'], item['link_tender'],
    #                             item['date_pre_contract'], item['date_winner_protokol'], item['data_tender']))

# try:
#     # TODO Подключиться к существующей базе данных
#     connection = psycopg2.connect(user="postgres",
#                                   # TODO пароль, который указали при установке PostgreSQL
#                                   password="Vfrcvfrc1",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="postgres_db")
#
#     cursor = connection.cursor()
# TODO  Выполнение SQL-запроса для вставки данных в таблицу
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

# cursor.execute("SELECT PRICE from mobile")
# # TODO Получить результат записи
# record = cursor.fetchall()
# print("Результат", record)

# TODO Получить список таблиц в базе
# cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
# for i in cursor:
#     print(i)

# TODO Выполнение SQL-запроса для обновления таблицы
# update_query = """Update mobile set price = 1500 where id = 1"""
# cursor.execute(update_query)
# connection.commit()
# count = cursor.rowcount
# print(count, "Запись успешно обновлена")
#  TODO Получить результат
# cursor.execute("SELECT * from mobile")
# print("Результат", cursor.fetchall())
#
# TODO Выполнение SQL-запроса для удаления данных
# delete_query = """Delete from mobile where id = 2"""
# cursor.execute(delete_query)
# connection.commit()
# count = cursor.rowcount
# print(count, "Запись успешно удалена")
# TODO Получить результат
# cursor.execute("SELECT * from mobile")
# print("Результат", cursor.fetchall())

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
