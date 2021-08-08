# -*- coding: utf-8 -*-
import psycopg2
from psycopg2 import Error
from termcolor import cprint
import csv
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json

# try:
#  # TODO создание или Подключение к существующей базе данных
#  #
#     connection = psycopg2.connect(user="postgres",
#                                   # пароль, который указали при установке PostgreSQL
#                                   password="Vfrcvfrc1",
#                                   host="127.0.0.1",
#                                   port="5432")
#     connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     # Курсор для выполнения операций с базой данных
#     cursor = connection.cursor()
#     sql_create_database = 'create database general_lids'
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
#      # Подключение к существующей базе данных
#     connection = psycopg2.connect(user="postgres",
#                                   #  пароль, который указали при установке PostgreSQL
#                                   password="Vfrcvfrc1",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="general_lids")

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
#         cprint("Соединение с PostgreSQL закрыто", color='green')

# TODO создание новой таблицы
try:
    # Подключиться к существующей базе данных
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="Vfrcvfrc1",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="general_lids")

    # Создайте курсор для выполнения операций с базой данных
    cursor = connection.cursor()

    # record = cursor.fetchall()
    # print("Результат", record)

    # SQL-запрос для создания новой таблицы
    create_table_query = '''CREATE TABLE no_validate_lids
                            (id SERIAL PRIMARY KEY,
                            name_company TEXT,
                            inn_company TEXT,
                            mail_company TEXT,
                            tel_company TEXT,
                            kpp_company TEXT,
                            ogrn_company TEXT,
                            registration_date_start date,
                            registration_date_end date,
                            adress_company TEXT,
                            adress_index_company INT,
                            boss_company TEXT,
                            date_record date);'''

    # Выполнение команды: это создает новую таблицу
    cursor.execute(create_table_query)
    connection.commit()
    print("Таблица успешно создана в PostgreSQL")

    # cursor.execute("DROP TABLE no_validate_lids;")
    # # TODO Получить результат записи
    # record = cursor.fetchall()
    # print("Результат", record)
    # TODO Удалить таблицу
    # delete_query = """DROP TABLE no_validate_lids"""
    # cursor.execute(delete_query)
    # connection.commit()
    # count = cursor.rowcount
    # print(count, "Таблица успешно удалена")

    # # TODO запись в файл таблицы
    # sql = "COPY(SELECT inn_company FROM no_validate_lids) TO STDOUT WITH (FORMAT CSV, HEADER, DELIMITER ';')"
    # with open("table.csv", "w") as file:
    #     cursor.copy_expert(sql, file)

    # path_normalized = os.path.abspath('file_base.csv')
    # with open(path_normalized, 'r', newline='') as file:
    #     reader = csv.DictReader(file, delimiter=';')
    #     count = 1
    #     for item in reader:
    #         print(item['name_company'])

    # cursor.execute("INSERT INTO no_validate_lids (name_company, inn_company,  mail_company, tel_company, kpp_company,"
    #                " ogrn_company, registration_date_start, registration_date_end,"
    #                "adress_company, boss_company,) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    #                (item['name_company'], item['inn_company'], item['mail_company'], item['tel_company'],
    #                 item['kpp_company'], item['ogrn_company'], item['registration_date_start'],
    #                 item['registration_date_end'], item['adress_company'],
    #                 item['boss_company']))
    # count += 1
    # connection.commit()
#         print(f'{count}', "Строк записано успешно")

# cursor.execute("SELECT adress_company from no_validate_lids")
# p =[]
# for i in cursor:
#     # print(i)
#     p.append(i)
#
# #     # count += 1
# #     print("Результат")
#     # print(f'{count}')
#     # print()
#
#
# # print(p[3])
# # print(p)
# d = re.findall(r"121099", str(p[-3]))
# # print(d)
# c = "121099"
# t = re.sub(r"[\[|\]|']", '', str(d))
#
#
# if int(t) == int(c):
#     cursor.execute("SELECT name_company, inn_company, adress_company from no_validate_lids where inn_company = '7705707793'")
#     print("Результат", cursor.fetchall())

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
