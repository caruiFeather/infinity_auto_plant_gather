import numpy as np
import cv2 as cv

def show(img):
    cv.imshow('img', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == '__main__':
    img = cv.imread(r'..\main\gatherImage\pearl.png')
    show(img)
