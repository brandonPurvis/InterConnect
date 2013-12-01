import InterConnectionClasses as icc

def END():
    return "ACK"

def WHO(connect):
    return connect.name

def ECHO(params):
    message = ""
    for string in params:
        message += string
    return message
    
connect = icc.InterConnection("localhost",40001,host=True)
connect.addMethod("WHO", lambda x: WHO(connect))
connect.addMethod("END", lambda x: END())
connect.addMethod("ECHO",lambda x: ECHO(x))
connect.listenLoop()
