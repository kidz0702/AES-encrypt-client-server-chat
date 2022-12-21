import socket
import argparse
from random import randrange
# from DH import DiffieHellman, primes, BUFFER_SIZE, asn_encoder, dec
from HandlerAES import recive_message, send_message
from _thread import start_new_thread

SECRET_KEY = 9999999999999999

def start_client():
    
    ConnectionInfo = argparse.ArgumentParser()
    ConnectionInfo.add_argument("-ip", default = socket.gethostname())
    ConnectionInfo.add_argument("-p", type = int, default = '8080')
    ConnectionInfoParsed = ConnectionInfo.parse_args()
    IP = ConnectionInfoParsed.ip
    PORT = ConnectionInfoParsed.p
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("[ Socket created ]")
    
    
    print(f"[ Connecting to {IP}:{PORT} ]")
    client_socket.connect((IP, PORT))
    print("[ Connected ]")
    
    return client_socket


if __name__ == "__main__":
    
    sock = start_client()
    
    # Trao đổi khóa
    # keys_exchange(sock)
    
    print("[ Handling incoming messages ]")
    start_new_thread(recive_message, (sock, socket.gethostname(), SECRET_KEY))
    send_message(sock, SECRET_KEY)
    
    sock.close()