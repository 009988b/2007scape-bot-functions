import pyautogui
import cv2 as cv
import pytesseract
from utilities import inventory as inv, banking as bank, core
import time, math
from random import randint, random


def enchanting(bank_tab, item_coord, cosmicrune_coord, is_init):
    #lvl 1 enchant
    rects, isOpen = bank.is_open(False)
    if not isOpen:
        bank.open(rects[2])
    time.sleep(1)
    if is_init:
        bank.set_quantity("all")
    bank.withdraw(bank_tab, cosmicrune_coord, True)
    bank.withdraw(bank_tab, item_coord, False)
    time.sleep(0.1)
    bank.close()
    c = 0

    cast_lvl1_enchant()

    pyautogui.press('esc')
    rects, isOpen = bank.is_open(False)
    if not isOpen:
        bank.open(rects[2])
    time.sleep(0.4)
    bank.deposit_all()


def cast_lvl1_enchant():
    time.sleep(0.15 + random() / 3)
    pyautogui.press('f6')
    for c in range(0,3):
        inv_coord = (randint(1, 3), randint(0, 4))
        time.sleep(0.15 + random() / 3)
        rand = randint(-3,3)
        if random() > 0.5:
            rand *= -1
        pyautogui.moveTo(718+rand,499+rand,0.1+random()/2,pyautogui.easeInQuad)
        pyautogui.click(clicks=1, interval=random() / 3)
        #600+45 x , 500+39 y
        pyautogui.moveTo(600+(45*inv_coord[0])+rand,500+(39*inv_coord[1]+c)+rand,0.1+random()/3,pyautogui.easeInQuad)
        time.sleep(0.15)
        pyautogui.click(clicks=1, interval=random() / 3)
        time.sleep(37.7)


def start(argv, attempts):
    start = time.time()
    if argv[1] == "enchant":
        if attempts == 0:
            enchanting(4, (1, 0), (0,0), True)
        else:
            enchanting(4, (1, 0), (0,0), False)
        end = time.time()
        elapsed = end - start
        rate = (27 / (elapsed / 60)) * 60
    est_time_left = ((int(argv[2])-(27*attempts)) / rate) * 60
    print("script running for approx " + str(est_time_left) + "more minutes.")
    print("loop count - " + str(attempts))
    print("rate: " + str(int(rate)) + " casts/hour")
    print("est profit: " + str(int((rate*160)/100)) + "k/hour")
    return est_time_left, end