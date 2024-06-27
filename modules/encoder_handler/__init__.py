from rotaryio import IncrementalEncoder
import microcontroller
import digitalio
from adafruit_debouncer import Button

class EncoderHandler():
    _lastPosition = 0
    def __init__(self, dt_pin, clk_pin, divisor:int = 4, button_pin: microcontroller.Pin = None) -> None:
        self._enc = IncrementalEncoder(dt_pin, clk_pin, divisor)
        if button_pin is not None:
            self._button = button_pin
            self._button.direction = digitalio.Direction.INPUT
            self._button.pull = digitalio.Pull.UP
            self._btnDeb = Button(self._button)

    @property
    def relativePosition(self):
        return self._enc.position - self._lastPosition
    
    @property
    def position(self):
        self._lastPosition = self._enc.position
        return self._enc.position

    @property
    def hasChanged(self) -> bool:
        return self._lastPosition != self._enc.position

    @property
    def isCW(self) -> bool:
        return self._enc.position > self._lastPosition

    @property
    def isCCW(self) -> bool:
        return not self.isCW
    
    def readButton(self) -> bool:
        pass

    def deinit(self) -> None:
        self._enc.deinit()
    
    def __enter__(self) -> IncrementalEncoder:
        return self._enc.__enter__()
    
    def __exit__(self) -> None:
        self._enc.__exit__()