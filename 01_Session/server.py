import socket

#binding
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 12345
server_socket.bind((host, port))

#듣기 모드 대기
server_socket.listen(1)
print('서버 시작, 기다려려')

flagServer = True
while flagServer:
  #클라이언트 연결 시도 대기
  client_socket, address = server_socket.accept()
  print('연결되었다', address)

  while True:
    data = client_socket.recv(1024)
    if not data:
      break

    rcvData = data.decode() #데이터 디코드로 보여주기
    if not (rcvData == 'quit'):
      flagServer = False
      print('수신: ', rcvData.encode())
    else: #quit이면
      print('종료: ', rcvData.encode())
      break
    client_socket.sendall(data)

client_socket.close()