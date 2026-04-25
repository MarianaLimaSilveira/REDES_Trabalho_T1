# Trabalho de Redes - Jogo STOP Distribuído

## Como executar o projeto

Para rodar o jogo corretamente, você precisará abrir múltiplos terminais (Prompt de Comando ou PowerShell). A ordem de execução é muito importante.

### Passo 1: Iniciar o Servidor
1. Abra o primeiro terminal.
2. Navegue até a pasta onde estão os arquivos do código.
3. Execute o servidor com o comando:
   `python servidor.py`
4. O terminal mostrará uma mensagem informando que está aguardando os jogadores se conectarem. Deixe esta janela aberta.

### Passo 2: Iniciar os Clientes (Jogadores)
1. Abra um novo terminal para o **Jogador 1**.
2. Execute o cliente com o comando:
   `python cliente.py`
3. Digite o nome do primeiro jogador.
4. Abra outro terminal para o **Jogador 2**.
5. Execute o cliente novamente:
   `python cliente.py`
6. Digite o nome do segundo jogador.

*Nota: O jogo foi configurado por padrão para 2 jogadores (variável `N_JOGADORES` no servidor). O jogo só começará e sorteará a primeira letra quando os 2 jogadores estiverem conectados.*

### Passo 3: Jogando
- Quando a rodada iniciar, a letra sorteada aparecerá na tela.
- Digite sua resposta para cada categoria e aperte `ENTER`. Se não souber a palavra, aperte `ENTER` deixando vazio.
- O servidor aguardará todos os jogadores enviarem suas respostas antes de calcular e exibir a pontuação na tela de todos.