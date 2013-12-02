import socket
import time

__AUTHOR__ = "Brandon Purvis"
__VERSION__ = "0.2.1"

class SocketScanner:
    """A wrapper around a socket object."""
    
    def __init__(self, socket, name = "SocketScanner"):
        """
        Wrapper around a socket providing easy I/O interfacing

        socket: socket object,
        name = sting.

        """ 
        self.name = name
        self.s = socket

    def printLine(self,line):
        """Send a line of text followed by a newline character over the socket."""
        self.s.send(line + "\n")

    def nextLine(self):
        """Return input data untill a new line character is recived."""
        message = ""
        char = self.socket.recv(1)
        while not (char == "\n"):
            message += char
        return message 

    def print(self, message):
        """send message over the socket. """
        self.s.send(message)

    def next(self):
        """Return all available data"""
        dataIn = self.s.recv(2048)
        return dataIn

class SocketScannerLenProto(SocketScanner):
    """
    Sends and recieves messages in accordance with a
    message length based protocal.

    messages sent with the length of the message in characters
    prepending the message and demarked with a '|' between the
    length and the message.

    example:  '12|Hello World!'

    """
    def __init__(self, socket, name = "SocketScannerLength"):
        SocketScanner.__init__(self, socket, name)

    def print(self, message):
        """Send message through socket."""

        messageLength = len(message)
        lenProtoMessage = str(messageLength)+"|"+message
        self.s.send(lenProtoMessage)

    def nextLine(self):
        

    def next(self):
        """recieve message from socket"""
        try:
        # Get the length of the message
            length = ""
            while True:
                char = self.s.recv(1)
                assert char.isDigit()
                if char != "|":
                    length += char
                else:
                    break
        # If given a string of all numbers, will go through counting each
        # as part of the length
        except AssertionError:
            print "Length Protocal not followed connected agent."
            return SocketScanner.nextLine(self)

        # Read in the message.
        length = int(length)
        message = ""
        if length < 2056:
            message = self.s.recv(length)
        else:
            for i in xrange(length/2056 + 1):
                message += self.s.recv(2056)
        return message
