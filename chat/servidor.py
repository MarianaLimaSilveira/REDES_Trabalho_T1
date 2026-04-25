import socket
import threading
from datetime import datetime

# lista que guarda quem está conectado só para ler as mensagens
clientes_recebedores = []

def tratar_cliente(conexao, endereco):
    # quando alguém conecta, a primeira coisa que o cliente manda é um aviso
    # dizendo se ele é quem manda (remetente) ou quem recebe (recebedor).
    tipo = conexao.recv(1024).decode()

    if tipo == "RECEBEDOR":
        #Se for recebedor, eu guardo a conexão dele na lista
        clientes_recebedores.append(conexao)
        
        #esse loop infinito serve só pra manter a thread viva, fica esperando até o cara fechar o terminal.
        while True:
            try:
                dado = conexao.recv(1024)
                if not dado: 
                    break # Se o cliente fechou, sai do loop
            except:
                break
                
        # Se ele saiu, tira da lista
        clientes_recebedores.remove(conexao)
        conexao.close()

    elif tipo == "REMETENTE":
        # Se for quem envia as mensagens, entra num loop infinito esperando texto
        while True:
            try:
                msg = conexao.recv(1024).decode()
                if not msg: 
                    break
                
                # a mensagem ta chegando assim: "nome|texto que ele digitou"
                # o split corta a string no primeiro "|" que achar, serve só pra formatação bonitinha
                nome, texto = msg.split("|", 1)
                
                # pega o IP que vem da variável 'endereco'
                ip = endereco[0]
                
                # pega a hora atual do PC
                hora = datetime.now().strftime("%H:%M:%S")
                
                msg_final = f"{nome} ({ip}) [{hora}] {texto}"
                
                # aq o servidor faz o "Broadcast", manda essa string praa quem tiver na lista de recebedores
                for cliente_lendo in clientes_recebedores:
                    cliente_lendo.sendall(msg_final.encode())
                    
            except:
                break # Se der erro, sai do loop
        conexao.close()

# cmç do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9000))
server.listen()
print("Grupo de mensagen iniciado...")

# Fica rodando para sempre esperando pessoas conectarem
while True:
    conn, addr = server.accept()
    # Para cada pessoa que entra, cria uma Thread para não travar os outros
    t = threading.Thread(target=tratar_cliente, args=(conn, addr))
    t.start()