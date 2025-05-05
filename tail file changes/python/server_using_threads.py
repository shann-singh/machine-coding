import os
import time
import threading
from websocket_server import WebsocketServer

clients = []

# WebSocket connection handler
def new_client(client, server):
    clients.append(client)
    print(f"New client connected: {client['address']}")

def client_left(client, server):
    if client in clients:
        clients.remove(client)
    print(f"Client disconnected: {client['address']}")

# Function to send new lines to all connected clients
def send_new_lines(filepath, server):
    with open(filepath, "r") as f:
        f.seek(0, os.SEEK_END)  # Go to the end of the file to only read new lines
        while True:
            line = f.readline()
            if line:
                for client in clients:
                    print(f"[{client['address']}] :: {line.strip()}")
                    server.send_message(client, line.strip())
            else:
                time.sleep(0.5)  # Wait for new lines to be added

# Start WebSocket server
def start_server():
    server = WebsocketServer(port=8765, host="localhost")
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    
    # Start the server in a separate thread
    server_thread = threading.Thread(target=server.run_forever)
    server_thread.daemon = True
    server_thread.start()

    return server

if __name__ == "__main__":
    filepath = os.path.join(os.getcwd(), "log.txt")  # File to monitor
    server = start_server()

    # Monitor file and send new lines to clients in separate thread
    file_change_thread = threading.Thread(target=send_new_lines, args=(filepath, server))
    file_change_thread.daemon = True
    file_change_thread.start()

    while True:
        time.sleep(1)
