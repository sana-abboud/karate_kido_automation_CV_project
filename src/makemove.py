from pynput.keyboard import Key, Controller
import time

# Initialize keyboard controller
keyboard = Controller()

key_press = {
    'left': Key.left,
    'right': Key.right
}

def make_a_move(direction, t=0.4):
    keyboard.press(key_press[direction])
    time.sleep(t)
    keyboard.release(key_press[direction])
