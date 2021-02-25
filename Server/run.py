from server import Server
import signal
import sys

if __name__ == "__main__":
    server = Server(IP="localhost", PORT=5000)
    server.start()