import cv2
import pyautogui
import time
import numpy as np
import pyscreenshot as imageGrab
import os
import pytesseract
'''----------Один монитор----------'''
import mss
import mss.tools

# top - подтянуть  верхнюю граицу вверх
# left - значение 0 левая сторона  экрана, если '-10' смещение влево, если '10' смещение вправо
# width - базовая ширина скрина
# height - подтянуть  нижнюю граицу вниз

#
# with mss.mss() as sct:
#     # The screen part to capture
#     monitor = {"top": 260, "left": 0, "width": 100, "height": 135}
#     output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor) # именуем файл по координатам
#
#     # Grab the data
#     sct_img = sct.grab(monitor)
#
#     # Save to the picture file
#     mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
#     print(output)

'''----------Второй монитор----------'''

# with mss.mss() as sct:
#     monitor_number = 3
#     mon = sct.monitors[monitor_number]
#     monitor = {"top": 260, "left": 300, "width": 200, "height": 435, "mon": monitor_number}
#     output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor) # именуем файл по координатам
#
#     # Grab the data
#     sct_img = sct.grab(monitor)
#
#     # Save to the picture file
#     mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
#     print(output)

with mss.mss() as sct:
    # Get information of monitor 3 - позиционирует по своим правилам не по винде
    monitor_number = 3
    mon = sct.monitors[monitor_number]

    # The screen part to capture
    monitor = {
        "top": mon["top"] + 215,  # 100px from the top
        "left": mon["left"] + 90,  # 100px from the left
        "width": 290,
        "height": 85,
        "mon": monitor_number,
    }
    filename = "image.png".format(**monitor)

    # Grab the data
    sct_img = sct.grab(monitor)

    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
    print(filename)
img = cv2.imread(filename)
text = pytesseract.image_to_string(img)
print(text)
# x = 1
# last_time = time.time()
# x_1 = 2555
# y_1 = 251
# x_2 = 2778
# y_2 = 364
#
#
# while True:
#     screen = np.array(imageGrab.grab(bbox=(x_1, y_1, x_2, y_2)))
#     print(f'loop took {time.time() - last_time }, seconds')
#     last_time = time.time()
#     cv2.imshow('window',  cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
#     cv2.imwrite(filename, screen)
#     x = x + 1
#     print(x)
#     if x == 2:
#         cv2.destroyAllWindows()
#         break


# time.sleep(2)
#
# print((pyautogui.position()))
# Point(x=2555, y=251)
# Point(x=2778, y=364)
