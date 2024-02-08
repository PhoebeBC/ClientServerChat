import socket
import threading

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
CLIENT_END_CONNECTION = "exit"


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def connect_to_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))  # Creates a socket object to connect to the server
        # - this is the one accept() will receive
        print("You are connected to the server!\nYou can now send the server messages. Type your message below.")

    def close_connection(self):
        self.socket.close()
        self.socket = None

    def send_server_message(self):
        client_message_bytes = input("Client:")
        client_message = bytes(client_message_bytes, 'utf-8')
        self.socket.sendall(client_message)  # Sends data to the server
        if client_message_bytes == CLIENT_END_CONNECTION:
            self.close_connection()
            print("The server connection has been terminated.")

    def receive_server_message(self):
        while self.socket:
            data = self.socket.recv(1024).decode("utf-8")         # Receives the servers reply
            print(f"\nServer:{data}")     # Prints servers reply
            if data == CLIENT_END_CONNECTION:
                self.close_connection()
                print("The server connection has been terminated.")


client1 = Client(HOST, PORT)
client1.connect_to_server()
t = threading.Thread(target=client1.receive_server_message)
t.daemon = True
t.start()
while client1.socket:
    client1.send_server_message()
