import socket
import ssl
import threading
import os

SERVER_HOST = 'localhost'
SERVER_PORT = 12345
server_address = (SERVER_HOST, SERVER_PORT)

# Path to certificate
CERT_DIR = os.path.join(os.path.dirname(__file__), 'certificates')
CERT_FILE = os.path.join(CERT_DIR, 'server-cert.crt')

def receive_messages(ssl_socket):
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            print(data.decode('utf-8'))
    except Exception as e:
        print(f"Error receiving: {e}")
    finally:
        ssl_socket.close()
        print("Disconnected from server")

def start_client():
    # Create TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(CERT_FILE)
    context.verify_mode = ssl.CERT_REQUIRED
    
    try:
        # Establish SSL connection
        ssl_socket = context.wrap_socket(
            client_socket,
            server_hostname=SERVER_HOST
        )
        ssl_socket.connect(server_address)
        print(f"Connected to server {SERVER_HOST}:{SERVER_PORT}")
        
        # Start receive thread
        receive_thread = threading.Thread(
            target=receive_messages,
            args=(ssl_socket,)
        )
        receive_thread.daemon = True
        receive_thread.start()
        
        # Send messages
        while True:
            message = input("> ")
            if message.lower() == 'exit':
                break
            ssl_socket.send(message.encode('utf-8'))
            
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        ssl_socket.close()

if __name__ == "__main__":
    start_client()