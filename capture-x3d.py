#!/usr/bin/env python3
import asyncio
import websockets
import time

async def get_x3d():
  uri = "ws://localhost:1234/"
  async with websockets.connect(uri) as websocket:
    await websocket.send("x3d;broadcast")
    while True:
      x3d_line = await websocket.recv()
      print(x3d_line)

if __name__ == "__main__":
  while True:
    try:
      asyncio.get_event_loop().run_until_complete(get_x3d())
    except:
      time.sleep(0.1)
