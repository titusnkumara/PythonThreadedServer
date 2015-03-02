import sys
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
from netifaces import interfaces, ifaddresses, AF_INET

def printStartMessage():
    print "we have found these IP addresses for you"
    print "try entering each one of them"

def findIPAddress():
    addressList = []
    invalid = ['127.0.0.1','No']
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No'}] )]
        if addresses[0] not in invalid:
            addressList.append(addresses[0])
    return addressList

def exitProgram():
    inp = raw_input("press any key to exit")
    sys.exit()

def validateIPList(ipList):
    length = len(ipList)
    if(length==0):
        print "sorry you don't have any ip"
        exitProgram()
    return length

def printAndGetInput(ipAddresList,IPnumbers):
    for i in range(0,IPnumbers):
        print "[",i,"]: ",ipAddresList[i]
    inputNumber = IPnumbers+1
    while(True):
        inputNumberTmp = raw_input()
        try:
            numb = int(inputNumberTmp)
        except:
            print "please enter a valid number"
            continue
        inputNumber = int(inputNumberTmp);
        if(inputNumber<IPnumbers and inputNumber>=0):
            break
        else:
            print "enter a number within range"
    return inputNumber
        

def choseOneOfIP(ipAddresList,IPnumbers):
    #handle one ip
    if(IPnumbers==1):
        print "Your app will start with IP:",ipAddresList[0]
        return ipAddresList[0]
    else:
        print "Type the index number of IP you want to start with"
    inputNumber = printAndGetInput(ipAddresList,IPnumbers)
    return ipAddresList[inputNumber]
    
def askForPort():
    print "enter port number you wish to continue between 2000~60000"
    inputNumber = 0
    while(True):
        inputNumberTmp = raw_input()
        try:
            numb = int(inputNumberTmp)
        except:
            print "please enter a valid number"
            continue
        inputNumber = int(inputNumberTmp);
        if(inputNumber<60000 and inputNumber>=2000):
            break
        else:
            print "enter a number within range"
    return inputNumber

class ThreadingSimpleServer(SocketServer.ThreadingMixIn,
                   BaseHTTPServer.HTTPServer):
    pass



ipAddresList=findIPAddress()
IPnumbers = validateIPList(ipAddresList)
ip = choseOneOfIP(ipAddresList,IPnumbers)
port = askForPort()


try:
    server = ThreadingSimpleServer((ip, port), SimpleHTTPServer.SimpleHTTPRequestHandler)

    print "Server started in address http://"+ip+":"+str(port)
except:
    "Sorry, the port maybe in use, try with different port"


try:
    while 1:
        sys.stdout.flush()
        server.handle_request()
except KeyboardInterrupt:
    print "Finished"
