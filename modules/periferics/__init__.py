from adafruit_matrixkeypad import Matrix_Keypad
from digitalio import DigitalInOut, Direction, Pull
from modules.encoder_handler import EncoderHandler
from rotaryio import IncrementalEncoder
import board
import util
try:
    from typing import List
except ImportError:
    pass

__version__ = "0.0.1"
__repo__ = "https://github.com/SergiuToporjinschi/KeyPadManager.git"

log = util.getLoggerFor('periferics')
class Periferics:
    _encButtonBit = 1024

    _keys_colGPIOs = (board.GP9, board.GP10, board.GP11, board.GP12, board.GP13)
    _keys_rowGPIOs = (board.GP15, board.GP14)
    _keys_values = [
                [1, 2, 4, 8, 16],
                [32, 64, 128, 256, 512]]
    
    _rotarry_clkGPIO = board.GP18
    _rotarry_dtGPIO = board.GP17
    _rotarry_swGPIO = board.GP16
    _rotarry_divisor = 2
   
    def __init__(self):
        log.info("Initialize periferics")
        self._initKeys()
        self._initRotarry()
        self._report = [0, 0]
        self._lastReport = [0, 0]

    def _initKeys(self):
        log.debug(f"Initialize keys \n\t\t\t Cols: {self._keys_colGPIOs}\n\t\t\t Rows: {self._keys_rowGPIOs}\n\t\t\t Values: {self._keys_values}")

        self._cols = [DigitalInOut(x) for x in self._keys_colGPIOs]
        self._rows = [DigitalInOut(x) for x in self._keys_rowGPIOs]
        self._keypad = Matrix_Keypad(self._rows, self._cols, self._keys_values)


    def _initRotarry(self):
        log.debug(f"Initialize encoder [clk: {self._rotarry_clkGPIO}; dt: {self._rotarry_dtGPIO}; Divisor: {self._rotarry_divisor}]")
        self._encoder = IncrementalEncoder(self._rotarry_clkGPIO, self._rotarry_dtGPIO, self._rotarry_divisor)

        log.debug(f"Initialize encoder button [sw: {self._rotarry_swGPIO}]")
        self._encoderButton = DigitalInOut(self._rotarry_swGPIO)
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
        log.info("Deinitialize encoder button")
        if self._encoderButton != None and hasattr(self._encoderButton, 'deinit'):
            self._encoderButton.deinit()
        
        log.debug("Deinitialize encoder")
        if hasattr(self._encoder, 'deinit'):  
            self._encoder.deinit()

        log.debug("Deinitialize column GPIOs")
        for pin in self._cols:
            if pin != None and hasattr(pin, 'deinit'):
                pin.deinit()

        log.debug("Deinitialize row GPIOs")
        for pin in self._rows:
            if pin != None and hasattr(pin, 'deinit'):
                pin.deinit() 

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.deinit()