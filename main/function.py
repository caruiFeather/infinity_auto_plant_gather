import time
import numpy as np
import pyautogui
import cv2 as cv


def pressKey(key, pressTime=0.1):
    # 按压指定按键,pressTimes太短可能无法被检测到
    pyautogui.keyDown(key)
    time.sleep(pressTime)
    pyautogui.keyUp(key)


def click(x=None, y=None, button='left', clickTime=0.1):
    # 点击指定位置
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown(button=button)
    time.sleep(clickTime)
    pyautogui.mouseUp(button=button)


def checkImage(templatePath,region=(0, 0, 1920, 1080)):
    # 检查屏幕上是否存在指定模板图像
    scs = pyautogui.screenshot(region=region)
    template = cv.imread(templatePath)
    gray_image = cv.cvtColor(np.array(scs), cv.COLOR_BGR2GRAY)
    gray_template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    result = cv.matchTemplate(gray_image, gray_template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    print(templatePath,'相似度:',max_val)
    return max_val, int(max_loc[0]+template.shape[1]/2), int(max_loc[1]+template.shape[0]/2)


def findAndPress(templatePath, key, tryTimes=1, timeout=0.4, threshold=0.8):
    # 查找并按压指定模板图像
    for i in range(tryTimes):
        confiLevel, x, y = checkImage(templatePath)
        if confiLevel > threshold:
            pressKey(key)
            return True
        else:
            time.sleep(timeout)
    return False


def findAndClick(templatePath, button='left',xoffset=0, yoffset=0,
                 threshold=0.8,tryTimes=1, timeout=1, clickTime=0.1
                 ):
    # 查找并点击指定模板图像
    for i in range(tryTimes):
        confiLevel, x, y = checkImage(templatePath)
        if confiLevel > threshold:
            click(int(x+xoffset), int(y+yoffset), button, clickTime)
            return True
        else:
            time.sleep(timeout)
    return False


def releaseAllKeys():
    """释放所有可能处于按下状态的按键"""
    # 常见按键列表
    common_keys = [
        'a',  'd', 's', 'w',
        'ctrl', 'alt', 'shift'
    ]

    # 尝试释放每个按键
    for key in common_keys:
        try:
            pyautogui.keyUp(key)
        except Exception as e:
            # 忽略无法释放的键
            pass
