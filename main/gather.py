import threading
import pyautogui
import time
from function import pressKey, click, checkImage, findAndClick, findAndPress


def buy():
    # 购买种子
    time.sleep(1)
    click(930, 560)  #确保点击落点在
    time.sleep(2)
    pressKey('2')  #购买种子数量的数字的十位数
    pressKey('delete')
    pressKey('4')  #购买种子数量的数字的个位数
    time.sleep(1)
    findAndClick(r'..\main\gatherImage\confirmInConvert.png')
    findAndClick(r'..\main\gatherImage\confirmInConvert.png')


def circulate():
    time.sleep(1)
    # 切换能力为种植,按键6为本人的种植套装的顺序
    pressKey('6', 0.2)

    def walk(key, duration):
        pyautogui.keyDown('ctrl')
        pressKey(key, duration)
        pyautogui.keyUp('ctrl')

    def fetch(stop_event):
        while not stop_event.is_set():
            findAndPress(r'..\main\gatherImage\fetch.png', 'f', threshold=0.9)

    def water(stop_event):
        while not stop_event.is_set():
            click(button='right')
            time.sleep(0.1)
            pressKey('e', 0.3)

    stopFetch = threading.Event()
    t1 = threading.Thread(target=walk, args=('w', 20))  #前走时间
    t2 = threading.Thread(target=fetch, args=(stopFetch,), daemon=True)
    t1.start()
    t2.start()
    t1.join()
    stopFetch.set()
    time.sleep(4)

    for i in range(4):
        pressKey('s', 0.2)
        pressKey('r', 0.04)
        if checkImage(r'..\main\gatherImage\itemConvert.png')[0] > 0.8:
            buy()
        time.sleep(1)

    stopWater = threading.Event()
    t4 = threading.Thread(target=water, args=(stopWater,), daemon=True)
    t3 = threading.Thread(target=walk, args=('s', 24))  #后走时间
    t4.start()
    t3.start()
    t3.join()
    stopWater.set()

    pressKey('w', 0.2)
    click()
    findAndClick(r'..\main\gatherImage\toBack.png', clickTime=0.2)
    click()
    findAndClick(r'..\main\gatherImage\itemConvert.png', clickTime=0.2)


def main():
    for i in range(60*10):
        # 循环耗时: 58.31399178504944+
        start = time.time()
        circulate()
        print('循环耗时:', time.time()-start)
        time.sleep(10)
        print("循环次数:", i + 1)

    time.sleep(3)


if __name__ == '__main__':
    main()