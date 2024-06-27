import asyncio
import board
import countio
import time
from modules.usb_device import DeviceController

import board
import digitalio

# button = digitalio.DigitalInOut(board.GP2)
# button.direction = digitalio.Direction.INPUT
# button.pull = digitalio.Pull.UP


# from adafruit_debouncer import Button
# button = digitalio.DigitalInOut(board.GP2)
# button.direction = digitalio.Direction.INPUT
# button.pull = digitalio.Pull.UP

# from modules.encoder_handler import EncoderHandler

# encoder = EncoderHandler(board.GP18, board.GP17, 2)
#sssaaass
# from digitalio import DigitalInOut
# from adafruit_matrixkeypad import Matrix_Keypad
# cols = [DigitalInOut(x) for x in (board.GP9, board.GP10, board.GP11, board.GP12, board.GP13)]
# rows = [DigitalInOut(x) for x in (board.GP15, board.GP14)]
# values = [
#     [1, 2, 4, 8, 16],
#     [32, 64, 128, 256, 512],
# ]
# # async def updateButton():
# #     print ("updateButton started", btn)
# #     while True:
# #         btn.update()
# #         await asyncio.sleep(0)

# keypad = Matrix_Keypad(rows, cols, values)

# async def sendToUSB():
#     dev = DeviceController()
#     last = keypad.pressed_keys
#     total = 0
#     while True:
#         ks = keypad.pressed_keys
#         total = sum(ks)
#         if ks != last:
#             dev.send(total, encoder.relativePosition)
#             last = keypad.pressed_keys
#         if encoder.hasChanged:
#             dev.send(total, encoder.relativePosition)
#         await asyncio.sleep(0)
#     pass

# async def updateScreen():
#     last = keypad.pressed_keys
#     total = 0
#     while True:
#         ks = keypad.pressed_keys
#         total = sum(ks)
#         if ks != last:
#             print("Button pressed", ks, total)
#             last = keypad.pressed_keys
#         if encoder.hasChanged:
#             print("encVal", encoder.relativePosition,  encoder.position)
#         await asyncio.sleep(0)

# async def main():
#     await asyncio.gather(
#         asyncio.create_task(sendToUSB())
#         # asyncio.create_task(updateScreen()), 
#     ) # Wait for both tasks to finish.  
#     # await asyncio.gather(asyncio.create_task(updateScreen(deb))) # Wait for both tasks to finish.

# asyncio.run(main())  
from modules.periferics import Periferics

with Periferics() as per:
    while True:
        per.update()


