import asyncio
from modules.usb_device import DeviceController
from modules.periferics import Periferics
import util
import os

log = util.getLoggerFor('code')

updatePerifericsPause = float(os.getenv("code.refreshPause.updatePeriferics"))
updateUSBPause = float(os.getenv("code.refreshPause.updateUSB"))

async def updateScreen(per: Periferics):
    log.debug('starting updateScreen')
    while True:
        if per.hasReportChanged:
            rep = per.report 
            print(' '.join(f"{byte:08b}" for byte in rep), rep)
        await asyncio.sleep(0)     

async def updatePeriferics(per: Periferics):
    log.debug('starting updatePeriferics')
    while True:
        per.update()
        await asyncio.sleep(updatePerifericsPause)   

async def updateUSB(per: Periferics): 
    log.debug('starting updateUSB')
    dev = DeviceController()
   
    while True:
        if per.hasReportChanged:
            dev.send(per.report)
        await asyncio.sleep(updateUSBPause)   


async def main():
    with Periferics() as per:
        await asyncio.gather(
            asyncio.create_task(updatePeriferics(per)),
            #asyncio.create_task(updateScreen(per)), 
            asyncio.create_task(updateUSB(per)), 
        ) 

log.info("Code started")
asyncio.run(main())   
