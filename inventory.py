from PIL import ImageGrab, Image, ImageOps
import cv2 as cv
from osrsbox import items_api, monsters_api
import requests
from io import BytesIO


all_db_items = items_api.load()
all_db_monsters = monsters_api.load()


def empty_inv(saved_coords):
    # x 600+45(x)
    # y 500+40(y)
    for x in range(0, 4):
        for y in range(1, 6):
            if (x, y) not in saved_coords:
                drop_item([600 + (45 * x), 500 + (39 * y)])


def drop_item(item_center_pt):
    offset = randint(-2, 2)
    offsety = randint(-2, 2)
    pt = (item_center_pt[0] + offset, item_center_pt[1] + offsety)
    pyautogui.moveTo(pt)
    pyautogui.click(clicks=1, interval=random() / 2, button='right')
    pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y + 45)
    pyautogui.click(clicks=1, interval=(random() * 1.5) / 2, button='left')


def get_inventory_item_rects(template_img):
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
        rect = [(pt[0], pt[1]), (pt[0] + w, pt[1] + h)]
        cv.rectangle(img_rgb, rect[0], rect[1], (255, 255, 255), 2)
        rects.append(rect)
    return img_rgb, rects


def get_item_icon(item_id):
    for item in all_db_items:
        if item.id == item_id:
            response = requests.get("https://osrsbox.com/osrsbox-db/items-icons/" + str(item_id) + ".png")
            im = Image.open(BytesIO(response.content))
            im.save(str(item_id) + ".png")
            return cv.imread(str(item_id) + ".png", 0)
