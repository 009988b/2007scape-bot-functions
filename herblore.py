import pyautogui
import cv2 as cv
from random import randint, random
from PIL import ImageGrab, Image, ImageOps
import numpy as np
import math
import time
from inventory import get_inventory_item_rects, get_item_icon
import pytesseract


def clean_all_herbs():
    # x 600+45(x)
    # y 500+40(y)
    for x in range(0, 4):
        for y in range(0, 7):
            rand = random() * 6
            if random() > 0.5:
                rand *= -1
            pyautogui.moveTo((600+rand+(45*x),500+rand+(39*y)))
            pyautogui.click(clicks=1, interval=random()/2)


def make_unf_pots():
    #with full inv
    rand = random() * 6
    if random() > 0.5:
        rand *= -1
    pyautogui.moveTo((600 + rand + (45 * randint(0,2)), 500 + rand + (39 * randint(0,2))))
    pyautogui.click(clicks=1, interval=random() / 2.5)
    time.sleep(0.2)
    pyautogui.moveTo((600 + rand + (45 * randint(2,3)), 500 + rand + (39 * randint(5,6))))
    pyautogui.click(clicks=1, interval=random() / 2.5)
    time.sleep(0.3)
    pyautogui.moveTo((250 + rand, 750 + rand))
    pyautogui.click(clicks=2, interval=random() / 3)