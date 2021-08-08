import os
import re
from pathlib import Path

import cv2
import pytesseract

file_way = os.path.abspath('C:\\Users\\User\\PycharmProjects\\python_base\\python_base\\My_Work\\My_first\\Banks\\Down')

# for filename in os.listdir(file_way):
# # print(fi)
#     if filename.endswith('.png'):
#         img = cv2.imread(filename)
#         text = pytesseract.image_to_string(img)
#
#         # get_note = re.findall('\d+', str(text))
#         # note = re.sub(r"['|\"|,|\s|\]|\[|\b|(|)\.|\r]", "", str(get_note))
#
#         # x = re.compile(r"[w\+W+][\d+]{10,12}", flags=re.I)
#         # y = re.findall(x, text)
#         # print(y)
#         # print(note) # только цифры
#         # print(get_note)#  цифры и знаки
#         # print(text)
#         x=re.compile('(\W\s+[\d+]{10,12}\s+\W\+?)', flags=re.I)
#         a = x.findall(str(text))
#         print(a)


# for dirpath, dirnames, filenames in os.walk(file_way):
#     for fil in filenames:
#         png_file_pre = os.path.abspath(os.path.join(file_way, fil))
#         # print(png_file_pre)
#         # print(fil)
#         try:
#             # for fi in os.listdir(png_file_pre):
#             # print(fi)
#             if png_file_pre.endswith('.png'):
#                 print(png_file_pre)
#                 img_ = cv2.imread(str(png_file_pre))
#                 # print(img)
#                 text = pytesseract.image_to_string(img_)
#                 #
#                 x = re.compile('(\W\s+[\d+]{10,12}\s+\W\+?)', flags=re.I)
#                 xx = re.compile(r"[\w+]{3}.[\d+]{10,12}", flags=re.I)
#                 a = x.findall(str(text))
#                 aa = xx.findall(str(text))
#                 # print(text)
#                 print(a)
#                 print(aa,'aa++')
#         except:
#             pass
# for dirpath, dirnames, filenames in os.walk(file_way):
#     for fil in filenames:
#         png_file_pre = os.path.abspath(os.path.join(file_way, fil))
#         # print(png_file_pre)
#         # print(fil)
#         try:
#             if png_file_pre.endswith('.png'):
#             # print(png_file_pre)
#                 img_ = cv2.imread(str(png_file_pre))
#                 print(img_)
#                 text = pytesseract.image_to_string(img_)
#                 print(text)
#                 x = re.compile('(\W\s+[\d+]{10,12}\s+\W\+?)', flags=re.I)
#                 xx = re.compile(r"[\w+]{3}.[\d+]{10,12}", flags=re.I)
#                 a = x.findall(str(text))
#                 aa = xx.findall(str(text))
#                 # print(text)
#                 print(a)
#                 print(aa, 'aa++')
#
#                 print(text)
#         except:
#             pass
#
try:
    for dirpath, dirnames, filenames in os.walk(file_way):
        for fil in filenames:
            png_file_pr = os.path.abspath(os.path.join(file_way, fil))
            # print(fil)
            if png_file_pr.endswith('.png'):
                print(png_file_pr)
                img = cv2.imread(str(png_file_pr))
                print(img)
                text = pytesseract.image_to_string(img)
                print(text)
                x = re.compile('(\W\s+[\d+]{10,12}\s+\W\+?)', flags=re.I)
                xx = re.compile(r"[\w+]{3}.[\d+]{10,12}", flags=re.I)
                a = x.findall(str(text))
                aa = xx.findall(str(text))
                # print(text)
                print(a)
                print(aa, 'aa++')

                print(text)

except:
    pass
