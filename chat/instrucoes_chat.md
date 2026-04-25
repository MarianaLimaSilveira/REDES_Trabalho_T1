# Instruções - Grupo de Mensagens

Para esse trabalho, a exigência era de não usar telas divididas no console. Por isso, o sistema separa o cliente em dois scripts diferentes: um que serve só pra receber as mensagens e outro que serve só pra enviar.

Pra testar com um usuário só, é preciso abrir **três terminais** e seguir esse passo a passo:

### Passo 1: Abrir o Servidor
Primeiro, abre um terminal e roda o servidor central:
- Comando: `python servidor.py`
- Ele que faz o "meio de campo" e manda as mensagens pra todo mundo. Pode deixar ele rodando quietinho lá.

### Passo 2: A tela de leitura (Quem recebe)
Abre um segundo terminal e roda o script de recepção:
- Comando: `python cliente_receber.py`
- Essa janela aqui você não vai usar pra digitar nada. Ela serve só pra você ficar de olho no que o pessoal tá escrevendo no grupo. É bom deixar ela bem visível.

### Passo 3: A tela de envio (Quem escreve)
Por último, abre o terceiro terminal pra ser a sua "mão" no chat:
- Comando: `python cliente_enviar.py`
- Ele vai pedir seu nome e depois disso é só sair digitando. Toda vez que você der ENTER aqui, o texto vai aparecer formatado lá no terminal de leitura (aquele do Passo 2).

*Se quiser simular mais pessoas conversando, é só ir abrindo mais terminais de envio e recepção. O servidor vai tratar cada um como um cliente novo e fazer o broadcast pra todo mundo.*