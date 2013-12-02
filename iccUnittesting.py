# Unittesting

import unittest
import socket
from  SocketScanner import SocketScanner
import thread

class TestSocketScanner(unittest.TestCase):
    def listenAccept(self, socket):
        socket.listen(1)
        sck, address = socket.accept()
        self.socketHost = sck
        
    def setUp(self):
        ip = socket.gethostbyname(socket.gethostname())
        port = 45000
        
        # Create test host socket
        self.socketHost = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketHost.bind((ip,port))
        thread.start_new_thread(self.listenAccept, (self.socketHost, ))
    
        # Create test Client socket and connect to host
        self.socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketClient.connect((ip,port))

        # create Scanners
        self.hostScanner = SocketScanner(self.socketHost, "testHostScanner")
        self.clientScanner = SocketScanner(self.socketClient, "testClientScanner")

    def tearDown(self):
        self.socketHost.close()
        self.socketClient.close()

    def testPrintLineNextLine(self):
        self.hostScanner.printLine("TEST1\n")
        received = self.ClientScanner.nextLine()
        self.assertEqual("TEST1",received)

if __name__ == "__main__":
    unittest.main()
        
