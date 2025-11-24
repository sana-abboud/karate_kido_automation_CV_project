import cv2
import numpy as np

# def detect_wood_objects(frame, wood_templates, threshold):
#     detections = []
#     for template in wood_templates:
#         wood_template = cv2.imread(template, 0)
#         wood_w, wood_h = wood_template.shape[::-1]

#         result = cv2.matchTemplate(frame, wood_template, cv2.TM_CCOEFF_NORMED)
#         locations = np.where(result >= threshold)
#         for pt in zip(*locations[::-1]):
#             detections.append((pt, (pt[0] + wood_w, pt[1] + wood_h)))
#     return detections


def detect_wood_objects(frame, wood_templates, threshold):
    """
    Detect wood objects in a frame using template matching and divide the frame
    vertically into left and right halves.

    Parameters:
        frame: Grayscale frame to search in.
        wood_templates: List of paths to template images.
        threshold: Matching threshold.

    Returns:
        Tuple of (detection, flag), where detection is (top_left, bottom_right) and flag is:
        -1 for left wood, 1 for right wood, 0 for no match.
    """
    frame_center_x = frame.shape[1] // 2  # X-coordinate of the vertical center of the frame

    for template_path in wood_templates:
        wood_template = cv2.imread(template_path, 0)  # Read in grayscale
        height, width = wood_template.shape[:2]
        new_width = int(0.25 * width)  # Multiply width by 0.2 and cast to int
        new_height = int(0.25 * height)  # Multiply height by 0.2 and cast to int

        # Resize template
        wood_template = cv2.resize(wood_template, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        if wood_template is None:
            raise FileNotFoundError(f"Template not found at {template_path}")

        wood_w, wood_h = wood_template.shape[::-1]
        print(f"Template size: {wood_w}x{wood_h}")  # Debug: Check template size

        result = cv2.matchTemplate(frame, wood_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        print(f"Max value: {max_val}, Location: {max_loc}")  # Debug: Check match quality

        if max_val >= threshold:
            # Determine detection location
            top_left = max_loc
            bottom_right = (top_left[0] + wood_w, top_left[1] + wood_h)

            # Check if the detection is in the left or right half
            if top_left[0] + wood_w // 2 < frame_center_x:
                print(f"Wood detected on left side: {top_left} to {bottom_right}")
                return (top_left, bottom_right), -1  # Left side
            else:
                print(f"Wood detected on right side: {top_left} to {bottom_right}")
                return (top_left, bottom_right), 1  # Right side

    # No match found
    print("No wood detected.")
    return None, 0

