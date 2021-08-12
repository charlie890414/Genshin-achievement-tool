import ctypes
import time
import re
import requests
from bs4 import BeautifulSoup
import win32api
import win32con

from setting import LANG, WORD_IMG_THRESHOLD


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def scroll(clicks=0, delta_x=0, delta_y=0, delay_between_ticks=0.1):
    if clicks > 0:
        increment = win32con.WHEEL_DELTA
    else:
        increment = win32con.WHEEL_DELTA * -1

    for _ in range(abs(clicks)):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,
                             delta_x, delta_y, increment, 0)
        time.sleep(delay_between_ticks)


def filter_img_text(img):
    img = img.convert("L")

    color_table = []
    for color in range(256):
        if color < WORD_IMG_THRESHOLD:
            color_table.append(0)
        else:
            color_table.append(1)

    return img.point(color_table, '1')

def get_clean_text(text):
    return re.sub(
        r'[^a-zA-Z0-9\u4e00-\u9fa5 ]', '', text).strip()

def get_all_achievements():
    res = requests.get(
        f'https://genshin.honeyhunterworld.com/db/achiev/ac_1/?lang={LANG}')
    res = BeautifulSoup(res.text, features="lxml")
    name =  list(map(lambda row: row.text, res.select('table.art_stat_table > tr:nth-child(n) > td:nth-child(3) > a')))
    description = list(map(lambda row: row.text, res.select('table.art_stat_table > tr:nth-child(n+2) > td:nth-child(4)')))
    return {name[i]: description[i] for i in range(len(name))}
