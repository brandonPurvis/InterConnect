import SocketServer
import socket
import time

class SocketScanner:
    """A wrapper around a socket object."""
    
    def __init__(self, socket, name = "SocketScanner"):
        self.name = name
        self.s = socket

    def printLine(self,line):
        """Send a line of text over the socket."""
        self.s.send(line + "\n")

    def nextLine(self):
        """Return the next line of text received by the socket."""
        message = self.s.recv(1024)
        return message

class InterConnection:
    """Represents a line of communication between two entities."""
    
    def __init__(self, ip, port = 41000, name = "PythonSocket", host = False):
        
        self.port = port
        self.name = name
        self.connected = True
        self.methods = {}
        if not host:
            self.socket = self.connectToHost(ip, port)
        else:
            self.ip = socket.gethostbyname(socket.gethostname())
            self.socket = self.hostConnection(self.ip, port)

    def addMethod(self, call, func):
        """Add a call and a function to the set of methods
        call - A string
        func - function called when the call is received.
        """
        self.methods[call] = func

    def hostConnection(self, ip, port):
        """Host a server socket."""

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip, port))
        s.listen(1)
        sck, address = s.accept()
        
        return SocketScanner(sck, self.name)
        
    def connectToHost(self, ip, port):
        """Connect to a host with the given ip at the given port.
        ip - string
        port - integer
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        socketScanner = SocketScanner(s)
        return socketScanner

    def send(self, data):
        """Send the given data over the socket.
        data - String 
        """
        data = data + "\n"
        self.socket.printLine(data)

    def receive(self):
        """Read in data from the socket, up to a new line character."""
        
        line = self.socket.nextLine()
        return line 

    def callMethod(self, call, params):
        """Call Method on the other side of the connection."""
        message = call
        for p in params:
            message += " " + p
        self.send(message)
        resp = self.receive()
        while len(resp) < 1:
            resp = self.receive()
        return resp
        
    def verify(self):
        """Return true if the other entity acknoledges a request for
        verification.

        verification protocol:
            send 'VERIFY'
            receive 'ACK'
        """
        self.send("VERIFY")        
        resp = self.receive()
        while resp == "":
            time.sleep(1)
            resp = self.receive()
        return resp == "ACK"

    def listenLoop(self):
        """Continiously read in recieved data, responding according to
        methods in the method dictionary, when given a recognized call
        name.
        """
        while self.connected:
            # Listen
            recv = self.receive()
            if len(recv) > 0:
                print("IN: "+recv)
                components = recv.split()
                method, params = components[0],components[1:]
                
                # Respond
                if method == "END":
                    print("Terminating Connection")
                    self.connected = False

                if method in self.methods.keys():
                    print("Recognized Input")
                    func = self.methods[method]
                    ans = func(params)
                    print("OUT: " + ans)
                    self.send(ans)

                else:
                    print("Unknown Input: {}".format(method))
                    self.send("INVALID")            
