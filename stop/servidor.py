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
resultado_formatado = "" # Variável global que vai guardar o placar em formato de texto

# Semáforos para guiar as fases do jogo
semaforo_inicio = threading.Semaphore(0)
semaforo_respostas = threading.Semaphore(0)
semaforo_resultados = threading.Semaphore(0)
semaforo_pronto = threading.Semaphore(0)
lock_dados = threading.Semaphore(1)

def gerar_resultados_da_rodada(letra):
    """Calcula os pontos da rodada e formata o texto para enviar aos clientes"""
    global resultado_formatado
    pontos_por_categoria = {tid: {t: 0 for t in temas} for tid in nomes_jogadores}
    
    # 1. Validação RIGOROSA e cálculo dos pontos
    for tema in temas:
        contagem = {}
        # Conta ocorrências APENAS das respostas válidas
        for tid in nomes_jogadores:
            resp = respostas_rodada[tid][tema].strip().upper()
            
            # REGRAS DE OURO PARA PONTUAR:
            # - Não pode ser a marcação de vazio ("---")
            # - Tem que ter pelo menos 2 letras (impede de digitar só a letra do sorteio)
            # - OBRIGATORIAMENTE tem que começar com a letra da rodada
            if resp != "---" and len(resp) >= 2 and resp.startswith(letra.upper()):
                contagem[resp] = contagem.get(resp, 0) + 1
        
        # Atribui pontos (3 para única, 1 para duplicada, 0 se não cumpriu as regras)
        for tid in nomes_jogadores:
            resp = respostas_rodada[tid][tema].strip().upper()
            
            if resp != "---" and len(resp) >= 2 and resp.startswith(letra.upper()):
                if contagem[resp] == 1:
                    pontos_por_categoria[tid][tema] = 3
                else:
                    pontos_por_categoria[tid][tema] = 1
            else:
                pontos_por_categoria[tid][tema] = 0  # Falhou em qualquer regra = ZERO pontos

    # 2. Formatação do Texto de Saída
    msg = "\n==================================="
    msg += "\n        RESPOSTAS DA RODADA        "
    msg += "\n===================================\n"
    for tema in temas:
        msg += f"\nCategoria {tema}:\n"
        linha_respostas = []
        for tid, nome in nomes_jogadores.items():
            linha_respostas.append(f"{nome}: {respostas_rodada[tid][tema]}")
        msg += "  |  ".join(linha_respostas) + "\n"
    
    msg += "\n==================================="
    msg += "\n             PONTUACAO             "
    msg += "\n===================================\n"
    for tema in temas:
        msg += f"\nCategoria {tema}:\n"
        linha_pontos = []
        for tid, nome in nomes_jogadores.items():
            linha_pontos.append(f"{nome}: +{pontos_por_categoria[tid][tema]} pontos")
        msg += "  |  ".join(linha_pontos) + "\n"
    
    # 3. Soma na pontuação Total Acumulada
    for tid in nomes_jogadores:
        for tema in temas:
            pontos_totais[tid] += pontos_por_categoria[tid][tema]
    
    msg += "\n==================================="
    msg += "\n     PONTUACAO TOTAL ACUMULADA     "
    msg += "\n===================================\n"
    for tid, nome in nomes_jogadores.items():
        msg += f"{nome}: {pontos_totais[tid]} pontos\n"
    
    resultado_formatado = msg

def atender_cliente(conn, addr, tid):
    # Identificação
    nome = conn.recv(1024).decode()
    with lock_dados:
        nomes_jogadores[tid] = nome
        pontos_totais[tid] = 0
    print(f"[Servidor] Jogador conectado: {nome}")
    
    for r in range(1, N_RODADAS + 1):
        # Aguarda liberar o início
        semaforo_inicio.acquire()
        conn.sendall(f"LETRA:{letra_sorteada}".encode())

        resps_do_cliente = {}
        for tema in temas:
            dado = conn.recv(1024).decode()
            t, resp = dado.split(":", 1)
            resps_do_cliente[t] = resp
        
        with lock_dados:
            respostas_rodada[tid] = resps_do_cliente
        
        # Sinaliza que este cliente terminou de enviar
        semaforo_respostas.release()
        
        # Aguarda o servidor mestre calcular tudo
        semaforo_resultados.acquire()

        # Envia a string gigante formatada
        conn.sendall(resultado_formatado.encode())
        
        # Aguarda o jogador digitar "ok" para seguir
        conn.recv(1024)
        semaforo_pronto.release()
    
    conn.close()

def iniciar_servidor():
    global letra_sorteada
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Aguardando {N_JOGADORES} jogadores conectarem...\n")

    for i in range(N_JOGADORES):
        conn, addr = server.accept()
        threading.Thread(target=atender_cliente, args=(conn, addr, i)).start()

    # Fluxo principal das Rodadas
    for r in range(1, N_RODADAS + 1):
        while len(nomes_jogadores) < N_JOGADORES: pass # Aguarda login
        
        letra_sorteada = random.choice("ABCDEFGIJKLMNOPQRSTUV")
        print(f"\n[RODADA {r}] Iniciada. Letra sorteada: {letra_sorteada}")
        
        # Libera os clientes para jogarem
        for _ in range(N_JOGADORES): semaforo_inicio.release()
        
        # Aguarda todos terminarem de preencher as categorias
        for _ in range(N_JOGADORES): semaforo_respostas.acquire()
        
        # Calcula e cria a string de resultados
        gerar_resultados_da_rodada(letra_sorteada)
        
        # Libera os clientes para verem o resultado
        for _ in range(N_JOGADORES): semaforo_resultados.release()
        
        # Aguarda todos darem OK no terminal
        for _ in range(N_JOGADORES): semaforo_pronto.acquire()
        
        print(f"[RODADA {r}] Concluida.")

    print("\nFim de Jogo! Servidor encerrando.")
    server.close()

if __name__ == "__main__":
    iniciar_servidor()