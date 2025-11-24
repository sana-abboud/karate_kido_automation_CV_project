import cv2
import numpy as np

def detect_lantern(scene, template_path, match_threshold=0.5):
    """
    Detects the best match for a template in a scene using multi-scale template matching.

    Parameters:
        scene (numpy.ndarray): The scene image (BGR format).
        template_path (str): Path to the template image.
        match_threshold (float): Threshold for template matching.

    Returns:
        tuple: The bounding box ((x1, y1), (x2, y2)) of the best match or None if no match is found.
    """
    # Load and preprocess the template
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Template image not found at {template_path}")

    template_edges = cv2.Canny(template, 50, 150)

    # Convert scene to grayscale and detect edges
    scene_gray = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
    scene_edges = cv2.Canny(scene_gray, 50, 150)

    # Multi-scale template matching
    best_match = None
    best_val = -1
    h, w = template_edges.shape

    for scale in np.linspace(0.5, 2.0, 20):  # Resize template at multiple scales
        resized_template = cv2.resize(template_edges, (int(w * scale), int(h * scale)))
        result = cv2.matchTemplate(scene_edges, resized_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > best_val and max_val >= match_threshold:  # Keep track of the best match
            best_val = max_val
            x1, y1 = max_loc
            x2, y2 = x1 + resized_template.shape[1], y1 + resized_template.shape[0]
            best_match = ((x1, y1), (x2, y2))

    # Extend the bottom of the box if needed
    if best_match:
        (x1, y1), (x2, y2) = best_match
        adjustment_factor = 0.2  # Adjust as required
        adjusted_y2 = int(y2 + (y2 - y1) * adjustment_factor)
        best_match = ((x1, y1), (x2, adjusted_y2))

    return best_match



def detect_lantern_with_shape_and_color(scene, template_path):
    """
    Detects objects in a scene using shape and color matching and marks them on the output image.

    Parameters:
        scene_path (str): Path to the scene image.
        template_path (str): Path to the template image.

    Returns:
        int: 1 if found in the right half, -1 if found in the left half, 0 if no detection.
    """
    # Load the scene and lantern template
    # scene = cv2.imread(scene_path, cv2.IMREAD_COLOR)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    if scene is None or template is None:
        raise FileNotFoundError("Scene or template image not found. Check the file paths.")

    # Preprocess the template
    template = cv2.resize(template, (50, 50))  # Resize to standard size for matching
    _, template_binary = cv2.threshold(template, 127, 255, cv2.THRESH_BINARY)  # Binarize
    template_contours, _ = cv2.findContours(template_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(template_contours) == 0:
        raise ValueError("No contours found in the template.")

    template_contour = template_contours[0]  # Use the first contour (assumes only one object)

    # Preprocess the scene
    scene_gray = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
    scene_edges = cv2.Canny(scene_gray, 50, 150)  # Detect edges

    # Detect contours in the scene
    scene_contours, _ = cv2.findContours(scene_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Blank mask for shape matching results
    shape_matching_mask = np.zeros(scene.shape[:2], dtype=np.uint8)

    # Loop through scene contours and match shapes
    for contour in scene_contours:
        area = cv2.contourArea(contour)
        if area > 500:  # Filter small noise
            ret = cv2.matchShapes(template_contour, contour, cv2.CONTOURS_MATCH_I1, 0.0)
            if ret < 0.5:  # Relaxed threshold for shape matching
                cv2.drawContours(shape_matching_mask, [contour], -1, 255, thickness=cv2.FILLED)

    # Step 3: Combine with Color Mask
    # Convert scene to HSV for color filtering
    hsv_scene = cv2.cvtColor(scene, cv2.COLOR_BGR2HSV)

    # Define color range for green lanterns
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])

    # Create color mask
    color_mask = cv2.inRange(hsv_scene, lower_green, upper_green)

    # Combine results
    combined_mask = cv2.bitwise_or(color_mask, shape_matching_mask)

    # Draw results on the scene
    output_scene = scene.copy()

    # Draw contours for Color Mask in blue
    color_contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(output_scene, color_contours, -1, (255, 0, 0), 2)

    # Draw contours for Shape Matching Mask in green
    shape_contours, _ = cv2.findContours(shape_matching_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(output_scene, shape_contours, -1, (0, 255, 0), 2)

    # Analyze the bounding boxes and determine the position
    height, width = scene.shape[:2]
    vertical_midline = width // 2

    found_left = False
    found_right = False

    for contour in shape_contours + color_contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)

        # Only consider meaningful contours
        if area > 500:  # Adjust the area threshold based on the expected size of the lantern
            center_x = x + w // 2

            if center_x < vertical_midline:
                found_left = True
            elif center_x >= vertical_midline:
                found_right = True

    # Decide the return value
    if found_right:
        result = 1
    elif found_left:
        result = -1
    else:
        result = 0

    # Display the output scene with the detection results
    # cv2.imshow("Final Detection", output_scene)


    return result
