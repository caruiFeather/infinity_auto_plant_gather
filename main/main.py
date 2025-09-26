import time
import threading
import function
import gather
from pynput.keyboard import Listener, Key


def main():
    # 停止事件，按End键结束程序
    stop_event = threading.Event()

    def on_press(key):
        if key == Key.end:
            stop_event.set()
            return False
    while function.checkImage(r"..\main\gatherImage\pearl.png")[0] < 0.9:
        time.sleep(1)

    gather_thread = threading.Thread(target=gather.main, daemon=True)
    gather_thread.start()

    # 设置键盘监听器
    with Listener(on_press=on_press) as listener:
        stop_event.wait()
        listener.stop()

    function.releaseAllKeys()


if __name__ == '__main__':
    main()
