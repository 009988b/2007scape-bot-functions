import pyautogui


def start_afk_agility(obstacles):
    if len(obstacles) > 0:
        selected = obstacles[0]
        rand = random() * 12
        if random() > 0.5:
            rand *= -1
        posX = (selected[0] + selected[2] / 2)
        posX += rand
        posY = (selected[1] + selected[3] / 2)
        posY += rand
        pyautogui.moveTo(posX, posY)
        pyautogui.click(button='left', clicks=1, interval=random() * 3)

