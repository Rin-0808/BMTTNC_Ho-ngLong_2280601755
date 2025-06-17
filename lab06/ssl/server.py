import socket
import ssl
import threading
import os

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
server_address = (SERVER_HOST, SERVER_PORT)

# Path to certificate files
CERT_DIR = os.path.join(os.path.dirname(__file__), 'certificates')
CERT_FILE = os.path.join(CERT_DIR, 'server-cert.crt')
KEY_FILE = os.path.join(CERT_DIR, 'server-key.key')

clients = []

def handle_client(ssl_socket):
    clients.append(ssl_socket)
    client_address = ssl_socket.getpeername()
    print(f"Connected to: {client_address}")

    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Received: {message}")
            
            # Broadcast to all clients
            for client in clients:
                if client != ssl_socket:
                    try:
                        client.send(message.encode('utf-8'))
                    except:
                        clients.remove(client)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        clients.remove(ssl_socket)
        ssl_socket.close()
        print(f"Disconnected: {client_address}")

def start_server():
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}...")

    # SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    try:
        while True:
            client_socket, _ = server_socket.accept()
            
            # Wrap with SSL
            ssl_socket = context.wrap_socket(client_socket, server_side=True)
            
            # Start client thread
            client_thread = threading.Thread(
                target=handle_client, 
                args=(ssl_socket,)
            )
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()