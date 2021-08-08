# -*- coding: utf-8 -*-
import logging
import os
import re
import shutil
import time
import zipfile
import random
import comtypes.client
from cachetools import TTLCache
from termcolor import cprint
import mod_logger
from My_Work.My_first.Banks.data_check import check_inn_ya

logger = mod_logger.get_logger(__name__)
_sessions_cache = TTLCache(maxsize=200, ttl=300)
# logging.disable(logging.INFO)
file_way = os.path.abspath('C:\working_download\down_step_1\download')


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 6)
        cprint(f'Функция {func.__name__} работала {elapsed} секунд(ы)', color='green')
        return result

    return surrogate


class ParseDocx:
    file_way = os.path.abspath('C:\working_download\down_step_1\download')

    def __init__(self, check_name, check_name_2):
        self.check_name = check_name
        self.check_name_2 = check_name_2

    @time_track
    def convert_docuent(self):
        # _sessions_cache.clear()
        # delete_file()
        # print('------------')
        time.sleep(5)
        logger.info(f'начало функции <не pdf>')
        for dirpath, dirnames, filenames in os.walk(self.file_way):
            for self.file in filenames:
                self.path_file_pre = os.path.join(self.file_way, self.file)
                logger.info(f'файл на входе  <{self.file}>')
                try:
                    if self.path_file_pre != self.check_name and self.path_file_pre != self.check_name_2:
                        self.delete_file()
                        logger.info(f'удален файл <{self.path_file_pre}>')
                        time.sleep(1)
                    if self.path_file_pre.endswith('.rtf') or self.path_file_pre.endswith('.doc'):
                        format = self.path_file_pre.split('.')[-1]
                        logger.info(f'формат файла <{format}>')
                        self.out_file = os.path.abspath(os.path.join(self.file_way,
                                                                     f'{random.randint(1, 99)}'))  # name of output file added to the current working directory
                        logger.info(f'новое имя файла <{self.out_file}>')
                        # конвертер
                        self.word = comtypes.client.CreateObject('Word.Application')
                        self.doc = self.word.Documents.Open(self.path_file_pre)  # name of input file
                        self.doc.SaveAs(self.out_file,
                                        FileFormat=16)  # output file format to Office word Xml default (code=16)
                        self.doc.Close()
                        self.word.Quit()
                        self.path_file = os.path.join(self.file_way, f'{self.out_file}.docx')
                        logger.info(f'конвертация файла <{self.path_file}>')
                        if not self.path_file:
                            logger.warning(f'ошибка конвертации файла <{self.path_file}>')
                            logger.info(f'ошибка конвертации файла <{self.path_file}>')
                        self.check_name = self.path_file
                        time.sleep(3)
                        os.remove(self.path_file_pre)
                        logger.info(f'удален файл <{self.path_file_pre}>')
                        if not self.path_file:
                            logger.warning(f'нет данных <{self.path_file}>')
                            logger.info(f'нет данных <{self.path_file}>')
                        return self.path_file
                    elif self.path_file_pre.endswith('.odt'):
                        os.remove(self.file_x_zip)
                    elif self.path_file_pre.endswith('.docx'):
                        format = self.path_file_pre.split('.')[-1]
                        logger.info(f'формат файла <{format}>')
                        self.check_name_2 = self.path_file_pre
                        if not self.path_file_pre:
                            logger.warning(f'нет данных <{self.path_file_pre}>')
                            logger.info(f'нет данных <{self.path_file_pre}>')
                        print()
                        print(self.path_file_pre)
                        print()
                        return self.path_file_pre
                    elif zipfile.is_zipfile(self.path_file_pre):  # определяем zip или нет
                        logger.info(f'формат файла <zip>')
                        #  обрезка расширения для имени новой папки
                        index = self.path_file_pre.index('.')
                        name = self.path_file_pre[:index]
                        # путь до новой папки
                        self.file_x_zip = os.path.abspath(os.path.join(file_way, name))
                        if not os.path.exists(self.file_x_zip):
                            os.mkdir(self.file_x_zip)
                            logger.info(f"создана новая папка <{name}>")
                            self.zip_archive = zipfile.ZipFile(self.path_file_pre, "r")
                            # место для сохранения распаковки
                            self.zip_file_pre = os.path.abspath(os.path.join(self.file_way, self.file_x_zip))
                            self.zip_archive.extractall(self.zip_file_pre)
                            logger.info(f"путь распаковки zip <{self.zip_file_pre}>")
                            if not self.zip_file_pre:
                                logger.warning(f'ошибка распаковки zip файла <{self.zip_file_pre}>')
                                logger.info(f'ошибка распаковки zip файла <{self.zip_file_pre}>')
                            self.zip_archive.close()
                        for dirpath, dirnames, filenames in os.walk(self.zip_file_pre):
                            for self.file in filenames:
                                self.path_file_pre = os.path.abspath(os.path.join(dirpath, self.file))
                                logger.info(f"новый путь к файлу zip <{self.zip_file_pre}>")
                                if self.path_file_pre.endswith('.rtf') or self.path_file_pre.endswith('.doc'):
                                    format = self.path_file_pre.split('.')[-1]
                                    logger.info(f'формат файла <{format}>')
                                    self.out_file = os.path.abspath(os.path.join(self.file_way,
                                                                                 f'{random.randint(1, 99)}'))  # name of output file added to the current working directory
                                    logger.info(f'новое имя файла <{self.out_file}>')
                                    # конвертер
                                    self.word = comtypes.client.CreateObject('Word.Application')
                                    self.doc = self.word.Documents.Open(self.path_file_pre)  # name of input file
                                    self.doc.SaveAs(self.out_file,
                                                    FileFormat=16)  # output file format to Office word Xml default (code=16)
                                    self.doc.Close()
                                    self.word.Quit()
                                    self.path_file = os.path.join(self.file_way, f'{self.out_file}.docx')
                                    logger.info(f'конвертация файла <{self.path_file}>')
                                    if not self.path_file:
                                        logger.warning(f'ошибка конвертации файла <{self.path_file}>')
                                        logger.info(f'ошибка конвертации файла <{self.path_file}>')
                                    self.check_name = self.path_file
                                    time.sleep(3)
                                    os.remove(self.path_file_pre)
                                    logger.info(f'удален файл <{self.path_file_pre}>')
                                    if not self.path_file:
                                        logger.warning(f'нет данных <{self.path_file}>')
                                        logger.info(f'нет данных <{self.path_file}>')
                                    return self.path_file
                                elif self.path_file_pre.endswith('.docx'):
                                    format = self.path_file_pre.split('.')[-1]
                                    logger.info(f'формат файла <{format}>')
                                    self.check_name_2 = self.path_file_pre
                                    if not self.path_file_pre:
                                        logger.warning(f'нет данных <{self.path_file_pre}>')
                                        logger.info(f'нет данных <{self.path_file_pre}>')
                                    return self.path_file_pre

                        # elif self.path_file_pre.endswith('.pdf'):
                        #     print(self.path_file_pre, '.pdf.pdf.pdf')
                        #     self.check_name_3 = self.path_file_pre
                        #     return self.path_file_pre
                except Exception as exc:
                    print(exc, 'except-------')

    def delete_file(self):
        # _sessions_cache.clear()
        # self.path_file, self.path_file_pre = self.convert_docuent()
        try:
            logger.info(f'начало удаления мусора')
            for dirpath, dirnames, filenames in os.walk(self.file_way):
                for self.file in filenames:
                    path_file_del = os.path.join(dirpath, self.file)
                    # logger.info(f'файл для удаления <{path_file_del}>')
                    # path_file_del_filename, file_extension = os.path.splitext(path_file_del)
                    # check_name_2_filename, file_extension = os.path.splitext(self.check_name_2)
                    if path_file_del == self.check_name:
                        os.remove(path_file_del)
                        logger.info(f'файл удален <{path_file_del}>')
                        # print('delele', self.check_name, '33333333333333----------')
                    elif path_file_del == self.check_name_2:
                        os.remove(path_file_del)
                        logger.info(f'файл удален <{path_file_del}>')
                        # print('delete', self.check_name_2, '44444444444444----------')
                    # elif path_file_del_filename == check_name_2_filename:
                    #     os.remove(path_file_del_filename)
                    #     print('delete', path_file_del_filename, '5555555555----------')
        except:
            pass

    @time_track
    def read_document(self):
        # time.sleep(5)
        # for self.item in self.convert_docuent():
        self.item = self.convert_docuent()
        if not self.item:
            logger.warning(f'нет данных документа <{self.item}>')
            logger.info(f'нет данных документа <{self.item}>')
        try:
            self.file_content_pre = zipfile.ZipFile(self.item)
            self.file_content = self.file_content_pre.read('word/document.xml').decode('utf-8')
            self.content = re.sub('<(.|\n)*?>', '', self.file_content)
            time.sleep(2)
            self.file_content_pre.close()
            if not self.content:
                logger.warning(f'ошибка чтения документа')
                logger.info(f'ошибка чтения документа')
            logger.info(f'документ прочитан')
            return self.content
        except Exception as exc:
            print(exc, 'read_document')


