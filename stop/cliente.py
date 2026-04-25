import socket

HOST = "127.0.0.1"
PORT = 9002

def iniciar_cliente():
    print("--- BEM-VINDO AO JOGO DE STOP ---")
    nome = input("Digite seu nome: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PORT))
            cliente.sendall(nome.encode())

            for r in range(3): # n_rodadas
                print("\nAguardando os outros jogadores e o sorteio da letra...")
                
                # Recebe a letra
                msg = cliente.recv(1024).decode()
                letra = msg.split(":")[1]
                print(f"\n---> A LETRA DA RODADA E: [{letra}] <---")

                # Preenchimento das Categorias
                for tema in ["Nome", "CEP", "Comida"]:
                    resp = input(f"{tema}: ").strip()
                    
                    # Se o jogador der apenas enter, envia vazio ("---")
                    if not resp:
                        resp = "---"
                        
                    cliente.sendall(f"{tema}:{resp}".encode())
                
                print("\nRespostas enviadas! Aguardando os outros jogadores terminarem...")
                
                # Recebe o Textão de Resultados do servidor (usa 4096 bytes por ser um texto longo)
                resultados = cliente.recv(4096).decode()
                print(resultados)

                # Sincronia para a próxima rodada
                input("\nDigite ENTER para indicar que esta pronto para a proxima rodada...")
                cliente.sendall("ok".encode())
            
            print("\nJogo finalizado! Obrigado por jogar.")
            
        except ConnectionRefusedError:
            print("Erro: Servidor nao encontrado.")

if __name__ == "__main__":
    iniciar_cliente()