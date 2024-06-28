from adafruit_matrixkeypad import Matrix_Keypad
from digitalio import DigitalInOut, Direction, Pull
from modules.encoder_handler import EncoderHandler
from rotaryio import IncrementalEncoder
import board

try:
    from typing import List
except ImportError:
    pass

__version__ = "0.0.1"
__repo__ = "https://github.com/SergiuToporjinschi/KeyPadManager.git"
class Periferics:
    _encButtonBit = 1024

    def __init__(self):
        self._initKeys()
        self._initRotarry()
        self._report = [0, 0]
        self._lastReport = [0, 0]

    def _initKeys(self):
        self._cols = [DigitalInOut(x) for x in (board.GP9, board.GP10, board.GP11, board.GP12, board.GP13)]
        self._rows = [DigitalInOut(x) for x in (board.GP15, board.GP14)]
        values = [
            [1, 2, 4, 8, 16],
            [32, 64, 128, 256, 512],
        ]

        self._keypad = Matrix_Keypad(self._rows, self._cols, values)


    def _initRotarry(self):
        self._encoder = IncrementalEncoder(board.GP18, board.GP17, 2)
        self._encoderButton = DigitalInOut(board.GP16)
        self._encoderButton.direction = Direction.INPUT
        self._encoderButton.pull = Pull.UP

    def update(self):
        self._calculateReport()
        pass

    @property
    def report(self) -> List:
        self._lastReport[0] = self._report[0]
        self._lastReport[1] = self._report[1]
        return self._lastReport

    @property
    def hasReportChanged(self) -> bool:
        return self._report != self._lastReport

    def _calculateReport(self) -> List:
        self._report[1] = self._encoder.position
        self._report[0] = sum(self._keypad.pressed_keys) 
        
        if self._encoderButton.value == False:
            self._report[0] = self._report[0] + self._encButtonBit


    def deinit(self) -> None:
        if self._encoderButton != None and hasattr(self._encoderButton, 'deinit'):
            self._encoderButton.deinit()
        if hasattr(self._encoder, 'deinit'):  
            self._encoder.deinit()
        for pin in self._cols:
            if pin != None and hasattr(pin, 'deinit'):
                pin.deinit()
        for pin in self._rows:
            if pin != None and hasattr(pin, 'deinit'):
                pin.deinit() 

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.deinit()