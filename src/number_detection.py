import cv2
import pytesseract
import numpy as np
import re

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Path to the tessdata directory
tessdata_dir_config = r'--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'

def erode_image(image):
    kernel = np.ones((4, 4), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

def extract_number_from_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, (20, 100, 100), (30, 255, 255)) 
    isolated_text = cv2.bitwise_and(image, image, mask=yellow_mask)

    gray = cv2.cvtColor(isolated_text, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  
    # Run Tesseract OCR
    config = rf'--psm 6 -c tessedit_char_whitelist=234x {tessdata_dir_config}'
    ocr_result = pytesseract.image_to_string(binary, config=config)
    boxes = pytesseract.image_to_boxes(binary, config=config)
    print("First OCR Result:", ocr_result.strip())

    match = re.search(r'x(\d)', ocr_result)
    if match:
        return match.group(1), boxes

    print("Applying erosion as fallback...")
    eroded_image = erode_image(binary)
    ocr_result = pytesseract.image_to_string(eroded_image, config=config)
    boxes = pytesseract.image_to_boxes(eroded_image, config=config)
    print("Detected Number:", ocr_result.strip())

    match = re.search(r'x(\d)', ocr_result)
    if match:
        return match.group(1), boxes
    else:
        return ocr_result.strip(), boxes

    return 0, None
