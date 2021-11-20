import pyautogui
from random import random
from PIL import ImageGrab
import math
import cv2 as cv
from utilities import inventory as inv
from utilities.core import get_bounding_rect_from_pts


def get_pickup_rects(o_img, cnts):  # returns bounding rect(s) of item(s) to pickup
    items = []
    line_pts = []
    for c in cnts:
        # compute the center of each contour
        M = cv.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            line_pts.append((cX, cY))
    # cv.rectangle(output,(minx,miny),(maxx,maxy),(0,255,255),2)
    maxslope = 0
    item_split_indices = [0]
    for x in range(1, len(line_pts) - 2):
        x1, y1 = (line_pts[x - 1])
        x2, y2 = (line_pts[x])
        if (x2 - x1) != 0:
            m = (y2 - y1) / (x2 - x1)
            if m > maxslope:
                maxslope = m
            if (m <= 0.05) and (m >= -0.05):
                cv.line(o_img, line_pts[x - 1], line_pts[x], (0, 255, 255), 2)
            else:
                # split lines based on slope and dist
                # print(item_split_indices)
                # print(math.dist((x1,y1),(x2,y2)))
                if (math.dist((x1, y1), (x2, y2))) >= 40 and x != 1:
                    item_split_indices.append(x)
    if len(item_split_indices) == 1:
        rect = get_bounding_rect_from_pts(line_pts[1:len(line_pts)])
        if rect not in items:
            items.append(rect)
    elif (len(item_split_indices) > 1):
        for i in range(0, len(item_split_indices) - 1):
            if i == 0:
                rect = get_bounding_rect_from_pts(line_pts[1:item_split_indices[i + 1]])
            elif (i + 1 <= len(item_split_indices) + 1):
                rect = get_bounding_rect_from_pts(line_pts[item_split_indices[i]:item_split_indices[i + 1]])
            if rect not in items:
                items.append(rect)
    for item in items:
        cv.rectangle(o_img, item[0], item[1], (0, 0, 255), 1)
    return items


def bury_bones(min_bone_count):
    inv_img, bones = inv.get_item_rects(inv.get_icon(526))
    inv_img2, big_bones = inv.get_item_rects(inv.get_icon(532))
    if len(bones) + len(big_bones) > min_bone_count:
        for rect in bones:
            rect[0]
            pt = ((rect[0][0] + 625 + rect[1][0] + 625) / 2, (rect[0][1] + 485 + rect[1][1] + 485) / 2)
            pyautogui.moveTo(pt)
            pyautogui.click(clicks=1, interval=random() * 3, button='left')
        for rect in big_bones:
            rect[0]
            pt = ((rect[0][0] + 625 + rect[1][0] + 625) / 2, (rect[0][1] + 485 + rect[1][1] + 485) / 2)
            pyautogui.moveTo(pt)
            pyautogui.click(clicks=1, interval=random() * 3, button='left')


def start_combat(targets, items, players, target_mask, selected):
    combat_img = ImageGrab.grab(bbox=[10, 50, 140, 69])
    enemy_name = pytesseract.image_to_string(combat_img)
    for name in marked_enemy_names:
        if enemy_name != None:
            if similar(enemy_name, name) > 0.7:
                enemy_name = name

    min_dist = 3000
    other_players_target = None

    for r in targets:
        for p in players:
            dist = math.sqrt(math.pow(r[0] - p[0][0], 2) + math.pow(r[1] - p[0][1], 2))
            if p in items:
                players.remove(p)

            if dist < 200:
                if r in targets:
                    if (dist < min_dist):
                        if r[2] > 30:
                            other_players_target = r
                    targets.remove(r)
                continue
        if r[2] > 10 and r in targets:
            cv.rectangle(target_mask, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (0, 255, 255), 2)

    if other_players_target is not None:
        if len(players) >= 1:
            if players[0] not in items:
                cv.line(target_mask, (other_players_target[0], other_players_target[1]),
                        (players[0][0][0], players[0][0][1]), (0, 255, 255), 2)
        cv.rectangle(target_mask, (other_players_target[0], other_players_target[1]), (
        other_players_target[0] + other_players_target[2], other_players_target[1] + other_players_target[3]),
                     (0, 40, 255), 2)

    if random() > 0.95:
        bury_bones(0)
    if enemy_name not in marked_enemy_names:
        if len(items) >= 1:
            # item pickup
            item = items[0]
            min = item[0]
            max = item[1]
            pyautogui.moveTo((min[0] + max[0]) / 2, ((min[1] + max[1]) / 2) + 10)
            pyautogui.click(clicks=2, interval=random(), button='left')
        elif len(rects[4]) > 0:
            # need combat panel screengrab and imagetotext
            # if in combat dont move cursor or click
            #
            if selected != targets[0]:
                selected = targets[0]
                pyautogui.moveTo((selected[0] + selected[2] / 2), (selected[1] + selected[3] / 2))
                pyautogui.click(button='left', clicks=1, interval=random())
