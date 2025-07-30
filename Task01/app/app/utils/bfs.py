import numpy as np
from collections import deque

def region_growing_adaptive(image: np.ndarray, seeds: list[tuple], threshold: int) -> np.ndarray:
    """
    Performs region growing segmentation using BFS with an adaptive threshold
    from multiple seed points.

    Args:
        image (np.ndarray): The input grayscale image as a NumPy array.
        seeds (list[tuple]): A list of (y, x) tuples for the starting seed points.
        threshold (int): The intensity difference threshold.

    Returns:
        np.ndarray: A binary mask of the segmented region.
    """
    if image is None:
        return None
    
    if not seeds:
        print("Error: No seed points provided.")
        return np.zeros_like(image, dtype=np.uint8)

    height, width = image.shape
    segmented_mask = np.zeros_like(image, dtype=np.uint8)
    queue = deque()
    
    region_intensity_sum = 0.0
    region_pixel_count = 0

    # --- Initialization from all seed points ---
    for seed_y, seed_x in seeds:
        if not (0 <= seed_y < height and 0 <= seed_x < width):
            print(f"Warning: Seed point ({seed_y}, {seed_x}) is outside image bounds. Skipping.")
            continue
        
        if segmented_mask[seed_y, seed_x] == 0:
            queue.append((seed_y, seed_x))
            segmented_mask[seed_y, seed_x] = 255
            region_intensity_sum += float(image[seed_y, seed_x])
            region_pixel_count += 1
    
    if region_pixel_count == 0:
        print("Error: All provided seed points were invalid or out of bounds.")
        return np.zeros_like(image, dtype=np.uint8)

    # --- Main BFS Loop (this part remains unchanged) ---
    while queue:
        current_y, current_x = queue.popleft()
        current_average_intensity = region_intensity_sum / region_pixel_count

        for y_offset in [-1, 0, 1]:
            for x_offset in [-1, 0, 1]:
                if y_offset == 0 and x_offset == 0:
                    continue

                neighbor_y, neighbor_x = current_y + y_offset, current_x + x_offset

                if 0 <= neighbor_y < height and 0 <= neighbor_x < width:
                    if segmented_mask[neighbor_y, neighbor_x] == 0:
                        neighbor_intensity = float(image[neighbor_y, neighbor_x])
                        if abs(neighbor_intensity - current_average_intensity) <= threshold:
                            segmented_mask[neighbor_y, neighbor_x] = 255
                            queue.append((neighbor_y, neighbor_x))
                            region_intensity_sum += neighbor_intensity
                            region_pixel_count += 1
                            
    return segmented_mask
