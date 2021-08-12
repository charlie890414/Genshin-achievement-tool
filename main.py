import pyautogui
from difflib import SequenceMatcher
from google_api import recognize
from setting import PAUSE, ICON_PATH, SCROLL_CLICKS, GRID_LEFT, GRID_TOP, GRID_WIDTH, GRID_LENGTH, WORD_RATIO_THRESHOLD
from tool import *

pyautogui.PAUSE = PAUSE


def click_game():
    genshin = None
    genshin = pyautogui.locateOnScreen(ICON_PATH)
    if genshin:
        debug = pyautogui.screenshot(region=genshin)
        debug.save(f'debug/icon.png')
        pyautogui.click(genshin)
    else:
        raise ValueError


if is_admin():
    click_game()
    pyautogui.moveTo(GRID_LEFT, GRID_TOP)
    myachievements = set()
    prev = None
    while True:
        time.sleep(0.2)
        img = pyautogui.screenshot(
            f'debug/screenshot.png', region=(GRID_LEFT, GRID_TOP, GRID_WIDTH, GRID_LENGTH))
        img = filter_img_text(img)
        img.save(f'debug/screenshot.png')
        recognize(f'debug/screenshot.png', f'debug/output.txt')
        clean_text = map(lambda s: get_clean_text(s), open(
            f'debug/output.txt', encoding='utf-8').read().split('\n'))
        clean_text = filter(lambda s: s, clean_text)
        myachievements.update(clean_text)
        if len(myachievements) == prev:
            break
        scroll(SCROLL_CLICKS)
        prev = len(myachievements)
    open('myachievements.txt', 'w',
         encoding='utf-8').write('\n'.join(myachievements))

    all_achievements = get_all_achievements()
    not_finish_achievements = []
    for achievement in all_achievements.keys():
        for myachievement in myachievements:
            if SequenceMatcher(None, get_clean_text(achievement), myachievement).ratio() > WORD_RATIO_THRESHOLD:
                print('Similer achievement', myachievement, '->', achievement)
                break
        else:
            not_finish_achievements.append(achievement)
    open('not_finish_achievements.txt', 'w',
         encoding='utf-8').write('\n'.join([f'{not_finish_achievement}\t{all_achievements[not_finish_achievement]}' for not_finish_achievement in not_finish_achievements]))
else:
    print("Please run with admin mode or use the run.bat")
