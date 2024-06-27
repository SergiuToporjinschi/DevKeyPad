import time
import board
from adafruit_matrixkeypad import Matrix_Keypad
from digitalio import DigitalInOut
try:
    from typing import List
    from digitalio import DigitalInOut
except ImportError:
    pass

cols = [DigitalInOut(x) for x in (board.GP9, board.GP10, board.GP11, board.GP12, board.GP13)]
rows = [DigitalInOut(x) for x in (board.GP15, board.GP14)]
values = [
    ["11", "12", "13", "14", "15"],
    ["21", "22", "23", "24", "25"],
]

class EventKeyPadMatrix(Matrix_Keypad):
    keys = []   
    _last_pressed_keys = []
    def __init__(self, row_pins, col_pins, vals):
        super().__init__(row_pins, col_pins, vals)
        self._last_pressed_keys = None

    @property
    def keysVals(self) -> List:
        kp = self.pressed_keys
        if self._last_pressed_keys != kp:
            self._last_pressed_keys = kp
            return self._last_pressed_keys
    
    @property
    def keysChanged(self) -> bool:
        return 

keypad = EventKeyPadMatrix(rows, cols, values)
while True:
    print("Pressed: ", keypad.keysVals)
    time.sleep(0.01)