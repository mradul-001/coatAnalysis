import cv2
import numpy as np
import matplotlib.pyplot as plt

def removeNoise(t_img: np.ndarray, contours: list) -> np.ndarray:
    
    if not contours:
        return t_img
    
    areas = [cv2.contourArea(c) for c in contours]
    avg_area = sum(areas) / len(areas)
    area_threshold = 0.5 * avg_area
    good_contours = [c for c in contours if cv2.contourArea(c) > area_threshold]
    final_img = np.zeros_like(t_img)
    
    cv2.drawContours(
        final_img, good_contours, -1, (255, 255, 255), thickness=cv2.FILLED
    )

    plt.imsave('final.png', final_img)
    return final_img
