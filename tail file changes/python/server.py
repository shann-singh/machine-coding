import asyncio
import websockets
import os

clients = set()

async def tail_file(websocket):
    clients.add(websocket)
    try:
        async for _ in websocket:  # Keep the connection alive
            pass
    finally:
        clients.remove(websocket)

async def send_new_lines(filepath):
    with open(filepath, "r") as f:
        f.seek(0, os.SEEK_END)  # Go to the end of file
        while True:
            line = f.readline()
            if not line:
                await asyncio.sleep(5)
                continue
            for client in clients:
                await client.send(line.strip())

async def main():
    filepath = os.path.join(os.getcwd(), "log.txt")  # The file you're writing to from console
    server = await websockets.serve(tail_file, "localhost", 8765)
    await asyncio.gather(server.wait_closed(), send_new_lines(filepath))

asyncio.run(main())
