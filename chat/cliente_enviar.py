import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("127.0.0.1", 9000))

# manda a primeira mensagem avisando a função
cliente.sendall("REMETENTE".encode())

nome = input("Digite seu nome: ")
print("Agora você pode digitar suas mensagens abaixo:")

while True:
    # Fica em loop pedindo para digitar algo
    texto = input("> ")
    
    #Junta o nome e o texto usando um "|" no meio para o servidor conseguir separar depois
    pacote = f"{nome}|{texto}"
    
    # envia pro servidor
    cliente.sendall(pacote.encode())