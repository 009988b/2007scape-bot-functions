import pyautogui
from random import randint, random
from PIL import ImageGrab, Image, ImageOps
import numpy as np
import math
import cv2 as cv


def face_camera_north():
    offset = randint(-12, 12)
    offsety = randint(-12, 12)
    pt = (666 + offset, 50 + offsety)
    pyautogui.moveTo(pt)
    pyautogui.click(clicks=randint(1, 2), interval=random(), button='left')
    pyautogui.moveTo((865 / 2, 830 / 2))


def minimap_move_to(destination):
    offset = randint(-1, 1)
    offsety = randint(-1, 1)
    pt = (destination[0] + offset, destination[1] + offsety)
    pyautogui.moveTo(pt)
    if pyautogui.position().x - pt[0] < 10:
        pyautogui.click(clicks=randint(1, 2), interval=random() * 5, button='left')
        return True
    else:
        return "moving"


def dist_from_minimap_center(pt):
    map_center = [(820 - 660) / 2, (210 - 30) / 2]
    dx = math.fabs(pt[0] - map_center[0])
    dy = math.fabs(pt[1] - map_center[1])
    return (dx, dy)


def minimap_match(template_img):
    w, h = template_img.shape
    minimap_img = ImageGrab.grab(bbox=[660, 30, 820, 210])
    img_np = np.array(minimap_img)
    img_rgb = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)
    res = cv.matchTemplate(img_gray, template_img, cv.TM_CCOEFF_NORMED)
    thresh = 0.65
    loc = np.where(res >= thresh)
    rects = []  # position boxes on screen
    for pt in zip(*loc[::-1]):
        x = pt[0]
        y = pt[1]
        rect = [(x, y), (x + w, y + h)]
        rc = rect_center(rect, 0)
        dist = dist_from_minimap_center(rc)
        color = (255, 255, 255)
        if dist[0] < 10 and dist[1] < 10:
            color = (0, 255, 0)
        cv.rectangle(img_rgb, rect[0], rect[1], color, 2)
        rect = [(pt[0] + 660, pt[1] + 30), (pt[0] + 660 + w, pt[1] + 30 + h)]
        rects.append(rect)
    return img_rgb, rects


def move_to_minimap_match(template_img_path, is_moving):
    im, matches = minimap_match(cv.imread(template_img_path, 0))
    # print(matches)
    if matches is None:
        # if none here, we are at waypoint, go to next
        is_moving = False
        return matches, "moved"
    elif len(matches) > 0:
        pt = rect_center(matches[0], randint(-6, 6))
        return matches, minimap_move_to(pt)
    elif len(matches) == 0:
        return matches, "no match"
