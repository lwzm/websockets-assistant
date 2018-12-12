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

sleep = asyncio.sleep

_tty = sys.stderr.isatty()


def log(*args, color=None):
    ts = datetime.now()
    if _tty and color:
        color, reset = colors[color], colors["reset"]
        print(f"{color}{ts}", *args, reset, file=sys.stderr, flush=True)
    else:
        print(f"{ts}", *args, file=sys.stderr, flush=True)


async def _loop(uri, consume, companion=None, once=False, timeout=5):
    ws = companion_task = None
    name = uri[:55]
    while True:
        ts = datetime.now()
        try:
            ws = await asyncio.wait_for(websockets.connect(uri), timeout)
            companion_task = companion and asyncio.create_task(companion(ws))
            log(f"{id(ws):x}", name, color="green")
            async for o in ws:
                consume(o)
        except asyncio.CancelledError:
            break
        except Exception as e:
            log(type(e), e, color="red")
        finally:
            ws and await ws.close()
            companion_task and companion_task.cancel()
            log(f"{id(ws):x}", name, datetime.now() - ts, color="yellow")

        if once:
            break
        await sleep(0.1)


def client(*args, **kwargs):
    return asyncio.create_task(_loop(*args, **kwargs))


def start(go=None):
    go and asyncio.run(go)


if __name__ == '__main__':
    async def hello(ws):
        await ws.send("hello")
        await sleep(1)
        await ws.send("websocket")
        await sleep(0.1)
        await ws.close()
    async def main():
        #await client("wss://echo.websocket.org/", log, hello, True)
        client("wss://echo.websocket.org/", log, hello, True)
        client("wss://echo.websocket.org/", log, hello, True)
        for i in range(5, 0, -1):
            print(i)
            await sleep(1)
    start(main())
