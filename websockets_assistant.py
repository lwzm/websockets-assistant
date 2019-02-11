#!/usr/bin/env python3

import asyncio
import signal
import sys
import traceback
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


async def _loop(uri, consume, companion=None, once=False, timeout=5, **kwargs):
    ws = companion_task = None
    name = uri[:55]
    while True:
        ts = datetime.now()
        try:
            ws = await asyncio.wait_for(
                websockets.connect(uri, **kwargs), timeout)
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
    cr = _loop(*args, **kwargs)
    return asyncio.create_task(cr)


async def _stdin(init=None):
    """loop forever util
    init is a normal function or a coroutine
    """
    if init:
        o = init()
        if hasattr(o, "cr_code"):
            return await asyncio.create_task(o)

    loop = asyncio.get_running_loop()

    # register SIGTSTP
    def print_all_tasks():
        for i in asyncio.all_tasks():
            print(i._coro)

    loop.add_signal_handler(signal.SIGTSTP, print_all_tasks)  # Ctrl-Z

    # read standard input forever
    q = asyncio.Queue()

    loop.add_reader(
        sys.stdin, lambda: q.put_nowait(input()))

    while True:
        s = await q.get()
        try:
            print(repr(eval(s.rstrip())))
        except Exception:
            traceback.print_exc()
        sys.stdout.flush()


def run(init):
    asyncio.run(_stdin(init))


if __name__ == '__main__':
    async def hello(ws):
        await ws.send("hello")
        await sleep(1)
        await ws.send("websocket")
        await sleep(0.1)
        await ws.close()

    # test 1
    async def main():
        await asyncio.gather(
            client("wss://echo.websocket.org/", log, hello, True),
            client("wss://echo.websocket.org/", log, hello, True),
            client("wss://echo.websocket.org/", log, hello, True),
        )
    run(main)

    # test 2
    def main():
        client("wss://echo.websocket.org/", log, hello, True),
        client("wss://echo.websocket.org/", log, hello, True),
    run(main)
