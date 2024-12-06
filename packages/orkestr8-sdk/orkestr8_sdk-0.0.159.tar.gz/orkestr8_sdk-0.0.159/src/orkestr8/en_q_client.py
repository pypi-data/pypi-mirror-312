"""
Client to communicate with SDK created Python Queue.

RUN STATES:
- GET: retreives data
- STOP: Sends message to shutdown
"""
import socket
import time


def poll():
    sock = socket.socket()
    sock.connect(("localhost", 8000))
    sock.setblocking(False)
    data = None
    x = 1
    while x < 5:
        x += 1
        try:
            data = sock.recv(1024)
        except BlockingIOError as e:
            pass

        time.sleep(0.5)
    print(" polled => ", data)
    sock.close()
    return data
