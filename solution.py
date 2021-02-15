 #import socket module
from socket import *
import sys # In order to terminate the program

def convert(resp) -> object:
    resp_str = ""

    for (k, v) in resp.items():
        resp_str = resp_str + k + ' ' + v + '\r\n'

    resp_str = resp_str + '\r\n'
    return resp_str

def get_host_ip():
    try:
        #hostname = gethostname()
        #ipaddr = gethostbyname(hostname)
        #this is what is needed for autograder
        ipaddr = gethostbyname('localhost')
    except:
        print("unable to get IP")
    return ipaddr

def webServer(port=13331):
   serverSocket = socket(AF_INET, SOCK_STREAM)
   serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
   ipaddr = get_host_ip()
   serverSocket.bind((ipaddr, port))
   serverSocket.listen(5)

   while True:
       #Establish the connection
       #print('Ready to serve...')
       connectionSocket, addr = serverSocket.accept()
       try:
           message = connectionSocket.recv(4096)
           if not message:
               break;
           filename = message.split()[1]
           f = open(filename[1:])
           outputdata = f.read()

           #Send one HTTP header line into socket
           #define header using dict and then convert to a string
           response_ok_hdr = {
                          'HTTP/1.1': '200 OK',
                          'Content-Type:': 'text/html; charset=UTF-8',
                          'Content-Length:': str(len(outputdata)),
                          'Connection:': 'close',}
           response = convert(response_ok_hdr)

           connectionSocket.send(response.encode())

           #Send the content of the requested file to the client
           #autograder doesn't like this so changing to sendall
           #for i in range(0, len(outputdata)):
           #    connectionSocket.send(outputdata[i].encode())

           connectionSocket.sendall(outputdata.encode())
           connectionSocket.send("\r\n".encode())
           connectionSocket.close()
           f.close()
       except IOError:
           #Send response message for file not found (404)
           error404 = {
               'HTTP/1.1': '404 Not Found',
               'Content-Type:': 'text/html; charset=iso-8859-1',
               'Content-Length:': '0',
               'Connection:': 'close',}
           response = convert(error404)
           connectionSocket.send(response.encode())

           #Close client socket
           connectionSocket.close()

   serverSocket.close()
   sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
   webServer(13331)

