# websockets-assistant

### How to use it

```
from websockets_assistant import client, start, sleep

async def hello(ws):
    await ws.send("hello")
    await sleep(1)
    await ws.send("websocket")
    await sleep(0.1)
    await ws.close()

async def main():
    client("wss://echo.websocket.org/", print, hello, True)
    client("wss://echo.websocket.org/", print, hello, True)
    for i in range(5, 0, -1):
        print(i)
        await sleep(1)

start(main())
```
