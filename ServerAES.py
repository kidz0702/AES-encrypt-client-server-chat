import socket
import argparse
from random import randrange
# from DH import DiffieHellman, primes, BUFFER_SIZE, asn_encoder, dec
from HandlerAES import recive_message, send_message
from _thread import start_new_thread

SECRET_KEY = 9999999999999999

def start_server():
    # Lấy địa chỉ IP và cổng từ các param trên dòng lệnh, mặc định localhost:8080
    ConnectionInfo = argparse.ArgumentParser()
    ConnectionInfo.add_argument("-ip", default = socket.gethostname())
    ConnectionInfo.add_argument("-p", type = int, default = '8080')
    ConnectionInfoParsed = ConnectionInfo.parse_args()
    IP = ConnectionInfoParsed.ip
    PORT = ConnectionInfoParsed.p
    
    # Tạo đối tượng socket: socket.AF_INET - socket sử dụng IPv4, socket.SOCK_STREAM - loại socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind với địa chỉ IP và cổng.
    server_socket.bind((IP, PORT))
    print (f"[ Socket bind complete ]")
    
    # Đang chờ kết nối máy khách: 1 - số lượng kết nối tối đa trong hàng đợi.
    server_socket.listen(1)

    print(f"[ Server is now listening on {IP}:{PORT} ]")

    return server_socket

if __name__ == "__main__":
    sock = start_server()
    
    # Thiết lập kết nối với client - nhận đối tượng IP và PORT từ client
    client_socket, client_addr = sock.accept()
    print(f'[ {client_addr} connected ]')
    
    # Trao đổi khóa
    # keys_exchange(client_socket)
     
    # Xử lý tin nhắn đến
    print("[ Handling incoming messages ]")
    start_new_thread(recive_message, (client_socket, client_addr, SECRET_KEY))
    send_message(client_socket, SECRET_KEY)
    
    # Đóng kết nối
    client_socket.close()
    sock.close()