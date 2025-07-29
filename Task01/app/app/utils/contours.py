import cv2
import matplotlib.pyplot as plt

def findContours(img):
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    plt.imsave("contour.png", contour_img)
    return contour_img, contours