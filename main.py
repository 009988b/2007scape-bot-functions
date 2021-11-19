import numpy as np
import math
import time
import cv2 as cv
import win32gui
import pyautogui
from random import randint, random
from PIL import ImageGrab, Image, ImageOps
from utilities import get_color_masks
from movement import face_camera_north
from herblore import clean_all_herbs, make_unf_pots
from inventory import get_inventory_item_rects, get_item_icon
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# define the list of boundaries


marked_enemy_names = [
    "Giant rat",
    "Giant frog",
    "Monk"
]

item_ids_to_fetch = [
    526, 532, 2134, 2142
]


def find_window():  # find window name returns PID of the window
    global hwnd
    hwnd = win32gui.FindWindow(None, "RuneLite - r00ntang")
    # hwnd = win32gui.GetForegroundWindow()860
    print('findWindow:', hwnd)
    win32gui.SetActiveWindow(hwnd)
    # win32gui.ShowWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)


def open_bank(rects):
    offset = randint(-2, 2)
    offsety = randint(-2, 2)
    pt = ((rects[0][0]+rects[0][2]/2) + offset, (rects[0][1]+rects[0][3]/2) + offsety)
    pyautogui.moveTo(pt)
    pyautogui.click(clicks=1, interval=random() / 2, button='left')
    #pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y + 45)
    #pyautogui.click(clicks=1, interval=(random() * 1.5) / 2, button='left')


def set_bank_quantity(quantity):
    if quantity == "all":
        pt = (350 + randint(-2, 2), 640 + randint(-2, 2))
        pyautogui.moveTo(pt)
        pyautogui.click(clicks=1, interval=(random() * 1.5) / 2, button='left')
    if quantity == "custom":
        pt = (330 + randint(-2, 2), 640 + randint(-2, 2))
        pyautogui.moveTo(pt)
        pyautogui.click(clicks=1, interval=(random() * 1.5) / 2, button='left')


def close_bank():
    pt = (500 + randint(-2, 2), 50 + randint(-2, 2))
    pyautogui.moveTo(pt)
    pyautogui.click(clicks=1, interval=(random() * 1.5) / 2, button='left')


def withdraw_from_bank(tab, coord, should_select_tab):
    # tabs x = 100+40(x)
    # tabs y = 80
    # items x = 103 + 50(x)
    # items y = 120 + 38(y)
    pt_tab = (100 + (40 * tab) + randint(-3, 3), 80 + randint(-3, 3))
    if should_select_tab:
        pyautogui.moveTo(pt_tab)
        pyautogui.click(clicks=1, interval=random() / 2, button='left')
    time.sleep(0.1)
    pt_item = (103 + (50 * coord[0]) + randint(-4, 4), 120 + (38 * coord[1]) + randint(-4, 4))
    pyautogui.moveTo(pt_item)
    pyautogui.click(clicks=1, interval=random() / 2, button='left')


def deposit_all():
    # if bank open and quantity = "all"
    rand = random() * 6
    if random() > 0.5:
        rand *= -1
    pyautogui.moveTo((600 + rand, 500 + rand))
    pyautogui.click(clicks=1, interval=random() / 2)

def herb_cleaning(bank_tab, bank_coord):
    # herb cleaning
    clean_all_herbs()
    if len(rects[2]) > 0:
        open_bank(rects[2])
    time.sleep(1)
    deposit_all()
    withdraw_from_bank(bank_tab, bank_coord)
    time.sleep(0.5)
    close_bank()

def craft_unf_pots(rects, bank_tab, vial_coord, herb_coord, is_init):
    # unf pot crafting
    if len(rects[4]) > 0:
        open_bank(rects[4])
    time.sleep(0.3)
    if is_init:
        set_bank_quantity("custom")
    withdraw_from_bank(bank_tab, vial_coord, True)
    withdraw_from_bank(bank_tab, herb_coord, False)
    time.sleep(0.2)
    close_bank()
    time.sleep(0.1)
    make_unf_pots()
    time.sleep(10.2)
    if len(rects[4]) > 0:
        open_bank(rects[4])
        time.sleep(0.6)
        deposit_all()
        time.sleep(0.3)
        close_bank()

if __name__ == "__main__":
    find_window()
    item_icons = []
    inventory = []
    # drop = right click, +30y, left click
    for id in item_ids_to_fetch:
        item_icons.append((id, get_item_icon(id)))
    dimensions = win32gui.GetWindowRect(hwnd)
    selected = None
    status = ""
    attempts = 0
    moving = False
    # face_camera_north()
    while True:
        start = time.time()
        img = ImageGrab.grab(bbox=dimensions)
        img_np = np.array(img)
        img_np = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)
        masks, rects, items, players = get_color_masks(img_np)
        #for rect in rects[2]:
            #print(rect)
        if attempts == 0:
            craft_unf_pots(rects,1,(0, 0),(1,0), True)
        else:
            craft_unf_pots(rects,1,(0, 0),(1,0), False)
        #herb_cleaning(1,(3,0))
        end = time.time()
        elapsed = end - start
        rate = (14/(elapsed/60))*60
        print("time elapsed:")
        print(end - start)
        print("rate: "+ str(rate) + " pots/hour")
        attempts += 1
        if cv.waitKey(1) & 0Xff == ord('q'):
            break
