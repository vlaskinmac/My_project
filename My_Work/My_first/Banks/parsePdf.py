import os
import random
import shutil
import time
import zipfile
from pathlib import Path
import fitz
import re
import cv2
import pytesseract
import mod_logger
# создаем директорию для загрузки pdf
from PIL import Image

# name = 'test_2'
# file_x = os.path.abspath(os.path.join(file_way_2, name))
# if not os.path.exists(file_x):
#     os.mkdir(file_x)
# директория загрузки pdf - в конце цикла удаляется
# from My_Work.My_first.Banks import get_inn
from My_Work.My_first.Banks.data_check import check_inn_ya

file_way = os.path.abspath('C:\\working_download\\down_step_1\\download')
logger = mod_logger.get_logger(__name__)


# проходим по pdf файлам


def base_pdf():
    global file_x, name, pdf_document, file, file_, pdf_file, zip_file_pre, file_new
    try:
        logger.info(f"начало pdf функции")
        for dirpath, dirnames, filenames in os.walk(file_way):
            for file in filenames:
                file_zip = os.path.abspath(os.path.join(file_way, file))
                logger.info(f'файл на входе  <{file}>')
                # проверка на формат
                if zipfile.is_zipfile(file_zip):  # определяем архив или нет
                    logger.info(f"файл <zip>")
                    #  обрезка расширения для имени новой папки
                    index = file_zip.index('.')
                    name = file_zip[:index]
                    # путь до новой папки
                    file_x_zip = os.path.abspath(os.path.join(file_way, name))
                    if not os.path.exists(file_x_zip):
                        os.mkdir(file_x_zip)
                        zip_archive = zipfile.ZipFile(file_zip, "r")
                        # место для сохранения распаковки
                        zip_file_pre = os.path.abspath(os.path.join(file_way, file_x_zip))
                        zip_archive.extractall(zip_file_pre)
                        if not zip_file_pre:
                            logger.warning(f'ошибка распаковки zip файла <{zip_file_pre}>')
                            logger.info(f'ошибка распаковки zip файла <{zip_file_pre}>')
                        zip_archive.close()
                        os.remove(file_zip)
                    for dirpath, dirnames, filenames in os.walk(zip_file_pre):
                        folder_zip = dirpath
                        for file in filenames:
                            file_pdf = os.path.abspath(os.path.join(dirpath, file))
                            if file_pdf.endswith('.pdf'):
                                logger.info(f"<zip --> файл <pdf>")
                                z = random.randint(1, 999)
                                newName = f'{z}.pdf'
                                file_new = os.path.abspath(os.path.join(file_way, newName))
                                logger.info(f"новое имя файла <{newName}>")
                                # print(file_new)
                                os.rename(file_pdf, file_new)
                                # print(file_new, 'way file')
                        shutil.rmtree(folder_zip)
                        # for dirpath, dirnames, filenames in os.walk(file_way):
                        #     for file_p in filenames:
                        #         print(file_p)
                        index = file_new.index('.')
                        name = file_new[:index]
                        file_x = os.path.abspath(os.path.join(file_way, name))
                    if not os.path.exists(file_x):
                        os.mkdir(file_x)
                        logger.info(f"создана новая папка <{name}>")
                    for dirpath, dirnames, filenames in os.walk(file_way):
                        for file_p in filenames:
                            pdf_document = f'{file_p}'
                            pdf_file = os.path.abspath(os.path.join(file_way, pdf_document))
                            logger.info(f"найден документ в папке <{pdf_document}>")
                        # print('kkk')
                        return pdf_file
                elif file_zip.endswith('.pdf'):
                    logger.info(f" файл <pdf>")
                    file_pdf = file_zip
                    z = random.randint(1, 999)
                    newName = f'{z}.pdf'
                    file_new = os.path.abspath(os.path.join(file_way, newName))
                    logger.info(f"новое имя файла <{newName}>")
                    # print(file_new)
                    os.rename(file_pdf, file_new)
                    # print(file_new, 'way file')
                    # for dirpath, dirnames, filenames in os.walk(file_way):
                    # for file_p in filenames:
                    #     pass
                    # print(file_p)
                    index = file_new.index('.')
                    name = file_new[:index]
                    file_x = os.path.abspath(os.path.join(file_way, name))
                    if not os.path.exists(file_x):
                        os.mkdir(file_x)
                        logger.info(f"создана новая папка <{name}>")
                    for dirpath, dirnames, filenames in os.walk(file_way):
                        for file_p in filenames:
                            pdf_document = f'{file_p}'
                            pdf_file = os.path.abspath(os.path.join(file_way, pdf_document))
                            logger.info(f"найден документ в папке <{pdf_document}>")
                        # print('kkk')
                        return pdf_file
    except:
        pass


