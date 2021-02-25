import socket
import pickle
from threading import Thread
import re
import sys

from clientConnection import ClientConnection

BUFFER_SIZE = 1024

class Server:
    def __init__(self, IP, PORT):
        """
            Initializing the object with IP and PORT.
        """
        self.IP = IP
        self.PORT = PORT
        
    def start(self):
        """
            Starting the server by creating client list binding the socket and listening to clients
            Also starting a new Thread When A Connection is established.
         """
        self.clients_connected = list()
        self.server_socket = socket.socket()
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen()
        print("[+] Server listening for connections!")
        Thread(target=self.accept_connections).start()
        
    def get_clients_connected(self):
        """
            A Getter method to get the list of connected clients.
        """
        return self.clients_connected
        
    def accept_connections(self):
        """
            A method that handles with accepting the connecting clients 
            The method will also create a new Thread for each client connection 
            which will target the method start_connection in the ClientConnection class.
            also the method adds the connected client to the clients_connected list.
            this method will always accept new connections thats done by the while True argumat.
        """
        while True:
            client_socket, _ = self.server_socket.accept()
            client = ClientConnection(client_socket, self)
            self.clients_connected.append(client)
            Thread(target=client.start_connection).start()
