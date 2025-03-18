import os
import socket
from pynput import keyboard

def on_press(key):
  global flagStatus, client_socket

  print(f"Pressed: {key}")
  if key == keyboard.Key.esc or (key.char == 'q'):
    flagStatus = False
  else:
    client_socket.send(key.char.encode())
    response = client_socket.recv(1024)
    respData = response.decode()
    print('echo: ', respData)

#소켓 옵젝 만들기
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#서버 연결
host = '10.150.149.232'
port = 54321
client_socket.connect((host, port))
print('서버에 연결')

flagStatus = True

#키보드 이벤트 리스너 실행
listener = keyboard.Listener(on_press=on_press)

listener.start()

try:
  while flagStatus:
    pass
except KeyboardInterrupt:
  listener.stop()

client_socket.sendall('quit'.encode()) #quit 보내고 클로즈
client_socket.close()
print('끝')