import asyncore
import logging
import string
import re
import TitlePicker

class Server(asyncore.dispatcher):
    """Receives connections and establishes handlers for each client.
    """
    
    def __init__(self, address, titlePicker):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.address = self.socket.getsockname()
        self.handlers = []
        self.listen(1)
        self.titlePicker = titlePicker
        self.handlersIndex = 0
        return

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()

        self.handlers.append(Handler(self, client_info[0], self.handlersIndex, self.titlePicker))
        self.handlersIndex += 1
        
        if len(self.handlersIndex) >= 4:
            self.handle_close()

        return
    
    def handle_close(self):
        self.close()
        return

class Handler(asyncore.dispatcher):
    """Handles echoing messages from a single client.
    """
    
    def __init__(self, parent, sock, index, titlePicker, chunk_size=1024):
        self.chunk_size = chunk_size
        asyncore.dispatcher.__init__(self, sock=sock)
        self.data_to_send = []
        self.ready = False
        self.parent = parent
        self.index = index
        self.titlePicker = titlePicker
        return
    
    def writable(self):
        """We want to write if we have received data."""
        response = bool(self.data_to_send)
        return response

    
    def handle_write(self):
        data = self.data_to_send.pop()
        sent = self.send(data)

        if sent < len(data):
            remaining = data[sent:]
            self.data_to_send.append(remaining)
        
        if not self.writable():
            self.handle_close()

    def handle_read(self):
        """Read an incoming message from the client and put it into our outgoing queue."""
        data = self.recv(self.chunk_size)
        
        """We want to ensure the Pis are ready"""

        if re.match("R-.*", data):
            self.ready = True
            self.data_to_send.append(titlePicker.getCurrentTitle().posList[self.index])

    
    def handle_close(self):
        self.close()

    def appendMessage(self, message):
        self.data_to_send.append(message)
        return


class Client(asyncore.dispatcher):
    """Sends messages to the server and receives responses.
    """
    
    def __init__(self, host, port, message, chunk_size=512):
        self.message = message
        self.to_send = message
        self.received_data = []
        self.chunk_size = chunk_size
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        return
    
    
    def handle_close(self):
        self.close()
        received_message = ''.join(self.received_data)
        if received_message == self.message:
            print('RECEIVED COPY OF MESSAGE\n')
        else:
            print('ERROR IN TRANSMISSION\n')
            print('EXPECTED "%s"\n', self.message)
            print('RECEIVED "%s"\n', received_message)
        return
    
    def writable(self):
        return bool(self.to_send)

    def handle_write(self):
        sent = self.send(self.to_send[:self.chunk_size])
        self.to_send = self.to_send[sent:]

    def handle_read(self):
        data = self.recv(self.chunk_size)
        self.received_data.append(data)

def main():
    #Main method for the server client on the main computer
    rasp1address = ("localhost", 0)
    shelfname = "titles"

    server = Server(rasp1address, TitlePicker(shelfname))

    ip, port = server.address
    
    client = Client(ip, port, "R", 1024)

    asyncore.loop()