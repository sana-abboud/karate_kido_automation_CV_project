import cv2
import numpy as np

def character_detect(frame, template_path, threshold):
    template = cv2.imread(template_path, 0)
    template_w, template_h = template.shape[::-1]

    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        top_left = max_loc
        bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
        return (top_left, bottom_right)
    return None
