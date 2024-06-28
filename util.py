import adafruit_logging as logging
import os
import sys
import storage


def getLoggerFor(name):
    """
    Returns a logger for the given name. 
       The logger is configured based on the configuration in the environment variables.
    """
    print("")
    log = logging.getLogger(name)
    if os.getenv(f"log.{name}.file") and not storage.getmount("/").readonly:
        log.addHandler(DevLogFileHandler(getLogFolder() + os.getenv(f"log.{name}.file"), maxBytes=1024*1024, backupCount=5))

    else:
        log.addHandler(DevLogHandler())

    log.setLevel(_getLogLevel(name))
    return log

def _getLogLevel(name):
    for level_value, level_name in logging.LEVELS:
        if level_name == os.getenv(f"log.{name}.level"):
            return level_value
    return 0  

class DevLogFileHandler(logging.RotatingFileHandler):
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0):
        super().__init__(filename, mode, maxBytes, backupCount)
    
    def format(self, record: logging._LogRecord) -> str:
        return f"{record.created:<0.3f}: [{record.name}]: {record.levelname} - {record.msg}\n"

class DevLogHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(sys.stderr)

    def format(self, record: logging._LogRecord) -> str:
        return f"{record.created:<0.3f} [{record.name}]: {record.levelname} - {record.msg}"


def isPushToReadOnly() -> bool:
    import board
    import digitalio 
    
    commonGIOno = os.getenv("boot.readOnly.GPIO.common")
    sw1GIOno = os.getenv("boot.readOnly.GPIO.switch1")
    sw2GIOno = os.getenv("boot.readOnly.GPIO.switch2")

    colSwt1 = digitalio.DigitalInOut(getattr(board, f"GP{sw1GIOno}"))
    colSwt1.direction = digitalio.Direction.INPUT
    colSwt1.pull = digitalio.Pull.UP

    colSwt2 = digitalio.DigitalInOut(getattr(board, f"GP{sw2GIOno}"))
    colSwt2.direction = digitalio.Direction.INPUT
    colSwt2.pull = digitalio.Pull.UP

    rowSwt = digitalio.DigitalInOut(getattr(board, f"GP{commonGIOno}"))
    rowSwt.direction = digitalio.Direction.OUTPUT
    rowSwt.value = False

    result = colSwt2.value and colSwt1.value

    colSwt1.deinit()
    colSwt2.deinit()
    rowSwt.deinit()

    return result

def path_exists(path):
    try:
        os.stat(path)
        return True
    except OSError:
        return False

def getLogFolder():
    result = "/"
    if os.getenv(f"log.folder"):
        if not path_exists(os.getenv(f"log.folder")):
            os.mkdir(os.getenv(f"log.folder"))
        result = os.getenv(f"log.folder")
    
    return result