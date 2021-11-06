import numpy as np
import math
import cv2 as cv
import win32gui
import pyautogui
from random import randint, random
from PIL import ImageGrab, Image, ImageOps
import pytesseract
from difflib import SequenceMatcher
from osrsbox import items_api, monsters_api
import requests
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# define the list of boundaries
boundary_colors = [
    ([0, 70, 235], [0, 80, 255]),  # PLAYER COLOR - 0
    ([0, 180, 0], [80, 255, 80]),  # GREEN - 1
    ([0, 200, 200], [60, 255, 255]),  # YELLOW - 2
    ([180, 0, 235], [255, 15, 255]),  # HIGHLIGHTED ITEM (PICK UP)- 3
    ([250, 250, 0], [255, 255, 5])  # UNIT TO ATTACK   (CYAN)   - 4
]

all_db_items = items_api.load()
all_db_monsters = monsters_api.load()

marked_enemy_names = [
    "Giant rat",
    "Giant frog",
    "Monk"
]

swamp_castle = ["paths/swamp-castle/swamp.PNG","paths/swamp-castle/1.PNG","paths/swamp-castle/2.PNG","paths/swamp-castle/3.PNG","paths/swamp-castle/castle.PNG","paths/swamp-castle/stairs.png","paths/swamp-castle/booth.png","paths/swamp-castle/stairs3.png"]

paths = [

]

item_ids_to_fetch = [
    526,532,2134,2142
]

def findWindow_runelite():  # find window name returns PID of the window
    global hwnd
    hwnd = win32gui.FindWindow(None, "RuneLite - r00ntang")
    # hwnd = win32gui.GetForegroundWindow()860
    print('findWindow:', hwnd)
    win32gui.SetActiveWindow(hwnd)
    # win32gui.ShowWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)

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

def get_other_player_rects(o_img, cnts): # returns bounding rect(s) of other player(s) on screen
    players = []
    line_pts = []
    bbox = [1,200,823,730]
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
        cv.putText(o_img, "player" + str(i), (players[i][0][0],players[i][0][1]), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
        cv.rectangle(o_img, player[0], player[1], (0, 0, 255), 1)
        i += 1
    return players

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
        ret, thresh = cv.threshold(output_gray, 0, 255, cv.THRESH_BINARY_INV if is_pickup_text or is_player_mask else cv.THRESH_BINARY)
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
            if is_interactable and w+h > 180:
                cv.rectangle(output, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 255, 255), 2)
                r.append(rect)
            elif is_player_mask and w+h > 20:
                #cv.rectangle(output, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 255, 255), 2)
                #cv.putText(output, str(w+h), (x,y), cv.FONT_HERSHEY_SIMPLEX, 12)
                r.append(rect)
            else:
                cv.rectangle(output, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 255, 255), 2)
                r.append(rect)
        rects.append(r)
        masks.append(output)
    return masks, rects, items, players

def rect_center(rect, offset):
    #[(x1,y1),(x2,y2)]
    print(rect)
    return (((rect[0][0] + rect[1][0]) / 2)+offset, ((rect[0][1] + rect[1][1]) / 2)+offset)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

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
            dist = math.sqrt(math.pow(r[0]-p[0][0],2)+math.pow(r[1]-p[0][1],2))
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
        cv.rectangle(target_mask, (other_players_target[0], other_players_target[1]), (other_players_target[0] + other_players_target[2], other_players_target[1] + other_players_target[3]), (0, 40, 255), 2)

    if random() > 0.95:
        bury_bones(0)
    if enemy_name not in marked_enemy_names:
        if len(items) >= 1:
            # item pickup
            item = items[0]
            min = item[0]
            max = item[1]
            pyautogui.moveTo((min[0] + max[0]) / 2, ((min[1] + max[1]) / 2)+10)
            pyautogui.click(clicks=2, interval=random(), button='left')
        elif len(rects[4]) > 0:
            # need combat panel screengrab and imagetotext
            # if in combat dont move cursor or click
            #
            if selected != targets[0]:
                selected = targets[0]
                pyautogui.moveTo((selected[0] + selected[2] / 2), (selected[1] + selected[3] / 2))
                pyautogui.click(button='left', clicks=1, interval=random())

def dist_from_minimap_center(pt):
    map_center = [(820-660)/2,(210-30)/2]
    dx = math.fabs(pt[0]-map_center[0])
    dy = math.fabs(pt[1]-map_center[1])
    return (dx,dy)

