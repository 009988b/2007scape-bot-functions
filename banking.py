import pyautogui
from random import randint, random
import time
import pytesseract


def open(rects):
    offset = randint(-2, 2)
    pt = rect_center(rects[0], offset)
    pyautogui.moveTo(pt[0],pt[1],random()/5,pyautogui.easeInQuad)
    pyautogui.click(clicks=1, interval=random() / 2, button='left')
    #pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y + 45)
    #pyautogui.click(clicks=1, interval=(random() * 1.5) / 2, button='left')


def set_quantity(quantity):
    if quantity == "all":
        pt = (350 + randint(-2, 2), 640 + randint(-2, 2))
        pyautogui.moveTo(pt[0],pt[1],random()/4,pyautogui.easeInQuad)
        time.sleep(0.25)
        pyautogui.click(clicks=1, interval=(random() * 1.5) / 2, button='left')
    if quantity == "custom":
        pt = (330 + randint(-2, 2), 640 + randint(-2, 2))
        pyautogui.moveTo(pt[0],pt[1],random()/4,pyautogui.easeInQuad)
        time.sleep(0.25)
        pyautogui.click(clicks=1, interval=(random() * 1.5) / 2, button='left')


def close():
    pt = (500 + randint(-2, 2), 50 + randint(-2, 2))
    pyautogui.moveTo(pt[0],pt[1],random()/4,pyautogui.easeInQuad)
    pyautogui.click(clicks=1, interval=(random() * 1.5) / 2, button='left')


def withdraw(tab, coord, should_select_tab):
    # tabs x = 100+40(x)
    # tabs y = 80
    # items x = 103 + 50(x)
    # items y = 120 + 38(y)
    pt_tab = (100 + (40 * tab) + randint(-3, 3), 80 + randint(-3, 3))
    if should_select_tab:
        pyautogui.moveTo(pt_tab[0],pt_tab[1],random()/6,pyautogui.easeInQuad)
        pyautogui.click(clicks=1, interval=random() / 2, button='left')
    time.sleep(0.1)
    pt = (103 + (50 * coord[0]) + randint(-4, 4), 120 + (38 * coord[1]) + randint(-4, 4))
    pyautogui.moveTo(pt[0],pt[1],random()/4,pyautogui.easeInQuad)
    pyautogui.click(clicks=1, interval=random() / 2, button='left')


def deposit_all():
    # if bank open and quantity = "all"
    rand = random() * 6
    if random() > 0.5:
        rand *= -1
    pyautogui.moveTo(600 + rand, 500 + rand,random()/4,pyautogui.easeInQuad)
    pyautogui.click(clicks=1, interval=random() / 2)
    pyautogui.moveTo(690+ rand, 500 + (39*3) + rand, random() / 4, pyautogui.easeInQuad)
    pyautogui.click(clicks=1, interval=random() / 2)