# Trabalho de Redes - Grupo de Mensagens

## Como executar o projeto

Para atender ao requisito de não utilizar telas divididas no terminal, o cliente foi separado em dois scripts diferentes: um exclusivo para leitura e outro exclusivo para envio. 

Para testar com um único usuário, você precisará abrir **três terminais** separados. Siga a ordem exata abaixo:

### Passo 1: Iniciar o Servidor (Roteador de Mensagens)
1. Abra o primeiro terminal.
2. Execute o servidor central com o comando:
   `python servidor.py`
3. Ele ficará aguardando as conexões. Deixe esta janela minimizada ou num canto da tela.

### Passo 2: Iniciar o Cliente de Leitura (Receptor)
1. Abra o segundo terminal.
2. Execute o script de recebimento com o comando:
   `python cliente_receber.py`
3. Esta janela servirá **apenas** para visualizar o histórico do chat. Posicione-a em um local visível na sua tela e não digite nada nela.

### Passo 3: Iniciar o Cliente de Envio (Remetente)
1. Abra o terceiro terminal.
2. Execute o script de envio com o comando:
   `python cliente_enviar.py`
3. Digite o seu nome de usuário quando for solicitado.
4. A partir de agora, use **apenas este terminal** para digitar e enviar suas mensagens. Ao apertar `ENTER`, a mensagem aparecerá automaticamente no terminal de Leitura (Passo 2).

*Para simular uma conversa com mais pessoas, basta abrir novos pares de terminais (um rodando `cliente_receber.py` e outro rodando `cliente_enviar.py`) para cada novo usuário.*