def minimap_match(template_img):
    w, h = template_img.shape
    minimap_img = ImageGrab.grab(bbox=[660,30,820,210])
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
        rc = rect_center(rect,0)
        dist = dist_from_minimap_center(rc)
        color = (255, 255, 255)
        if dist[0] < 10 and dist[1] < 10:
            color = (0, 255, 0)
        cv.rectangle(img_rgb, rect[0], rect[1], color, 2)
        rect = [(pt[0] + 660, pt[1]+30), (pt[0] + 660 + w, pt[1] + 30 + h)]
        rects.append(rect)
    return img_rgb, rects

def get_inventory_item_rects(template_img):
    w, h = template_img.shape
    #pyautogui.press("esc")
    invent_img = ImageGrab.grab(bbox=[625,485,820,750])
    img_np = np.array(invent_img)
    img_rgb = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)
    res = cv.matchTemplate(img_gray, template_img, cv.TM_CCOEFF_NORMED)
    thresh = 0.6
    loc = np.where(res >= thresh)
    rects = [] #position boxes on screen
    for pt in zip(*loc[::-1]):
        rect = [(pt[0],pt[1]),(pt[0]+w,pt[1]+h)]
        cv.rectangle(img_rgb,rect[0],rect[1],(255,255,255),2)
        rects.append(rect)
    return img_rgb, rects

def get_item_icon(item_id):
    for item in all_db_items:
        if (item.id == item_id):
            response = requests.get("https://osrsbox.com/osrsbox-db/items-icons/" + str(item_id) + ".png")
            im = Image.open(BytesIO(response.content))
            im.save(str(item_id) + ".png")
            return cv.imread(str(item_id) + ".png", 0)

def face_camera_north():
    offset = randint(-12,12)
    offsety = randint(-12,12)
    pt = (666+offset,50+offsety)
    pyautogui.moveTo(pt)
    pyautogui.click(clicks=randint(1,2), interval=random(), button='left')
    pyautogui.moveTo((865/2,830/2))

def minimap_move_to(destination):
    offset = randint(-1, 1)
    offsety = randint(-1, 1)
    pt = (destination[0]+offset,destination[1]+offsety)
    pyautogui.moveTo(pt)
    if pyautogui.position().x - pt[0] < 10:
        pyautogui.click(clicks=randint(1,2), interval=random()*5, button='left')
        return True
    else:
        return "moving"

def drop_item(item_center_pt):
    offset = randint(-6,6)
    offsety = randint(-6,6)
    pt = (item_center_pt[0]+offset,item_center_pt[1]+offsety)
    pyautogui.moveTo(pt)
    pyautogui.click(clicks=1, interval=random(), button='right')
    pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y + 30)
    pyautogui.click(clicks=1, interval=random()*1.5, button='left')

def bury_bones(min_bone_count):
    inv_img, bones = get_inventory_item_rects(get_item_icon(526))
    inv_img2, big_bones = get_inventory_item_rects(get_item_icon(532))
    if len(bones)+len(big_bones) > min_bone_count:
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

def move_to_minimap_match(template_img_path, is_moving):
    im, matches = minimap_match(cv.imread(template_img_path, 0))
    #print(matches)
    if matches is None:
        #if none here, we are at waypoint, go to next
        is_moving = False
        return matches, "moved"
    elif len(matches) > 0:
        pt = rect_center(matches[0], randint(-6, 6))
        return matches, minimap_move_to(pt, is_moving)
    elif len(matches) == 0:
        return matches, "no match"

if __name__ == "__main__":
    findWindow_runelite()
    item_icons = []
    inventory = []
    #drop = right click, +30y, left click
    for id in item_ids_to_fetch:
        item_icons.append((id,get_item_icon(id)))
    dimensions = win32gui.GetWindowRect(hwnd)
    selected = None
    status = ""
    step = 4
    path = swamp_castle
    direction = -1
    face_camera_north()
    while True:
        img = ImageGrab.grab(bbox=dimensions)
        img_np = np.array(img)
        img_np = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)
        masks, rects, items, players = get_color_masks(img_np)
        start_combat(rects[4], items, players, masks[4], selected)
        #matches, status = move_to_minimap_match("paths/swamp-castle/stairs3.PNG", moving)
        #im, matches = minimap_match(cv.imread("paths/swamp-castle/stairs.PNG",0))
        cv.imshow("frame", masks[4])
        #cv.imshow("waypoint", im)
        #if len(matches) > 0:
            #pt = rect_center(matches[0], randint(0, 0))
            #status = minimap_move_to(pt)
            #if (status == True):
                #step += direction
                #go to next waypt

            #if moving:
                #continue
        #print(matches)
        #if matches is not None and len(matches) != 0:
            #.rectangle(img_np, matches[0][0], matches[0][1], (255, 0, 0), 2)

        if cv.waitKey(1) & 0Xff == ord('q'):
            break
