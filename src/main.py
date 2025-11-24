import cv2
import numpy as np
from src.config import TEMPLATES, MATCH_THRESHOLD, WOOD_THRESHOLD, LANTERN_THRESHOLD, GLASS_MIN_AREA
from src.game_window import activate_game_window_by_image
from src.character_detect import character_detect
from src.wood_detection import detect_wood_objects
from src.lantern_detection import detect_lantern, detect_lantern_with_shape_and_color
from src.glass_detection import detect_glass
from src.number_detection import extract_number_from_image
from utils.screen_capture import capture_window
from utils.preprocessing import crop_roi
from src.makemove import make_a_move
from src.decisions import decide_action

roi_h, roi_w = 0,0
root_w=200 # need detect 

# Activate game window
window_region = activate_game_window_by_image(TEMPLATES["game"])
if not window_region:
    print("Game window not found!")
    exit()

# Load wood templates
wood_templates = TEMPLATES["wood"]

# Load lantern templates
lantern_template_path = TEMPLATES["lantern"]
# Main loop
first_run=True
decisions='left'
while True:
    # Capture game window
    # window_region = activate_game_window_by_image(TEMPLATES["game"])
    screenshot = capture_window(window_region)
    gray_frame = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Match character templates
    match1 = character_detect(gray_frame, TEMPLATES["character1"], MATCH_THRESHOLD)
    match2 = character_detect(gray_frame, TEMPLATES["character2"], MATCH_THRESHOLD)

    # Draw matches for characters
    if match1:
        roi, roi_top_left, roi_bottom_right = crop_roi(gray_frame, match1, "match1")
        cv2.rectangle(screenshot, match1[0], match1[1], (0, 255, 0), 2)
    if match2:
        roi, roi_top_left, roi_bottom_right = crop_roi(gray_frame, match2, "match2" )
        cv2.rectangle(screenshot, match2[0], match2[1], (0, 255, 0), 2)

    if roi is not None:
        print(roi.shape)
        cv2.imshow('roi',roi)
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    else:
        raise ValueError("ROI is None. Ensure template matching returned valid matches.")


    # Detect wood objects
    detection, wood_flag = detect_wood_objects(roi_gray, wood_templates, 0.78)
    if detection:
        top_left, bottom_right = detection
        print(f"Detection at {top_left} to {bottom_right}, flag: {wood_flag}")
        cv2.rectangle(roi, top_left, bottom_right, (0, 255, 0) if wood_flag == -1 else (255, 0, 0), 2)
    else:
        print("No match found, flag: 0")


    # Detect lanterns
    result = detect_lantern_with_shape_and_color(roi, lantern_template_path)
    if result == 1:
        print("Object detected in the right half of the scene.")
    elif result == -1:
        print("Object detected in the left half of the scene.")
    else:
        print("No object detected.")
        

    # Detect glass
    top_left, bottom_right, detected = detect_glass(roi)
    if detected:
        print(f"Glass detected at: Top Left {top_left}, Bottom Right {bottom_right}")
        cv2.rectangle(roi, top_left, bottom_right, (168, 10, 200), 3)
    else:
        print("No glass detected.")


    if first_run:
            decisions,steps=decide_action(wood_flag,0,detected,result,decisions)
            print("+++++++++++++++++++++")
            print(f"GO TO THE {decisions}")
            print("+++++++++++++++++++++")
    else:
            decisions,steps=decide_action(wood_flag,0,detected,result,decisions)
            print("+++++++++++++++++++++")
            print(f"GO TO THE {decisions}")
            print("+++++++++++++++++++++")
    make_a_move(decisions)
    #Detect numbers
    # number , boxes = extract_number_from_image(roi )
    # imgH,imgW,_=screenshot.shape
    # number,boxes = extract_number_from_image(roi)
    # for box in boxes.splitlines():
    #     box=box.split()
    #     x,y,w,h=int(box[1]),int(box[2]),int(box[3]),int(box[4])
    #     cv2.rectangle(screenshot,(x,imgH-y),(w,imgH-h),(100,0,100),2)
    
    
    # Display results
    cv2.imshow("Game Automation", screenshot)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
