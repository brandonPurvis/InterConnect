import socket
import time

__AUTHOR__ = "Brandon Purvis"
__VERSION__ = "0.2"
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
        """Send a line of text over the socket."""
        self.s.send(line + "\n")

    def nextLine(self):
        """Return the next line of text received by the socket."""
        message = self.s.recv(1024)
        return message

    def nextLine2(self):
        """Return input data untill a new line character is recived."""
        message = ""
        char = self.socket.recv(1)
        while not (char == "\n"):
            message += char
        return message 

    def next(self):
        """Return all available data"""
        print("Receiving Data...")
        dataIn = self.s.recv(1024)
        print ("IN: {}".format(dataIn))
        while True:
            more = self.s.recv(1024)
            print("PLUS: {}".format(more))
            if more == "":
                print("DONE")
                return datain
            else:
                dataIn += more

class SocketScannerLenProto(SocketScanner):
    """Sends and recieves messages in accordance with a
    message length based protocal.

    messages sent with the length of the message in characters
    prepending the message and demarked with a '|' between the
    length and the message.

    example:  '12|Hello World!'
    """
    def __init__(self, socket, name = "SocketScannerLength"):
        SocketScanner.__init__(self, socket, name)

    def printLine(self, message):
        """Send message through socket."""
        messageLength = len(message)
        lenProtoMessage = str(messageLength)+"|"+message
        self.s.send(lenProtoMessage)

    def nextLine(self):
        """recieve message from socket"""
        # Get the length of thr message
        length = ""
        while True:
            char = self.s.recv(1)
            if char != "|":
                length += char
            else:
                break
        try:
            assert char.isDigit() # Length must be a number
        except AssertionError:
            print "Length Protocal not followed connected agent."
            return SocketScanner.nextLine(self)

        length = int(length)
        
        # Read in the message.
        message = ""
        if length < 2056:
            message = self.s.recv(length)
        else:
            for i in xrange(length/2056 + 1):
                message += self.s.recv(2056)
        return message
