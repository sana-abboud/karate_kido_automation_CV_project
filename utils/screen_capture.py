import numpy as np
from mss import mss

def capture_window(region):
    with mss() as sct:
        screenshot = np.array(sct.grab(region))
        return screenshot
