import time
import usb_hid
from adafruit_hid import find_device

class DeviceController:
    _reportLength = 3
    _controller = None
    _report = None
    _lastReport = None
    @staticmethod
    def buildDeviceDescriptor() -> usb_hid.Device:
        report_id = 5
        return usb_hid.Device(
            report_descriptor=bytes((
                0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
                0x09, 0x05,        # Usage (Game Pad)
                0xA1, 0x01,        # Collection (Application)
                
                0x85, report_id,   # Report ID (5)
                0xA1, 0x00,        # Collection (Physical)

                # Button
                0x05, 0x09,        # Usage Page (Button)
                0x19, 0x01,        # Usage Minimum (Button 1)
                0x29, 0x0B,        # Usage Maximum (Button 11)
                0x15, 0x00,        # Logical Minimum (0)
                0x25, 0x01,        # Logical Maximum (1)
                0x75, 0x01,        # Report Size (1)
                0x95, 0x0B,        # Report Count (11)
                0x81, 0x02,        # Input (Data,Var,Abs)

                # Padding
                0x75, 0x05,        # Report Size (5)
                0x95, 0x01,        # Report Count (1)
                0x81, 0x03,        # Input (Cnst,Var,Abs)

                # Rotary encoder
                0x05, 0x01,        # Usage Page (Generic Desktop Controls)
                0x09, 0x38,        # Usage (Wheel)
                0x15, 0x81,        # Logical Minimum (-127)
                0x25, 0x7F,        # Logical Maximum (127)
                0x75, 0x08,        # Report Size (8)
                0x95, 0x01,        # Report Count (1)
                0x81, 0x06,        # Input (Data,Var,Rel)

                0xC0,              # End Collection
                0xC0               # End Collection 

            )),
            usage_page=0x01,           # Generic Desktop Control
            usage=0x05,                # Gamepad
            report_ids=(report_id,),   # Descriptor uses report ID 5.
            in_report_lengths=(DeviceController._reportLength,),    # This gamepad sends 1 bytes in its report.
            out_report_lengths=(DeviceController._reportLength,),   # It does not receive any reports.
        )
    
    def __init__(self) -> None:
        self._controller = find_device(usb_hid.devices, usage_page=0x01, usage=0x05)
        
        if self._controller is None:
            raise ValueError("No device found (check boot.py).")
        self._report = bytearray(self._reportLength)

        # Do a no-op to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.send([0, 0])
        except OSError:
            time.sleep(1)
            self.send([0, 0])
            
    def readReport(self):
        val = self._controller.get_last_received_report(5)
        if val is not None:
            print("**********************" + val)

    def send(self, list: int[2]):
        rotary_val = list[1]
        button = list[0]
        
        if not (-127 <= rotary_val <= 127):
            raise ValueError("rotary value must be between -127 and 127")
        
        if not (0 <= button <= 2047): 
            raise ValueError("Too many buttons")
        
        bytess = button.to_bytes(3, 'little')

        self._report[0] = bytess[0]
        self._report[1] = bytess[1]
        # self._report[2] = bytess[2]
        #convert rotary_val to little binary signed 
        self._report[2] = rotary_val.to_bytes(1, 'little', signed=True)[0]
        

        # self._report[2] = 0x00
        print(' '.join(f"{byte:08b}" for byte in self._report), list)
        self._controller.send_report(self._report)
        self._lastReport = self._report

    # def _convertToBinary(self, val: int[]) -> bytes:
    #     return val.to_bytes(2, 'little')


