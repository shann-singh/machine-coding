import asyncio
import websockets
import os

class LogTailServer:
    def __init__(self, filepath, host="localhost", port=8765):
        self.filepath = filepath
        self.host = host
        self.port = port
        self.clients = set()

    async def register(self, websocket):
        print(f"Client added :: [{websocket.remote_address}]")
        self.clients.add(websocket)
        try:
            async for _ in websocket:  # Keeps the connection alive
                pass
        finally:
            self.clients.remove(websocket)

    async def send_new_lines(self):
        with open(self.filepath, "r") as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    await asyncio.sleep(0.5)
                    continue
                await self.broadcast(line.strip())

    async def broadcast(self, message):
        if self.clients:
            print(" | ".join(f"[{client.remote_address[0]}:{client.remote_address[1]}] :: {message}" for client in self.clients))
            await asyncio.gather(*(client.send(message) for client in self.clients))

    async def start(self):
        server = await websockets.serve(self.register, self.host, self.port)
        print(f"Server running at ws://{self.host}:{self.port}")
        await asyncio.gather(server.wait_closed(), self.send_new_lines())

if __name__ == "__main__":
    file_path = os.path.join(os.getcwd(), "log.txt")
    log_server = LogTailServer(filepath=file_path)
    asyncio.run(log_server.start())
