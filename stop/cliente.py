import socket

HOST = "127.0.0.1"  
PORT = 9002

def iniciar_cliente():
    print("--- Bem-vindo ao jogo de STOP ---")
    
    nome = input("Digite seu nome para jogar: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PORT))
            print(f"\n[{nome}] Conectado com sucesso!")
            print("Aguardando os outros jogadores conectarem e o servidor sortear a letra...")
            
            # Recebe a mensagem do servidor contendo o aviso de início e a letra
            mensagem_servidor = cliente.recv(1024).decode()
            print(f"\n[Servidor] {mensagem_servidor}")
            
            # 1. Enviar o 'nome' para o servidor (cliente.sendall...)
            # 2. Pedir os inputs dos temas (CEP, Nome, etc.)
            # 3. Enviar as respostas para o servidor

            input("\n[Pressione ENTER para encerrar o cliente provisoriamente...]")

        except ConnectionRefusedError:
            print("Erro: A conexão foi recusada. O servidor está rodando?")

if __name__ == "__main__":
    iniciar_cliente()