import numpy as np


def calculateWidth(final_img: np.ndarray, scale: float) -> tuple[float, float]:
    final_img = final_img.astype(int)
    thicknesses = []

    for col in range(final_img.shape[1]):
        white_found = False
        first = None
        last = None
        for i in range(final_img.shape[0]):
            if final_img[i, col] == 255 and not white_found:
                white_found = True
                first = i
                last = i
            elif final_img[i, col] == 255:
                last = i
        if white_found and first is not None and last is not None:
            thicknesses.append(last - first)

    if not thicknesses:
        return 0.0, 0.0

    avg_thickness = np.mean(thicknesses) * scale
    std_dev = np.std(thicknesses) * scale

    return avg_thickness, std_dev
