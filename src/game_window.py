import os
import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
def activate_game_window_by_image(image_path):
    target_image = cv2.imread(image_path, 0)
    windows = gw.getWindowsWithTitle('')
    for window in windows:
        if window.isMinimized or not window.visible:
            continue
        try:
            screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
            screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

            result = cv2.matchTemplate(screenshot_gray, target_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)

            if max_val > 0.9:
                windows = [w for w in gw.getAllWindows() if "Play games, WIN REAL REWARDS!" in w.title]  # Filter for the correct game window
                window = windows[0]  # Return the first matching window
                window.show()  # Show the window if it's hidden
                window.activate()
                print(f"Game window activated: {window.title}")
                # print(f' {"top": window.top, "left": window.left, "width": window.width, "height": window.height}')
                return {"top": window.top, "left": window.left, "width": window.width, "height": window.height}
        except Exception as e:
            print(f"Error activating window: {e}")
    return None
