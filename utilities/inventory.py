from PIL import ImageGrab, Image, ImageOps
import cv2 as cv
from osrsbox import items_api, monsters_api
import requests
from io import BytesIO
from random import random
import pyautogui, time
import numpy as np

all_db_items = items_api.load()
all_db_monsters = monsters_api.load()


def empty(saved_coords):
    # x 600+45(x)
    # y 500+40(y)
    for x in range(0, 4):
        for y in range(1, 6):
            if (x, y) not in saved_coords:
                drop_item([600 + (45 * x), 500 + (39 * y)])


def use(item1_coord, item2_coord, action_pos_on_screen):
    rand = random() * 6
    if random() > 0.5:
        rand *= -1
    pyautogui.moveTo(600 + rand + (45 * item1_coord[0]), 500 + rand + (39 * item1_coord[1]), random() / 4,
                     pyautogui.easeInQuad)
    pyautogui.click(clicks=1, interval=random() / 2.5)
    time.sleep(0.2)
    pyautogui.moveTo(600 + rand + (45 * item2_coord[0]), 500 + rand + (39 * item2_coord[1]),random()/4,pyautogui.easeInQuad)
    pyautogui.click(clicks=1, interval=random() / 2.5)
    time.sleep(0.33)
    if action_pos_on_screen is not None:
        pyautogui.moveTo(action_pos_on_screen[0] + rand, action_pos_on_screen[1] + rand, random() / 4, pyautogui.easeInQuad)
        pyautogui.click(clicks=2, interval=random() / 3)


def drop_item(item_center_pt):
    offset = randint(-2, 2)
    offsety = randint(-2, 2)
    pt = (item_center_pt[0] + offset, item_center_pt[1] + offsety)
    pyautogui.moveTo(pt)
    pyautogui.click(clicks=1, interval=random() / 2, button='right')
    pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y + 45)
    pyautogui.click(clicks=1, interval=(random() * 1.5) / 2, button='left')


def get_item_rects(template_img):
    w, h = template_img.shape
    # pyautogui.press("esc")
    invent_img = ImageGrab.grab(bbox=[625, 485, 820, 750])
    img_np = np.array(invent_img)
    img_rgb = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)
    res = cv.matchTemplate(img_gray, template_img, cv.TM_CCOEFF_NORMED)
    thresh = 0.6
    loc = np.where(res >= thresh)
    rects = []  # position boxes on screen
    for pt in zip(*loc[::-1]):
        rect = [pt[0],pt[1],w,h]
        #cv.rectangle(img_rgb, rect[0], rect[1], (255, 255, 255), 2)
        rects.append(rect)
    print("matches found: " + str(len(rects)))
    return img_rgb, rects


def get_icon(item_id):
    for item in all_db_items:
        if item.id == item_id:
            response = requests.get("https://osrsbox.com/osrsbox-db/items-icons/" + str(item_id) + ".png")
            im = Image.open(BytesIO(response.content))
            im.save(str(item_id) + ".png")
            return cv.imread(str(item_id) + ".png", 0)
