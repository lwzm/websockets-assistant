#!/usr/bin/env python3

import asyncio
import sys
from datetime import datetime

import websockets

"""
find corlord fonts from colorama:

    colors = {}
    for i in dir(colorama.Fore):
        if not i.startswith("_"):
            print(getattr(colorama.Fore, i), i)
            colors[i.lower()] = getattr(colorama.Fore, i)
"""

colors = {
    'black': '\x1b[30m',
    'blue': '\x1b[34m',
    'cyan': '\x1b[36m',
    'green': '\x1b[32m',
    'lightblack_ex': '\x1b[90m',
    'lightblue_ex': '\x1b[94m',
    'lightcyan_ex': '\x1b[96m',
    'lightgreen_ex': '\x1b[92m',
    'lightmagenta_ex': '\x1b[95m',
    'lightred_ex': '\x1b[91m',
    'lightwhite_ex': '\x1b[97m',
    'lightyellow_ex': '\x1b[93m',
    'magenta': '\x1b[35m',
    'red': '\x1b[31m',
    'reset': '\x1b[39m',
    'white': '\x1b[37m',
    'yellow': '\x1b[33m',
}


def log(*args, color=None):
    color = colors.get(color, "")
    ts = datetime.now()
    print(f"{color}{ts}", *args, colors["reset"], file=sys.stderr, flush=True)


async def _loop(uri, consume=lambda x: x, assist=None, once=False):
    ws = None
    name = uri[:55]
    while True:
        ts = datetime.now()
        try:
            async with websockets.connect(uri) as ws:
                log(f"{id(ws):x}", name, color="green")
                if assist:
                    asyncio.get_event_loop().create_task(assist(ws))
                async for o in ws:
                    consume(o)
        except Exception as e:
            log(type(e), e, color="red")
        finally:
            log(f"{id(ws):x}", name, datetime.now() - ts, color="yellow")

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
