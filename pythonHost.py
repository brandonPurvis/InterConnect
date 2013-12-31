import InterConnectionClasses as icc
import sys

__ALL__ = ["END","WHO","ECHO","ADD","MULT", "ALL"]

PORT = 40000    # DEFAULT PORT 
if len(sys.argv) >= 2:
    PORT = int(sys.argv[1])
    

def END():
    return "ACK"

def WHO(connect):
    return connect.name

def ECHO(params):
    message = ""
    for string in params:
        message += " " + string
    return message

def ADD(params):
    s = sum(map(int, params))
    return str(s)

def MULT(params):
    p = reduce(lambda x,y: x*y, map(int, params) )
    return str(p)

def ALL():
    message = ""
    for m in __ALL__:
        message += m + " "
    return message

connect = icc.InterConnection("localhost",PORT ,host=True)
connect.addMethod("WHO", lambda x: WHO(connect))
connect.addMethod("END", lambda x: END())
connect.addMethod("ECHO",lambda x: ECHO(x))
connect.addMethod("ADD", lambda x: ADD(x))
connect.addMethod("MULT", lambda x: MULT(x))
connect.addMethod("ALL", lambda x: ALL())
connect.listenLoop()
