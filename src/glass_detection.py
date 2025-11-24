import cv2
import numpy as np

def detect_glass(image, min_area=500):
    """
    Detects glass objects in an image based on color detection in the HSV space.

    Parameters:
        image (numpy.ndarray): The input frame/image (BGR format) to process.
        min_area (int): Minimum area threshold to filter small detections.

    Returns:
        tuple: (top_left, bottom_right, 1) for the first detected glass object,
               or (None, None, 0) if no glass object is detected.
    """
    if image is None:
        raise ValueError("Error: Input image is None.")

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for bluish/cyan color (adjust based on glass color)
    lower_blue = np.array([85, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Create a mask to isolate blue regions
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Clean up the mask using morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Fill gaps
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # Remove noise

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:  # Filter out small detections
            x, y, w, h = cv2.boundingRect(contour)
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            return top_left, bottom_right, 1  # Return the first detection

    return None, None, 0  # No glass object detected

