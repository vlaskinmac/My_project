# -*- coding: utf-8 -*-
import os
import random
import time
import zipfile
from pathlib import Path
import sys
import comtypes.client
import docx
import docx2txt
import fitz
import olefile
import textract
import re
import cv2
import pytesseract

# создаем директорию для загрузки pdf
file_way = os.path.abspath('C:\\Users\\User\\PycharmProjects\\python_base\\python_base\\My_Work\\'
                           'My_first\\Banks\\Down\\Test_1')
