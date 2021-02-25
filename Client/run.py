import socket
from threading import Thread
import pickle
import sys

BUFFER_SIZE = 1024

class DisconnectFromServer(Exception): ...


class Client:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

    def start(self):
        """
            Connects to the server with the IP & PORT provided and procceds to the request_username function.
        """
        
        self.client_socket = socket.socket()
        try:
            self.client_socket.connect((self.IP, self.PORT))
        except ConnectionRefusedError:
            print("The server is not running currently.")
            sys.exit(0)
        self.request_username()

    def request_username(self):
        """
            Requests a username from the user, sends it to the server and recieves
            a boolean response that indicates if the name is valid or not. If the
            name is valid, two threads are created. One thread is for constantly recieving
            incoming messages, and for constantly looking for new messages to send. 
        """
        name = input("Please insert your name: ")
        self.client_socket.send(name.encode())
        is_name_valid = pickle.loads(self.client_socket.recv(BUFFER_SIZE))

        if type(is_name_valid) is bool:
            Thread(target=self.receieve_messages).start()
            Thread(target=self.send_messages).start()
        elif type(is_name_valid) is dict:
            print(is_name_valid["ERROR"])
            self.request_username()
            

    def send_messages(self):
        """
            Responsiable for sending messages from the client to the server.
        """

        while True:
            message = input()
            if message:
                if message != "exit()":
                    self.client_socket.send(message.encode())
                else:
                    self.client_socket.close()
                    raise DisconnectFromServer("You closed the client...bye :(")
    def receieve_messages(self):
        """
            Responsiable for listening for new messages indefinitely, if a
            message is recieved, it's printed to the console.
        """

        while True:
            print(self.client_socket.recv(BUFFER_SIZE).decode())

if __name__ == "__main__":
    client = Client(IP = "localhost", PORT = 5000)
    client.start()