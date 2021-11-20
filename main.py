import numpy as np
import math
import time
import sys
import cv2 as cv
import win32gui
import pyautogui
from random import randint, random
from PIL import ImageGrab, Image, ImageOps
import banking as bank
import inventory as inv
import herblore
import utilities
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


if __name__ == "__main__":
    find_window()
    item_icons = []
    inventory = []
    # drop = right click, +30y, left click
    for id in item_ids_to_fetch:
        item_icons.append((id, inv.get_icon(id)))
    dimensions = win32gui.GetWindowRect(hwnd)
    selected = None
    status = ""
    attempts = 0
    moving = False
    # face_camera_north()
    init_time = time.time()
    est_time_left = 3600
    while True:
        #if attempts == 1:
            #est_time_left = start_herblore(sys.argv, attempts)
        #else:
            #start_herblore(sys.argv, attempts)
        attempts += 1
        if end - init_time > (est_time_left*60):
            break
        if cv.waitKey(1) & 0Xff == ord('q'):
            break
