#!/usr/bin/env python3

import asyncio
import sys
from datetime import datetime

import websockets


def log(*args):
    print(datetime.now(), *args, file=sys.stderr, flush=True)


async def _loop(uri, consume=lambda x: x, assist=None, once=False):
    ws = None
    name = uri[:55]
    while True:
        ts = datetime.now()
        try:
            async with websockets.connect(uri) as ws:
                log(ws, name, "begin")
                if assist:
                    asyncio.get_event_loop().create_task(assist(ws))
                async for o in ws:
                    consume(o)
        except Exception as e:
            log(type(e), e)
        finally:
            log(ws, name, datetime.now() - ts)

        if once:
            break


def run(*args, **kwargs):
    return asyncio.get_event_loop().create_task(_loop(*args, **kwargs))


def start():
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    async def hello(ws):
        await ws.send("hello")
        await ws.send("websocket")
        await ws.close()
        await asyncio.sleep(0.1)
        asyncio.get_event_loop().stop()
    run("wss://echo.websocket.org/", print, hello, True)
    start()
