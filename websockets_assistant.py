#!/usr/bin/env python3

import asyncio
import sys
import traceback

import pendulum
import websockets


def log(*args):
    print(pendulum.now(), *args, file=sys.stderr, flush=True)


async def _loop(uri, consume=lambda x: x, assist=None, once=False):
    ws = None
    while True:
        try:
            async with websockets.connect(uri) as ws:
                log(ws, "begin", uri[:50])
                if assist:
                    asyncio.get_event_loop().create_task(assist(ws))
                async for o in ws:
                    consume(o)
                log(ws, "end", uri[:50])
        except Exception:
            log(ws, uri[:50])
            traceback.print_exc()
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
    run("wss://echo.websocket.org/", print, hello)
    start()
