import socket

HOST = "127.0.0.1"
PORT = 9002

def iniciar_cliente():
    print("<--- BEM-VINDO AO JOGO DE STOP --->")
    nome = input("Digite seu nome: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PORT))
            
            # manda o nome pro servidor assim q conecta
            cliente.sendall(nome.encode())

            # faz o laço rodar as 3 rodadas
            for r in range(3): 
                print("\nAguardando os outros jogadores para o sorteio da letra...")
                
                # recebe a string do servidor e corta no ":" pra pegar só a letra
                msg = cliente.recv(1024).decode()
                letra = msg.split(":")[1]
                print(f"\n---> A LETRA DA RODADA É: [{ letra }] <---")

                # loop pra pedir os inputs das categorias
                for tema in ["Nome", "CEP", "Comida"]:
                    resp = input(f"{tema}: ").strip()
                    
                    # se o cara der só enter, manda "---" pro servidor saber q ele pulou
                    if not resp:
                        resp = "---"
                        
                    cliente.sendall(f"{tema}:{resp}".encode())
                
                print("\nRespostas enviadas! Aguardando os outros jogadores terminarem...")
                
                resultados = cliente.recv(4096).decode()
                print(resultados)

                # segura a tela ate o cara dar enter pra nao emendar uma rodada na outra sem ele ler
                input("\nDigite ENTER para indicar que esta pronto para a proxima rodada...")
                cliente.sendall("ok".encode())
            
            print("\nJogo finalizado! Obrigado por jogar.")
            
        except ConnectionRefusedError:
            print("Erro: Servidor nao encontrado.")

if __name__ == "__main__":
    iniciar_cliente()