def prepare_pdf():
    global png_file_pre
    logger.info(f"начало распаковки <pdf>")
    try:
        # for _file in e():
        # print(_file)
        # pdf_fil = os.path.abspath(os.path.join(file_way, e()))
        doc = fitz.open(base_pdf())
        # print(pdf_fil)
        page_count = 0
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                page_count += 1
                pix1.writePNG(f"{file_x}/picture_number_{page_count}_from_page_{i + 1}.png")
                pix1 = None
        png_file_pre = os.path.abspath(os.path.join(file_way, file_x))
        # print(png_file_pre)
        return png_file_pre

    except:

        # if not png_file_pre:
        logger.warning(f'нет картинок страниц из <pdf>')
        logger.info(f'нет картинок страниц из <pdf>')



def tesseract():
    list_text = []
    global a, textt
    way = prepare_pdf()
    logger.info(f" начало <tesseract>")
    try:
        for dirpath, dirnames, filenames in os.walk(way):
            for fil in filenames:
                # print(fil)
                png_file_pr = os.path.abspath(os.path.join(way, fil))
                # print(fil)
                if png_file_pr.endswith('.png'):
                    # print(png_file_pr)
                    img = cv2.imread(str(png_file_pr))
                    # print(img)
                    textt = pytesseract.image_to_string(img)
                    list_text.append(textt)
    except:
        pass
    if not list_text:
        logger.warning(f'нет текста <tesseract>')
        logger.info(f'нет текста <tesseract>')
    return list_text


