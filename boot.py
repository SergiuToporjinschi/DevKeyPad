#------------------ boot with writtable 
import board
import digitalio
import storage
# For Gemma M0, Trinket M0, Metro M0/M4 Express, ItsyBitsy M0/M4 Express
switch = digitalio.DigitalInOut(board.GP2)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If the switch pin is connected to ground CircuitPython can write to the drive
# storage.remount("/", readonly=switch.value)

#--------------------------- USB
import supervisor
supervisor.set_usb_identification(manufacturer="Me&Co",product="Development key pad", vid=0x6001, pid=0x1000)

#--------------------------- USB HID
import usb_hid
import usb_midi
from modules.usb_device import DeviceController

usb_midi.disable() 
usb_hid.set_interface_name("Development key pad")
device = DeviceController.buildDeviceDescriptor()


usb_hid.enable((device,))
  