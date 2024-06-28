import asyncio
from modules.usb_device import DeviceController
from modules.periferics import Periferics

print("\n")

async def updateScreen(per: Periferics):
    print('starting updateScreen')
    while True:
        if per.hasReportChanged:
            rep = per.report 
            print(' '.join(f"{byte:08b}" for byte in rep), rep)
        await asyncio.sleep(0)     

async def updatePeriferics(per: Periferics):
    print('starting updatePeriferics')
    while True:
        per.update()
        await asyncio.sleep(0)   

async def updateUSB(per: Periferics): 
    dev = DeviceController()
   
    print('starting updateUSB')
    while True:
        if per.hasReportChanged:
            dev.send(per.report)
        await asyncio.sleep(0)   


async def main():
    with Periferics() as per:
        await asyncio.gather(
            asyncio.create_task(updatePeriferics(per)),
            #asyncio.create_task(updateScreen(per)), 
            asyncio.create_task(updateUSB(per)), 
        ) 

asyncio.run(main())   
