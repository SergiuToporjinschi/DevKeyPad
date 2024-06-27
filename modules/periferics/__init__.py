from adafruit_matrixkeypad import Matrix_Keypad
from digitalio import DigitalInOut
from modules.encoder_handler import EncoderHandler
from rotaryio import IncrementalEncoder
import board
__version__ = "0.0.1"
__repo__ = "https://github.com/SergiuToporjinschi/KeyPadManager.git"
class Periferics:
    _encButtonBit = 1024

    def __init__(self):
        self._initKeys()
        self._initRotarry()
        self._report = None

        pass

    def _initKeys(self):
        self._cols = [DigitalInOut(x) for x in (board.GP9, board.GP10, board.GP11, board.GP12, board.GP13)]
        self._rows = [DigitalInOut(x) for x in (board.GP15, board.GP14)]
        values = [
            [1, 2, 4, 8, 16],
            [32, 64, 128, 256, 512],
        ]

        self._keypad = Matrix_Keypad(self._rows, self._cols, values)

        pass

    def _initRotarry(self):
        self._encoder = IncrementalEncoder(board.GP18, board.GP17, 2)
        # self._encoder = EncoderHandler(board.GP18, board.GP17, 2)
        pass

    def update(self):
        # self._keypad.pressed_keys 
        # self._encoder.position 
        pass

    def deinit(self) -> None:
        if hasattr(self._encoder, 'deinit'):  
            self._encoder.deinit()
        for pin in self._cols:
            if pin != None and hasattr(pin, 'deinit'):
                pin.deinit()
        for pin in self._rows:
            if pin != None and hasattr(pin, 'deinit'):
                pin.deinit() 
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:

        self.deinit()
        pass 