import InterConnectionClasses as icc
import sys
# Python Client

# DEFAULTS
IP = icc.socket.gethostbyname(icc.socket.gethostname())
PORT = 40000

# SPECIFIED
ARGS = sys.argv
if len(ARGS) >= 2:
    IP = ARGS[1]
    PORT = ARGS[2]

print("Python Client:")
print("IP: {}".format(IP))
print("PORT: {}".format(PORT))
connection = icc.InterConnection(IP, PORT, name = "LabtopClient", host = False)
print("Connected")

if __name__ == "__main__":
    running = True
    while running == True:
        method = raw_input("METHOD: ")
        params = raw_input("PARAMS: ").split()
        response = connection.callMethod(method, params)
        print(response)
        print("")
        if response == "COMPLETE":
            running = False
            break
            
