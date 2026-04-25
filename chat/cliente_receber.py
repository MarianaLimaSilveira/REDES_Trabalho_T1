import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("127.0.0.1", 9000))

#Manda a primeira mensagem avisando eu sou quem lê as mensagens
cliente.sendall("RECEBEDOR".encode())

print("Aguardando novas mensagens do grupo...\n")

while True:
    # O programa fica parado nessa linha até o servidor mandar algo
    msg = cliente.recv(1024).decode()
    
    print(msg)