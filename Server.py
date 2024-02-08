import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
SERVER_END_CONNECTION = "exit"


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.conn = None
        self.addr = None

    def socket_binding(self):
        # for socket.SOCK_STREAM, this type uses TCP as default
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def listen_for_client(self):
        self.socket.listen()  # the listening socket is distinct to the one wew ill use to communicate with later
        self.conn, self.addr = self.socket.accept()
        ''' accept() returns the host and port for the connection - the client host and port, 
            this also defines a new socket object and will be the one used to 
            communicate with the client. Conn = connection - connection handler, addr = address
            Here conn is the client socket object'''
        # defining the endpoint, socket.AF_INET (IPv4) expects a two-tuple: (host, port)
        # with conn:  # socket will be closed at end of block
        print(f"Connected by {self.addr}")  # prints address of client server connection

    def close_connection(self):
        self.conn.close()
        self.conn = None

    def send_client_message(self):
        server_message_bytes = input("Server:")
        server_message = bytes(server_message_bytes, 'utf-8')
        self.socket.sendall(server_message)  # Sends data to the server
        if server_message_bytes == SERVER_END_CONNECTION:
            self.close_connection()
            print("The client connection has been terminated.")

    def receive_client_message(self):
        while self.conn:
            data = self.socket.recv(1024).decode("utf-8")         # Receives the servers reply
            print(f"\nClient:{data}")     # Prints servers reply
            if data == SERVER_END_CONNECTION:
                self.close_connection()
                print("The client connection has been terminated.")







# while True:
#     '''the function recv() blocks the rest of the code from running (pauses execution) until it
#         receives data as then the funtion call is complete'''
#     data = conn.recv(1024).decode("utf-8")  # reads client data, 1024 means can receive 1024
#     print(f"\nClient:{data}")
#     if not data:            # if the conn.recv() returns and empty bytes object (no size) then this runs
#         break               # stops while loop
#     server_message = bytes(input("Server:"), 'utf-8')
#     conn.sendall(server_message)      # send client data back
