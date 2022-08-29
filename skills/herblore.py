import pyautogui
import cv2 as cv
from random import randint, random
import numpy as np
import time
from utilities import banking as bank, inventory as inv
import sys
import pyscreenshot as ImageGrab

def clean_inv():
    # x 600+45(x)
    # y 500+40(y)
    for x in range(0, 4):
        time.sleep(0.15 + random()/4)
        if not x & 0x1: #is odd
            for y in range(6, -1, -1):
                rand = random() * 6
                if random() > 0.5:
                    rand *= -1
                pyautogui.moveTo((600+rand+(45*x),500+rand+(39*y)))
                pyautogui.click(clicks=1, interval=random()/3)
        else:
            for y in range(0, 7):
                rand = random() * 6
                if random() > 0.5:
                    rand *= -1
                pyautogui.moveTo((600+rand+(45*x),500+rand+(39*y)))
                pyautogui.click(clicks=1, interval=random()/3)


def craft_inv_pots():
    #with full inv
    inv.use((randint(0,2),randint(0,2)),(randint(2,3),randint(5,6)),(250,750))


def cleaning(bank_tab, bank_coord):
    # herb cleaning
    clean_inv()
    rects, isOpen = bank.is_open(False)
    if not isOpen:
        bank.open(rects[2])
    time.sleep(1)
    bank.deposit_all()
    bank.withdraw(bank_tab, bank_coord, True)
    time.sleep(0.5)
    bank.close()


def craft_unf_pots(bank_tab, vial_coord, herb_coord, is_init):
    # unf pot crafting
    rects, isOpen = bank.is_open(False)
    if not isOpen:
        bank.open(rects[2])
        time.sleep(1.2)
        if is_init:
            bank.set_quantity("custom")
    bank.withdraw(bank_tab, vial_coord, True)
    bank.withdraw(bank_tab, herb_coord, False)
    time.sleep(0.2)
    bank.close()
    time.sleep(0.1)
    craft_inv_pots()
    time.sleep(10.2)
    rects, isOpen = bank.is_open(False)
    if not isOpen:
        bank.open(rects[2])
    time.sleep(0.6)
    rects, isOpen = bank.is_open(False)
    if isOpen:
        bank.deposit_all()
    time.sleep(0.3)
    if is_init:
        bank.close()


def start(argv, attempts):
    start = time.time()
    # img = ImageGrab.grab(bbox=dimensions)
    # img_np = np.array(img)
    # img_np = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)
    # masks, rects, items, players = get_color_masks(img_np)
    # cv.imshow("frame", masks[2])
    # for rect in rects[2]:
    # print(rect)
    num = 0
    if argv[1] == "pots":
        num = 14
        if attempts == 0:
            craft_unf_pots(1, (0, 0), (1, 0), True)
        else:
            craft_unf_pots(1, (0, 0), (1, 0), False)
        end = time.time()
        elapsed = end - start
        rate = (14 / (elapsed / 60)) * 60
    elif argv[1] == "clean":
        cleaning(1, (2, 0))
        end = time.time()
        elapsed = end - start
        rate = (28 / (elapsed / 60)) * 60
    est_time_left = ((int(argv[2])-(num*attempts)) / rate) * 60
    print("script running for approx " + str(est_time_left) + "more minutes.")
    print("loop count - " + str(attempts))
    print("rate: " + str(rate) + " pots/hour")
    return est_time_left, end
