import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("127.0.0.1", 9000))

# Manda a primeira mensagem avisando: "Eu sou o cara que só lê"
cliente.sendall("RECEBEDOR".encode())

print("Aguardando novas mensagens do grupo...\n")

while True:
    # O programa fica parado/travado nessa linha até o servidor mandar algo
    msg = cliente.recv(1024).decode()
    
    # Quando chega, ele só imprime na tela
    print(msg)