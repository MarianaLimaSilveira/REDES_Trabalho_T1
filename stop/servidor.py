import random
import socket
import threading

#Configuração (Setup)
HOST = "0.0.0.0"
PORT = 9002

N_JOGADORES = 2 
N_RODADAS = 3

clientes_conectados = []
threads_jogadores = []

letras_sorteaveis = "ABCDEFGIJLMNOPQRSTUV"
letra_sorteada = "" # Variável global para armazenar a letra da rodada

semaforo_mensagens = threading.Semaphore(1)
evento_largada = threading.Event()


def atender_cliente(conn, addr, tid):
    """
    Função executada por cada Thread. Gerencia a partida para um jogador específico.
    """
    global letra_sorteada
    print(f"[Thread {tid}] Iniciada para o jogador {addr}. Aguardando os outros...")
    
    # A thread pausa aqui e só continua quando o servidor fizer: evento_largada.set()
    evento_largada.wait() 
    
    # Mensagens combinadas para evitar o "Engarrafamento" do TCP
    mensagem_inicio = f"O jogo comecou! A letra desta rodada e: {letra_sorteada}"
    conn.sendall(mensagem_inicio.encode())
    
    # Mantendo a thread viva por enquanto para você não ter erros de execução
    pass 


def iniciar_servidor():
    """
    Função principal que inicia o socket e gerencia a Sala de Espera.
    """
    global letra_sorteada
    print("--- Iniciando Servidor de STOP ---")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Permite reutilizar a porta imediatamente se o servidor cair ou for reiniciado
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        
        print(f"[Servidor] Ouvindo em {HOST}:{PORT}")
        print(f"[Servidor] Aguardando {N_JOGADORES} jogadores se conectarem...\n")

        # Sala de espera
        for i in range(N_JOGADORES):
            conn, addr = server.accept()
            clientes_conectados.append((conn, addr))
            
            print(f"[Servidor] Jogador {i+1}/{N_JOGADORES} conectado: {addr}")
            
            # Criamos a thread passando a conexão, o endereço e agora o ID correto (i)
            thread = threading.Thread(target=atender_cliente, args=(conn, addr, i), daemon=True)
            threads_jogadores.append(thread)
            
            # Inicia a thread
            thread.start()

        print("\n[Servidor] Todos os jogadores conectados! Sala de espera fechada.")
        
        # Sorteia a letra uma única vez para todos os jogadores
        letra_sorteada = random.choice(letras_sorteaveis)
        print(f"[Servidor] A letra sorteada para a rodada foi: {letra_sorteada}")
        
        # Libera todas as threads que estavam pausadas no wait()
        evento_largada.set()
       
        for thread in threads_jogadores:
            thread.join()

if __name__ == "__main__":
    iniciar_servidor()