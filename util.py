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
        log.addHandler(DevLogFileHandler(os.getenv(f"log.{name}.file"), maxBytes=1024, backupCount=5))
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
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False):
        super().__init__(filename, mode, maxBytes, backupCount, encoding, delay)
    
    def format(self, record: logging._LogRecord) -> str:
        return f"{record.created:<0.3f}: [{record.name}]: {record.levelname} - {record.msg}"

class DevLogHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(sys.stderr)

    def format(self, record: logging._LogRecord) -> str:
        return f"{record.created:<0.3f} [{record.name}]: {record.levelname} - {record.msg}"