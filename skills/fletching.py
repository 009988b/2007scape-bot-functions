import pyautogui
import cv2 as cv
import pytesseract
from utilities import inventory as inv, banking as bank
import time, math
from random import randint, random

def use_chisel(inv_coord):
    inv.use(inv_coord,(randint(2,3),randint(0,2)),(250,750))


def cut_gems(bank_tab, gem_coord, chisel_inv_coord, is_init):
    # unf pot crafting
    rects, isOpen = bank.is_open(False)
    if not isOpen:
        bank.open(rects[2])
        time.sleep(1.2)
        if is_init:
            bank.set_quantity("all")
    bank.withdraw(bank_tab, gem_coord, True)
    time.sleep(0.2)
    bank.close()
    time.sleep(0.1)
    for x in range(0,3):
        inv.use(chisel_inv_coord, (randint(2, 3), randint(1+x, 3+x)), (250, 750))
        time.sleep(27)
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

def cut_logs_shortbow(bank_tab, logs_coord, knife_inv_coord, is_init):
    # unf pot crafting
    rects, isOpen = bank.is_open(False)
    if not isOpen:
        bank.open(rects[2])
        time.sleep(1.2)
        if is_init:
            bank.set_quantity("all")
    bank.withdraw(bank_tab, logs_coord, True)
    time.sleep(0.2)
    bank.close()
    time.sleep(0.1)
    for x in range(0,2):
        inv.use(knife_inv_coord, (randint(2, 3), randint(3+x, 4+x)), (150, 750))
        time.sleep(25.4)
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


def string_bows(bank_tab, bow_coord, string_coord, is_init):
    # unf pot crafting
    rects, isOpen = bank.is_open(False)
    if not isOpen:
        bank.open(rects[2])
        time.sleep(1.2)
        if is_init:
            bank.set_quantity("custom")
    bank.withdraw(bank_tab, bow_coord, True)
    bank.withdraw(bank_tab, string_coord, False)
    time.sleep(0.2)
    bank.close()
    time.sleep(0.1)
    inv.use((randint(2, 3), randint(0, 2)), (randint(2, 3), randint(5, 6)), (250, 750))
    time.sleep(15.6)
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


def cut_logs_longbow(bank_tab, logs_coord, knife_inv_coord, is_init):
    # unf pot crafting
    rects, isOpen = bank.is_open(False)
    if not isOpen:
        bank.open(rects[2])
        time.sleep(1.2)
        if is_init:
            bank.set_quantity("all")
    bank.withdraw(bank_tab, logs_coord, True)
    time.sleep(0.2)
    bank.close()
    time.sleep(0.1)
    for x in range(0,2):
        inv.use(knife_inv_coord, (randint(2, 3), randint(3+x, 4+x)), (250, 750))
        time.sleep(25.4)
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
    if argv[1] == "string":
        if attempts == 0:
            string_bows(1, (0, 0), (1, 0), True)
        else:
            string_bows(1, (0, 0), (1, 0), False)
        end = time.time()
        elapsed = end - start
        rate = (13 / (elapsed / 60)) * 60
    if argv[1] == "tips":
        for x in range(0,int(int(argv[2])/100)):
            inv.use((2,0),(1,0),(250,750))
            time.sleep(12.1)
    if argv[1] == "gems":
        if attempts == 0:
            cut_gems(2, (0, 0), (1,0), True)
        else:
            cut_gems(2, (0, 0), (1,0), False)
        end = time.time()
        elapsed = end - start
        rate = (27 / (elapsed / 60)) * 60
    if argv[1] == "logs":
        if attempts == 0:
            cut_logs_longbow(3, (0, 0), (1,0), True)
        else:
            cut_logs_longbow(3, (0, 0), (1,0), False)
        end = time.time()
        elapsed = end - start
        rate = (27 / (elapsed / 60)) * 60
    est_time_left = ((int(argv[2])-(27*attempts)) / rate) * 60
    print("script running for approx " + str(est_time_left) + "more minutes.")
    print("loop count - " + str(attempts))
    print("rate: " + str(rate) + " bolt tips/hour")
    print("est profit: " + str(rate*160))
    return est_time_left, end
