#------------------ boot with writtable 
import board
import digitalio
import util

log = util.getLoggerFor('boot')

log.info("Boot sequence started")

# For Gemma M0, Trinket M0, Metro M0/M4 Express, ItsyBitsy M0/M4 Express
switch = digitalio.DigitalInOut(board.GP2)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If the switch pin is connected to ground CircuitPython can write to the drive
# storage.remount("/", readonly=switch.value)

#--------------------------- USB
import supervisor

manu = "Me&Co"
prod = "Development key pad"
_VID = 0x6001
_PID = 0x1000
interface_name = "Development key pad"



supervisor.set_usb_identification(manufacturer=manu,product=prod, vid=_VID, pid=_PID)
log.debug(f"USB identification set [{manu}, {prod}, {_VID}, {_PID}]")

#--------------------------- USB HID
log.info("Setting USB HID")
import usb_hid
import usb_midi


usb_midi.disable() 
log.debug("USB MIDI disabled")

usb_hid.set_interface_name(interface_name)
log.debug(f"Interface name set {interface_name} ")

from modules.usb_device import DeviceController
device = DeviceController.buildDeviceDescriptor()

usb_hid.enable((device,))
log.debug("USB HID enabled")
log.debug("END")