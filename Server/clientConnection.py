import pickle
from threading import Thread
import re
import socket

BUFFER_SIZE = 1024

class ClientConnection:
    def __init__(self, client:socket, server):
        """
            Initializing the ClientConnection class with an object
            needs the socket of the client and the server object.
        """
        self._client = client
        self._server = server
         
    def is_name_exists(self, name):
        """
            checks if the name is existing in the connected clients list and
             if its more then one of the same name the server sends an error back to the user.
        """
        counter = 0
        for clients_name in self._server.clients_connected:
            if name == clients_name.name:
                counter += 1
        return counter > 1

    def check_client_name(self, name):
        """
            Checks if the username of the client is valid.
        """
        expr = r"^[a-zA-Z]{2,}"
        if re.match(expr, name) is None:
            return {"ERROR": "A name must contain only letters! Please Connect again with a diffrent name."}
        elif self.is_name_exists(name):
            return {"ERROR": f"The name: {name} is already connected. Please connect again with a diffrent name."}
        else:
            return True
       
    def start_connection(self):
        """
            starts a connection between the server and client.
            gets a name from a client and sends the name to the check_client_name method
            sends back to the client a bool which tells if the name is valid or not.
        """
        is_name_ok = {}
        while type(is_name_ok) is dict: 
            self.name = self._client.recv(BUFFER_SIZE).decode()
            is_name_ok = self.check_client_name(self.name)
            self._client.send(pickle.dumps(is_name_ok))
        
        self.broadcast_message("Has joined.")

        Thread(target=self.await_client_message).start()

    def await_client_message(self):
        """
            checks and recivies a message from a client. 
            and sends the message to the broadcast_message method.
        """
        try:
            while True:
                client_message = self._client.recv(BUFFER_SIZE).decode()
                if not client_message:
                    self.close_connection()
                self.broadcast_message(client_message)
        except ConnectionResetError:
            self.close_connection()
         
    def broadcast_message(self, msg):
        """
            sends a message to all the clients that are connected to server.
        """
        for client in self._server.get_clients_connected():
            client_socket = client._client
            client_socket.send(f"{self.name}: {msg}".encode())
    
    def close_connection(self):
        """
            Closes the existing connection to the server by removing the Client
            object from the currently connected clients list.
        """
        self._server.clients_connected.remove(self)
        self._client.close()