# websockets-assistant

### How to use it

```
from websockets_assistant import run, start

async def hello(ws):
    await ws.send("hello")
    await ws.send("websocket")

run("wss://echo.websocket.org/", print, hello)

start()
```