def parse_inn():
    list_inn = []
    logger.info(f" начало <регулярки>")
    text = tesseract()
    # for text in tesseract():

    ogrn_pre = re.compile(r"(\W+[\w+]{4}\W*[\d+]{13}\W)\+?", flags=re.I)  # 'огрн'

    inn_ooo_pre = re.compile(r'(\W+[\w+]{3}[\W]{2}[\d+]{10}\W)\+?', flags=re.I)  # 'инн ooo'
    inn_ooo_pre_2 = re.compile(r'(\W+[\w+]{4}[\W]{2}[\d+]{10}\W)\+?', flags=re.I)  # 'инн ooo 2'
    inn_ooo_pre_3 = re.compile(r'(\W+[\w+]{3}\W[\d+]{10}\W)\+?', flags=re.I)  # 'инн ooo 3'
    inn_ooo_pre_4 = re.compile(r'(\W+[\w+]{4}\W[\d+]{10}\W)\+?', flags=re.I)  # 'инн ooo 4'
    inn_ooo_pre_5 = re.compile(r'(\W*[\d+]{10}\W*)\+?', flags=re.I)  # 'инн ooo 5'

    inn_ip = re.compile(r'(\W+[\w+]{3}[\W]{2}[\d+]{12}\W)\+?', flags=re.I)  # 'инн ип'
    inn_ip_2 = re.compile(r'(\W+[\w+]{4}[\W]{2}[\d+]{12}\W)\+?', flags=re.I)  # 'инн ип 2'
    inn_ip_3 = re.compile(r'(\W+[\w+]{3}\W[\d+]{12}\W)\+?', flags=re.I)  # 'инн ип 3'
    inn_ip_4 = re.compile(r'(\W+[\w+]{4}\W[\d+]{12}\W)\+?', flags=re.I)  # 'инн ип 4'

    ogrn = ogrn_pre.findall(str(text))
    logger.info(f'огрн <ogrn> {ogrn}')
    inn_ooo = inn_ooo_pre.findall(str(text))
    logger.info(f'инн <inn_ooo> {inn_ooo}')
    inn_ooo_2 = inn_ooo_pre_2.findall(str(text))
    logger.info(f'инн <inn_ooo_2> {inn_ooo_2}')
    inn_ooo_3 = inn_ooo_pre_3.findall(str(text))
    logger.info(f'инн <inn_ooo_3> {inn_ooo_3}')
    inn_ooo_4 = inn_ooo_pre_4.findall(str(text))
    logger.info(f'инн <inn_ooo_4> {inn_ooo_4}')
    inn_ooo_5 = inn_ooo_pre_5.findall(str(text))
    logger.info(f'инн <inn_ooo_5> {inn_ooo_5}')

    inn__ip = inn_ip.findall(str(text))
    logger.info(f'инн ИП <inn__ip> {inn__ip}')
    inn__ip_2 = inn_ip_2.findall(str(text))
    logger.info(f'инн ИП <inn__ip_2> {inn__ip_2}')
    inn__ip_3 = inn_ip_3.findall(str(text))
    logger.info(f'инн ИП <inn__ip_3> {inn__ip_3}')
    inn__ip_4 = inn_ip_4.findall(str(text))
    logger.info(f'инн ИП <inn__ip_4> {inn__ip_4}')

    for i in ogrn:
        if i:
            list_inn.append(i)
            # print(ogrn, 'ogrn')
    for i in inn_ooo:
        if i:
            list_inn.append(i)
            # print(inn_ooo, 'inn_ooo')
    for i in inn_ooo_2:
        if i:
            list_inn.append(i)
            # print(inn_ooo_2, 'inn_ooo_2')
    for i in inn_ooo_3:
        if i:
            list_inn.append(i)
            # print(inn_ooo_3, 'inn_ooo_3')

    for i in inn_ooo_4:
        if i:
            list_inn.append(i)
            # print(inn_ooo_4, 'inn_ooo_4')
    for i in inn_ooo_5:
        if i:
            list_inn.append(i)
            # print(inn_ooo_5, 'inn_ooo_5')

    for i in inn__ip:
        if i:
            list_inn.append(i)
            # print(inn__ip, 'инн ooo')

    for i in inn__ip_2:
        if i:
            list_inn.append(i)
            # print(inn__ip_2, 'inn__ip_2')

    for i in inn__ip_3:
        if i:
            list_inn.append(i)
            # print(inn__ip_3, 'inn__ip_3')

    for i in inn__ip_4:
        if i:
            list_inn.append(i)
            # print(inn__ip_4, 'inn__ip_4')
    if not list_inn:
        logger.warning(f"пусто <регулярки>")
        logger.info(f"пусто <регулярки>")
    print(list_inn, '---список инн')

    shutil.rmtree(file_x)
    logger.info(f" временная папка удалена <{file_x}>")
    os.remove(file_new)
    logger.info(f" переименованный файл удален <{file_new}>")
    return list_inn


def parse_list_inn_pdf(*args):
    winner = args
    parse_list_inn_pdf = parse_inn()
    if not parse_list_inn_pdf:
        # вызов модуля с ожиданием протокола итогов затем повторное определние победителю
        pass
    else:
        # for i in parse_list_inn_pdf:
        check_inn = check_inn_ya.parse_index_name(str(parse_list_inn_pdf).split(','), winner)
        return check_inn

        # вызов модуля с поиском в базе
        # вызов модуля с поиском в яндексе по названию далее поиск в базе, при отсутствии  дополнение базы

# ======================================================
# list_inn
# вызов модуля с поиском в базе c определением:
# if not list_inn:
# вызов модуля с поиском в яндексе по названию далее поиск в базе, при отсутствии  дополнение базы
# ======================================================

# if __name__ == '__main__':
# parse_list_inn_pdf()

# тессеракт не видит 1 принимает как спецсимвол
# pars_inn_2()
