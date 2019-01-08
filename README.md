# websockets-assistant

### How to use it

```
from websockets_assistant import client, run, sleep

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
```
