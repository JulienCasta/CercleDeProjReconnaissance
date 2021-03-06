import asyncio
from CPUdata import CPUdata
import logging
import websockets
import datetime
import json
import os
#from DSText import Audio, VADAudio
import argparse
# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send("Pong")

async def wsJson(websocket):
    while True:
        CpuData = CPUdata.getJsonData(CPUdata)
        await websocket.send(json.dumps(CpuData, default=str))
        await asyncio.sleep(3)

async def main():
    async with websockets.serve(wsJson, "192.168.3.211", 5000):
        await asyncio.Future()  # run forever
asyncio.run(main())