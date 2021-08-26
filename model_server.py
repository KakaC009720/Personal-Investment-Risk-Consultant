import socket
import threading
from dnn_server import dnn_server
HOST = '140.112.73.209'
PORT = 8001

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST, PORT))



# def start():
while True:
    server.listen(5)
    conn, addr = server.accept()
    print('Connected by ', addr)

    while True:
        response = '0'
        data = conn.recv(1024).decode('utf-8')
        print(data)
        data = data.split(',')
        cust_no, company, c_stock, t_type = data[0], data[1], data[2], data[3]
        response = dnn_server(cust_no, company, c_stock, t_type)
        print(response)
        conn.sendall(str(response).encode('utf-8'))

