import socket

# Conecta no servidor local
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("127.0.0.1", 9000))

# Manda a primeira mensagem avisando: "Eu sou o cara que digita"
cliente.sendall("REMETENTE".encode())

# Pede o nome uma vez só
nome = input("Digite seu nome: ")
print("Você já pode digitar suas mensagens abaixo:")

while True:
    # Fica em loop pedindo para digitar algo
    texto = input("> ")
    
    # Junta o nome e o texto usando um "|" no meio para o servidor conseguir separar depois
    pacote = f"{nome}|{texto}"
    
    # Envia pro servidor
    cliente.sendall(pacote.encode())