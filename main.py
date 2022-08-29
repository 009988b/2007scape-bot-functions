import time
import cv2 as cv
from utilities import inventory as inv, core
from skills import herblore as h, fletching as fl, magic as ma
import pytesseract
import sys
from osrsbox import items_api

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





if __name__ == "__main__":
    items = items_api.load()
    core.find_window()
    inventory = []
    # drop = right click, +30y, left click
    selected = None
    status = ""
    mode = sys.argv[1]
    attempts = 0
    moving = False
    # face_camera_north()
    init_time = time.time()
    est_time_left = 3600
    while True:
        if mode == "pots" or mode == "clean":
            if attempts == 1:
                est_time_left, end = h.start(sys.argv, attempts)
            else:
                unused, end = h.start(sys.argv, attempts)
        elif mode == "enchant":
            if attempts == 1:
                est_time_left, end = ma.start(sys.argv, attempts)
            else:
                unused, end = ma.start(sys.argv, attempts)
        else:
            if attempts == 1:
                est_time_left, end = fl.start(sys.argv, attempts)
            else:
                unused, end = fl.start(sys.argv, attempts)
        attempts += 1
        if end - init_time > (est_time_left*60):
            break
        if cv.waitKey(1) & 0Xff == ord('q'):
            break
