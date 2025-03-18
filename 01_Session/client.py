import os
import time
import socket
import threading
from pynput import keyboard

#소켓 옵젝 만들기
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#서버 연결
host = 'localhost'
port = 12345
client_socket.connect((host, port))
print('서버에 연결')
flagClient = True
while flagClient:
  ch = input('입력: ')
  client_socket.send(ch.encode())

  response = client_socket.recv(1024)
  respData = response.decode()
  print('에코: ', respData)

  if (ch == 'q'):
    break

client_socket.sendall('quit'.encode()) #quit 보내고 클로즈
client_socket.close()
print('끝')