from AES import AESCipher
# from random import randint as r
# from random import choice as pl
import time
from datetime import datetime

# current timestamp

# print("Timestamp:", x)

import socket
BUFFER_SIZE = 4096
        
def recive_message(sock: socket, addr: str, secret: int) -> None:
    while True:
        try:
            # msg = sock.recv(BUFFER_SIZE).decode('utf-8')
            # ts = time.time()
            dt = datetime.now()
            # str_dt = dt.strftime("%d-%m-%Y, %H:%M:%S")
            
            msg = sock.recv(BUFFER_SIZE)
            msg = AESCipher(msg, str(secret)).decrypt()
            if not msg:
                break
            print(f"\r{addr} : {msg} - {dt}")
            print("\r> ", end="")
        except socket.error:
            print("[ ERROR: Could not recive message ]")
            break
        except ValueError:
            break

    print(f"[ Connection with {addr} closed ]\n")
    sock.close()   
    
def send_message(sock: socket, secret: int) -> None:
    while True:
        # msg = input("> ").encode('utf-8')
        # ts = time.time()
        dt = datetime.now()
        # str_dt = dt.strftime("%d-%m-%Y, %H:%M:%S")
        
        msg = input("> ")
        print(f"\r> sent at: {dt}")
        # msg = dt + msg
        if not msg:
            break
        encrypt_client = AESCipher(msg, str(secret)).encrypt()
        try:
            sock.sendall(encrypt_client)
        except socket.error:
            print("[ ERROR: Could not send message ]")
            break
        
    print(f"[ Connection closed ]\n")
    sock.close()

def recieve(sock: socket) -> str:
    msg = sock.recv(BUFFER_SIZE).decode("utf-8")
    return msg