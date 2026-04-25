import socket
import threading
from datetime import datetime

# Lista para guardar quem está conectado apenas para LER as mensagens
clientes_recebedores = []

def tratar_cliente(conexao, endereco):
    # Quando alguém conecta, a primeira coisa que o cliente manda é um aviso
    # dizendo se ele é um REMETENTE ou um RECEBEDOR.
    tipo = conexao.recv(1024).decode()

    if tipo == "RECEBEDOR":
        # Se for recebedor, eu guardo a conexão dele na lista
        clientes_recebedores.append(conexao)
        
        # Esse loop infinito serve só pra manter a thread viva. 
        # Fica esperando até o cara fechar o terminal.
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
                
                # A mensagem chega assim: "Nome|Texto que ele digitou"
                # O .split("|", 1) corta a string no primeiro "|" que achar
                nome, texto = msg.split("|", 1)
                
                # Pega o IP que vem da variável 'endereco'
                ip = endereco[0]
                
                # Pega a hora atual do PC
                hora = datetime.now().strftime("%H:%M:%S")
                
                # Monta a string exatamente igual à Figura do professor:
                # Exemplo: Celso (192.168.10.40) [17:21:15] Oi pessoal
                msg_final = f"{nome} ({ip}) [{hora}] {texto}"
                
                # Agora o servidor faz o "Broadcast": manda essa string 
                # para TODOS que estão na lista de recebedores
                for cliente_lendo in clientes_recebedores:
                    cliente_lendo.sendall(msg_final.encode())
                    
            except:
                break # Se der erro (ex: cliente fechou abruptamente), sai do loop
        conexao.close()

# ---- INÍCIO DO SERVIDOR ----
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9000))
server.listen()
print("Servidor de Chat iniciado na porta 9000...")

# Fica rodando para sempre esperando pessoas conectarem
while True:
    conn, addr = server.accept()
    # Para cada pessoa que entra, cria uma Thread para não travar os outros
    t = threading.Thread(target=tratar_cliente, args=(conn, addr))
    t.start()