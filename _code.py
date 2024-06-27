import usb_hid
from usb_device import DeviceController
# from gyro import Gyro
import bitbangio as io
import board
import digitalio
from periferics import ResponseType
import microcontroller
import time
import random
import rotaryio


def handle_out_report(report):
    # Process the OUT report data here 
    print("Received OUT report:", report)


dev = DeviceController()

button = digitalio.DigitalInOut(board.GP2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

buttonEnc = digitalio.DigitalInOut(board.GP16)
buttonEnc.direction = digitalio.Direction.INPUT
buttonEnc.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.GP18, board.GP17, 2)
last_position = encoder.position
def readButtonFromGPODebounced():
   return not button.value

while True:
   position = encoder.position
   if last_position is not None and position != last_position:
      if last_position > position:
         print(position, "CCW", abs(last_position - position))
      else:
         print(position, "CW", abs(last_position - position))
  

   if buttonEnc.value == False:
      print("Button pressed")


   # angleXZ,angleYZ, acc, gyro, temp = devices[0].read(ResponseType.RAW)
      # print(f"XZ: {angleXZ:03.0f}, YZ: {angleYZ:03.0f}, Acc-x: {acc[0]:03.4f}, Acc-y: {acc[1]:03.4f}, Acc-z: {acc[2]:03.4f}, Gyro-x: {gyro[0]:03.4f}, Gyro-y: {gyro[1]:03.4f}, Gyro-z: {gyro[2]:03.4f}")
   time.sleep(0.1)
   # led_report = dev.readReport()
   
   dev.send(readButtonFromGPODebounced(), last_position - position)

   last_position = position