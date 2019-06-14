import socket
import signal

looping = True
def sig_handler(signum, _):
    global looping
    looping = False

signal.signal(signal.SIGINT, sig_handler)

TCP_IP = "192.168..39"
PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, PORT))
s.listen(1)
print "Listening..."

conn, addr = s.accept()
print "Connection address:", addr
while looping:
    data = conn.recv(BUFFER_SIZE)
    print "Received data:", data

conn.close()