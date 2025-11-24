import cv2

def crop_roi(img, match, match_type, root_w=100, padding_x=25, padding_y=10):
    """
    Calculate and crop the region of interest (ROI) based on the match.

    Parameters:
        img: Original image.
        match: Coordinates of the matched template ((top_left, bottom_right)).
        match_type: Identifier for match1 or match2 to handle them differently.
        root_w: Additional width to include in ROI.
        padding_x: Horizontal padding.
        padding_y: Vertical padding.

    Returns:
        roi (cropped image), roi_top_left, roi_bottom_right
    """
    if not match:
        return None, None, None

    top_left, bottom_right = match
    ch_h = bottom_right[1] - top_left[1]
    ch_w = bottom_right[0] - top_left[0]

    # Adjust ROI based on match type (match_type)
    if match_type == "match1":
        roi_top_left = (top_left[0] - padding_x, top_left[1] - ch_h - padding_y - 5)
        roi_bottom_right = (bottom_right[0] + ch_w + root_w + padding_x, bottom_right[1] - ch_h - padding_y)
    elif match_type == "match2":
        roi_top_left = (top_left[0] - ch_w - root_w - padding_x, top_left[1] - ch_h - padding_y)
        roi_bottom_right = (bottom_right[0] + padding_x, bottom_right[1] - ch_h - padding_y)
    else:
        raise ValueError("Unknown match type")

    # Ensure ROI is within image bounds
    roi_top_left = (max(0, roi_top_left[0]), max(0, roi_top_left[1]))
    roi_bottom_right = (min(img.shape[1], roi_bottom_right[0]), min(img.shape[0], roi_bottom_right[1]))

    # Crop the ROI
    roi = img[roi_top_left[1]:roi_bottom_right[1], roi_top_left[0]:roi_bottom_right[0]]
    roi=cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
    return roi, roi_top_left, roi_bottom_right