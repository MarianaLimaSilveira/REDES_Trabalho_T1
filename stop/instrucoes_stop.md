# Instruções - Jogo de STOP (Sistemas Distribuídos)

Pra rodar o jogo , você vai precisar abrir alguns terminais (pode ser o CMD ou o PowerShell) e seguir essa ordem aqui pra não dar erro de conexão:

### 1. Ligando o Servidor
O primeiro passo é abrir um terminal na pasta do projeto e ligar o "cérebro" do jogo. 
- Digite: `python servidor.py`
- Ele vai avisar que está esperando os jogadores entrarem. Deixe essa janela aberta no canto, ela que controla toda a lógica.

### 2. Entrando com os Jogadores
Agora, pra cada jogador que for entrar, você abre um novo terminal separado. 
- No terminal do Jogador 1, digite: `python cliente.py` e coloque o nome dele.
- No terminal do Jogador 2, faça a mesma coisa: `python cliente.py` e coloque o nome.
*OBS: O código tá configurado pra começar quando tiver 2 jogadores (é possível mudar isso na variável N_JOGADORES no servidor), então o jogo só sorteia a letra quando o segundo player conectar.*

### 3. Como o jogo funciona
Assim que a letra aparecer, é só ir digitando as respostas de cada categoria e dar ENTER. 
- Se não souber alguma, pode dar ENTER com tudo vazio que o sistema entende como pulado.
- O servidor só calcula os pontos depois que todo mundo responder, então se a tela "travar" um pouco, é só esperar o outro jogador terminar de digitar. No fim de cada rodada, aparece uma mensagem com o placar atualizado.