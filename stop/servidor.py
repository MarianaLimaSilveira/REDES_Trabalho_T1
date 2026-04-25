import random
import socket
import threading

HOST = "0.0.0.0"
PORT = 9002

N_JOGADORES = 2 
N_RODADAS = 3

nomes_jogadores = {}
pontos_totais = {}
respostas_rodada = {}
temas = ["Nome", "CEP", "Comida"]
letra_sorteada = ""

# variavel global pra guardar o placar em formato de texto gigante
resultado_formatado = "" 

# semaforos pra cada coisa
semaforo_inicio = threading.Semaphore(0)
semaforo_respostas = threading.Semaphore(0)
semaforo_resultados = threading.Semaphore(0)
semaforo_pronto = threading.Semaphore(0)
lock_dados = threading.Semaphore(1)

def gerar_resultados_da_rodada(letra):
    # calcula os pontos da rodada e formata o texto pra mandar pros clientes
    global resultado_formatado
    pontos_por_categoria = {tid: {t: 0 for t in temas} for tid in nomes_jogadores}
    
    # validação e calculo dos pontos
    for tema in temas:
        contagem = {}
        # conta quantas vezes cada resposta apareceu
        for tid in nomes_jogadores:
            resp = respostas_rodada[tid][tema].strip().upper()
            
            # regras: nao pode ser nulo, tem q ter 2 letras ou mais e começar com a letra certa
            if resp != "---" and len(resp) >= 2 and resp.startswith(letra.upper()):
                contagem[resp] = contagem.get(resp, 0) + 1
        
        # da 3 pontos se for unica, 1 se alguém repetiu, e 0 se errou as regras
        for tid in nomes_jogadores:
            resp = respostas_rodada[tid][tema].strip().upper()
            
            #startswith foi o comando q encontrei pra fazer a validação se a resposta começa com a letra sorteada
            if resp != "---" and len(resp) >= 2 and resp.startswith(letra.upper()):
                if contagem[resp] == 1:
                    pontos_por_categoria[tid][tema] = 3
                else:
                    pontos_por_categoria[tid][tema] = 1
            else:
                pontos_por_categoria[tid][tema] = 0  # zerou a categoria
                
    # formatação do placar
    msg = "\n<===================================>"
    msg += "\n        RESPOSTAS DA RODADA        "
    msg += "\n<===================================>\n"
    for tema in temas:
        msg += f"\nCategoria {tema}:\n"
        linha_respostas = []
        for tid, nome in nomes_jogadores.items():
            linha_respostas.append(f"{nome}: {respostas_rodada[tid][tema]}")
        msg += "  |  ".join(linha_respostas) + "\n"
    
    msg += "\n<===================================>"
    msg += "\n             PONTUACAO             "
    msg += "\n<===================================:>n"
    for tema in temas:
        msg += f"\nCategoria {tema}:\n"
        linha_pontos = []
        for tid, nome in nomes_jogadores.items():
            linha_pontos.append(f"{nome}: +{pontos_por_categoria[tid][tema]} pontos")
        msg += "  |  ".join(linha_pontos) + "\n"
    
    # soma os pontos da rodada no total de cada jogador
    for tid in nomes_jogadores:
        for tema in temas:
            pontos_totais[tid] += pontos_por_categoria[tid][tema]
    
    msg += "\n<===================================>"
    msg += "\n     PONTUACAO TOTAL ACUMULADA     "
    msg += "\n<===================================>\n"
    for tid, nome in nomes_jogadores.items():
        msg += f"{nome}: {pontos_totais[tid]} pontos\n"
    
    resultado_formatado = msg

def atender_cliente(conn, addr, tid):
    # função que cada thread vai rodar pra cuidar de um jogador
    # recebe o nome logo q conecta
    nome = conn.recv(1024).decode()
    
    # usa o lock pra não dar bug de duas threads mexendo ao msm tempo
    with lock_dados:
        nomes_jogadores[tid] = nome
        pontos_totais[tid] = 0
    print(f"[Servidor] Jogador conectado: {nome}")
    
    for r in range(1, N_RODADAS + 1):
        # segura ate o servidor principal sortear a letra e liberar
        semaforo_inicio.acquire()
        conn.sendall(f"LETRA:{letra_sorteada}".encode())

        resps_do_cliente = {}
        for tema in temas:
            dado = conn.recv(1024).decode()
            t, resp = dado.split(":", 1)
            resps_do_cliente[t] = resp
        
        with lock_dados:
            respostas_rodada[tid] = resps_do_cliente
        
        # avisa q esse jogador ja respondeu tudo e libera um espaço do semaforo
        semaforo_respostas.release()
        
        #Espera o servidor principal calcular os pontos pra poder ver o resultado
        semaforo_resultados.acquire()

        conn.sendall(resultado_formatado.encode())
        
        # espera o jogador dar enter pra ir pra proxima rodada
        conn.recv(1024)
        semaforo_pronto.release()
    
    conn.close()

def iniciar_servidor():
    global letra_sorteada
    
    # cmç do servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Aguardando {N_JOGADORES} jogadores conectarem...\n")

    for i in range(N_JOGADORES):
        conn, addr = server.accept()
        threading.Thread(target=atender_cliente, args=(conn, addr, i)).start()

    # laço principal do jogo
    for r in range(1, N_RODADAS + 1):
        # segura a tela aqui ate todo mundo entrar
        while len(nomes_jogadores) < N_JOGADORES: pass 
        
        letra_sorteada = random.choice("ABCDEFGIJKLMNOPQRSTUV")
        print(f"\n[RODADA {r}] Iniciada. Letra sorteada: {letra_sorteada}")
        
        # destrava as threads pros clientes começarem a jogar
        for _ in range(N_JOGADORES): semaforo_inicio.release()
        
        # trava aqui ate todos os jogadores mandarem as respostas pro servidor
        for _ in range(N_JOGADORES): semaforo_respostas.acquire()
        
        # calcula os pontos
        gerar_resultados_da_rodada(letra_sorteada)
        
        # libera os clientes pra verem o resultado
        for _ in range(N_JOGADORES): semaforo_resultados.release()
        
        # espera todo mundo dar OK no terminal antes de sortear a proxima letra
        for _ in range(N_JOGADORES): semaforo_pronto.acquire()
        
        print(f"[RODADA {r}] Concluida.")

    print("\nFim de Jogo! Servidor encerrando.")
    server.close()

if __name__ == "__main__":
    iniciar_servidor()