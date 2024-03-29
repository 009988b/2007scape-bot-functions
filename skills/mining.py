import pyautogui
import cv2 as cv
from random import randint, random
from PIL import Image, ImageOps
import numpy as np
import math
from utilities import inventory as inv
import pytesseract
import pyscreenshot as ImageGrab


def start(nodes, attempts):
    inv_img, ores = inv.get_item_rects(inv.get_icon(440))
    length = len(ores)
    status_img = ImageGrab.grab(bbox=[5, 45, 140, 69])
    img_np = np.array(status_img)
    img_np = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)
    status = pytesseract.image_to_string(img_np)
    #if random() > 0.96:
        #empty_inv([(0,0),(1,0)])
        #attempts = 0

    if status != "Mining" and status != "Scorpion" and len(nodes) > 0:
        selected = nodes[0]
        rand = random() * 12
        if random() > 0.5:
            rand *= -1
        posX = (selected[0] + selected[2] / 2)
        posX += rand
        posY = (selected[1] + selected[3] / 2)
        posY += rand
        pyautogui.moveTo(posX, posY)
        pyautogui.click(button='left', clicks=1, interval=random()*3)
    cv.imshow("test",np.array(status_img))


def drop_ores():
    length = 0
    inv_img, ores = inv.get_item_rects(inv.get_icon(436))
    length = len(ores)
    while length > 0:
        for rect in ores:
            pt = ((rect[0][0] + 625 + rect[1][0] + 625) / 2, (rect[0][1] + 485 + rect[1][1] + 485) / 2)
            drop_item(pt)
        inv_img, ores = inv.get_item_rects(inv.get_icon(436))
        length = len(ores)
