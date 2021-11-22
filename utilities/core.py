import numpy as np
import math
import cv2 as cv
from random import randint, random
from PIL import ImageGrab, Image, ImageOps
from difflib import SequenceMatcher
import pytesseract
import win32gui


boundary_colors = [
    ([0, 70, 235], [0, 80, 255]),  # PLAYER COLOR - 0
    ([0, 180, 0], [80, 255, 80]),  # GREEN - 1
    ([0, 200, 200], [60, 255, 255]),  # YELLOW - 2
    ([180, 0, 235], [255, 15, 255]),  # HIGHLIGHTED ITEM (PICK UP)- 3
    ([250, 250, 0], [255, 255, 5])  # UNIT TO ATTACK   (CYAN)   - 4
]




def get_other_player_rects(o_img, cnts):  # returns bounding rect(s) of other player(s) on screen
    players = []
    line_pts = []
    bbox = [1, 200, 823, 730]
    for c in cnts:
        x, y, w, h = cv.boundingRect(c)
        r = [x, y, w, h]
        # compute the center of each contour
        M = cv.moments(c)
        if M["m00"] != 0 and w > 6 and h > 6:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            line_pts.append((cX, cY))
    # cv.rectangle(output,(minx,miny),(maxx,maxy),(0,255,255),2)
    maxslope = 0
    arr_split_indices = [0]
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
                # print(math.dist((x1,y1),(x2,y2)))
                if (math.dist((x1, y1), (x2, y2))) >= 40 and x != 1:
                    arr_split_indices.append(x)
    if len(arr_split_indices) == 1:
        rect = get_bounding_rect_from_pts(line_pts[1:len(line_pts)])
        if rect not in players:
            players.append(rect)
    elif (len(arr_split_indices) > 1):
        for i in range(0, len(arr_split_indices) - 1):
            if i == 0:
                rect = get_bounding_rect_from_pts(line_pts[1:arr_split_indices[i + 1]])
            elif (i + 1 <= len(arr_split_indices) + 1):
                rect = get_bounding_rect_from_pts(line_pts[arr_split_indices[i]:arr_split_indices[i + 1]])
            if rect not in players:
                players.append(rect)
    i = 0
    for player in players:
        cv.putText(o_img, "player" + str(i), (players[i][0][0], players[i][0][1]), cv.FONT_HERSHEY_SIMPLEX, 1,
                   (0, 0, 255))
        cv.rectangle(o_img, player[0], player[1], (0, 0, 255), 1)
        i += 1
    return players


def find_window():  # find window name returns PID of the window
    global hwnd
    hwnd = win32gui.FindWindow(None, "RuneLite - r00ntang")
    # hwnd = win32gui.GetForegroundWindow()860
    print('findWindow:', hwnd)
    win32gui.SetActiveWindow(hwnd)
    # win32gui.ShowWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)
    return win32gui.GetWindowRect(hwnd)


dimensions = find_window()


def get_color_masks(image):
    masks = []
    rects = []
    items = []
    players = []
    # loop over the boundaries
    for (lower, upper) in boundary_colors:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        is_pickup_text = False
        is_interactable = False
        is_player_mask = False
        is_target_mask = False
        if lower[0] == 180:
            is_pickup_text = True
        if lower[1] == 200:
            is_interactable = True
        if lower[2] == 235:
            is_player_mask = True
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv.inRange(image, lower, upper)
        output = cv.bitwise_and(image, image, mask=mask)
        output_gray = cv.cvtColor(output, cv.COLOR_RGB2GRAY)
        ret, thresh = cv.threshold(output_gray, 0, 255,
                                   cv.THRESH_BINARY_INV if is_pickup_text or is_player_mask else cv.THRESH_BINARY)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # item mask
        if is_pickup_text and len(contours) > 1:
            items = get_pickup_rects(output, contours)
        if is_player_mask and len(contours) > 1:
            players = get_other_player_rects(output, contours)
        # else:
        r = []
        for c in contours:
            x, y, w, h = cv.boundingRect(c)
            rect = [x, y, w, h]
            center_pt = (int(x+w-(w/2)),int(y+h-(h/2)))
            if is_interactable and w + h > 200:
                cv.rectangle(output, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 255, 255), 2)
                print(center_pt)
                cv.circle(output, center_pt, 3, (0,0,255), 1)
                r.append(rect)
            elif is_player_mask and w + h > 20:
                # cv.rectangle(output, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 255, 255), 2)
                # cv.putText(output, str(w+h), (x,y), cv.FONT_HERSHEY_SIMPLEX, 12)
                r.append(rect)
            elif w + h > 90:
                cv.rectangle(output, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 255, 255), 2)
                r.append(rect)
        rects.append(r)
        masks.append(output)
    return masks, rects, items, players


def get_bounding_rect_from_cnts(cnts):  # cnt = contour
    minx = 3000
    maxx = 0
    miny = 3000
    maxy = 0
    for c in cnts:
        for point in c:
            p = point[0]
            if p[0] < minx and p[0] != 0:
                minx = p[0]
            if p[1] < miny and p[1] != 0:
                miny = p[1]
            if p[0] > maxx and p[0] < 864:
                maxx = p[0]
            if p[1] > maxy and p[1] < 829:
                maxy = p[1]
    return [(minx, miny), (maxx, maxy)]


def get_bounding_rect_from_pts(pts):
    minx = 3000
    maxx = 0
    miny = 3000
    maxy = 0
    for p in pts:
        if p[0] < minx and p[0] != 0:
            minx = p[0]
        if p[1] < miny and p[1] != 0:
            miny = p[1]
        if p[0] > maxx and p[0] < 864:
            maxx = p[0]
        if p[1] > maxy and p[1] < 829:
            maxy = p[1]
    return [(minx, miny), (maxx, maxy)]


def rect_center(rect, offset):
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    return (int(x+w-(w/2)),int(y+h-(h/2)))


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