class ParserInn(ParseDocx):
    count = 0

    def __init__(self):
        super().__init__(check_name=None, check_name_2=None)

    @time_track
    def parse_inn(self):
        # time.sleep(5)
        list_inn = []
        list_adress = []
        try:
            logger.info(f" начало <регулярки>")
            self.tex = self.read_document()
            if not self.tex:
                logger.warning(f'ошибка нет данных документа')
                logger.info(f'ошибка нет данных документа')
            # print(self.tex)
            self.text = str(self.tex).replace('«', '"').replace('»', '"')
            self.inn_table_pre_ip = re.compile(r'(ИНН\W*[\d*]{12}\W*)', flags=re.I)  # 'инн из таблицы'-ИП
            self.inn_table_pre_ip_2 = re.compile(r'(Индивидуальный предприниматель\W*\w*\W*\w*\W*\w*\W*[\d]{12})',
                                                 flags=re.I)  # 'инн из таблицы'-ИП без пробела
            self.inn_table_pre_2 = re.compile(r'(ИНН\W*[\d*]{10}\W*)', flags=re.I)  # 'инн из таблицы'
            self.inn_table_pre_3 = re.compile(r'([\w+\W*]{130}\W+[\d+]{6},[\w+\W*]{20})', flags=re.I)  # 'адрес'
            self.inn_table_ip = self.inn_table_pre_ip.findall(str(self.text))
            logger.info(f'инн <inn_table_ip> {self.inn_table_ip}')
            self.inn_table_ip_2 = self.inn_table_pre_ip_2.findall(str(self.text))
            logger.info(f'инн <inn_table_ip_2> {self.inn_table_ip_2}')
            self.inn_table_2 = self.inn_table_pre_2.findall(str(self.text))
            logger.info(f'инн <inn_table_2> {self.inn_table_2}')
            self.inn_table_3 = self.inn_table_pre_3.findall(str(self.text))
            logger.info(f'инн <inn_table_3> {self.inn_table_3}')

            for i in self.inn_table_ip:
                if i:
                    list_inn.append(i)
                    # print(ogrn, 'ogrn')
            for i in self.inn_table_ip_2:
                if i:
                    list_inn.append(i)
                    # print(inn_ooo, 'inn_ooo')
            for i in self.inn_table_2:
                if i:
                    list_inn.append(i)
                    # print(inn_ooo_2, 'inn_ooo_2')
            if not list_inn:
                for i in self.inn_table_3:
                    if i:
                        if re.findall(r'Место публикации', str(i), flags=re.I):
                            continue
                        elif re.findall(r'Место рассмотрения', str(i), flags=re.I):
                            continue
                        else:
                            list_adress.append(i)
            if not list_inn:
                logger.warning(f"пусто <регулярки>")
                # logger.info(f"пусто <регулярки>")
            # отбираем inn
            list_inn_res = []
            for i in list_inn:
                if i not in list_inn_res:
                    i_pre_2 = re.findall(r"\d+", str(i), flags=re.I)
                    i_pre = re.sub(r'[\'|\"|\]|\[|.|,|\s|\t|\r]', '', str(i_pre_2))
                    list_inn_res.append(i_pre)
                else:
                    del i
            time.sleep(0.2)
            try:
                os.remove(self.path_file)

                # logger.info(f'удален файл {self.path_file}')
            except:
                pass
            try:
                os.remove(self.path_file_pre)
                # logger.info(f'удален файл {self.path_file_pre}')
            except:
                pass
            # удаляем папку распаковки архива и файл
            try:
                shutil.rmtree(self.file_x_zip)
                # logger.info(f'удалена папка {self.file_x_zip}')
            except:
                pass
            return list_inn_res, list_adress
        except Exception as exc:
            print(exc)

    def parse_list_inn_docx(self, *args):
        logger.info(f" начало <parse_list_inn_docx>")
        winner = args
        self.list_index_docx = []
        self.list_inn_docx, self.list_adress_docx = self.parse_inn()
        try:
            if not self.list_inn_docx:
                if self.list_adress_docx:
                    for self.item in self.list_adress_docx:
                        find_index_pre = re.findall(r'\W[\d+]{6},', str(self.item), flags=re.I)
                        if find_index_pre:
                            find_index_pre_2 = re.findall(r'[\d+]{6}', str(find_index_pre), flags=re.I)
                            self.find_index = re.sub(r'[\'|\"|\]|\[|.|,|\s|\t|\r]', '', str(find_index_pre_2))
                            if self.find_index:
                                self.list_index_docx.append(self.find_index)
                    self.list_index_docx_clean_pre = set(self.list_index_docx)
                    self.list_index_docx_clean = re.sub(r"[\t\s{})\[\]'(\"]", '', str(self.list_index_docx_clean_pre),
                                                        flags=re.I)
                    print(self.list_index_docx_clean.split(','), 'inn--', winner)
                    check_inn_index = check_inn_ya.parse_index_name(self.list_index_docx_clean.split(','), winner)
                    return check_inn_index
                else:
                    # вызов модуля с ожиданием протокола итогов затем повторное определние победителя
                    pass
            else:
                if self.list_inn_docx:
                    self.list_inn_docx_clean_pre = set(self.list_inn_docx)
                    self.list_inn_docx_clean = re.sub(r"[\t\s{})\[\]'(\"]", '', str(self.list_inn_docx_clean_pre),
                                                      flags=re.I)
                    print(self.list_inn_docx_clean.split(','), 'inn--', winner)

                    check_inn = check_inn_ya.parse_index_name(self.list_inn_docx_clean.split(','), winner)
                    return check_inn


        except Exception as exc:
            print(exc)
        if not self.list_inn_docx and self.list_adress_docx:
            logger.warning(f"пусто <inn_docx, adress_docx>")
            logger.info(f"пусто <inn_docx, adress_docx>")

            # вызов модуля с поиском в базе
            # вызов модуля с поиском в яндексе по названию далее поиск в базе, при отсутствии  дополнение базы


# ======================================================
# list_inn_res
# вызов модуля с поиском в базе
# ======================================================


parse_doc = ParseDocx(check_name=None, check_name_2=None)
parse = ParserInn()
# parse.parse_inn()
# parse.parse_list_inn_docx()
