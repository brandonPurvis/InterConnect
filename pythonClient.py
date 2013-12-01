import InterConnectionClasses as icc
# Python Client


ip = icc.socket.gethostbyname(icc.socket.gethostname())
port = 40001

print("Python Client:")
print("IP: {}".format(ip))
print("PORT: {}".format(port))
connection = icc.InterConnection(ip, port, name = "LabtopClient", host = False)
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
            
