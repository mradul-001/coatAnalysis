import cv2
import matplotlib.pyplot as plt

def otsuBinarization(img):
    # img = cv2.medianBlur(img, 5)
    img = cv2.medianBlur(img, 3)
    plt.imsave("blurred.png", img)
    ret, t_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    plt.imsave("otsu.png", t_img)
    return t_img


"""
0.png => median blur 3
00.png
"""