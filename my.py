print('bem-vindo à sua assistente virtual!')

nome = input('Digite seu nome: ').strip()
if nome:
    print(f'Olá, {nome}! Seja bem-vindo!')
else:
    nome = 'usuário'
    print('Olá, usuário! Seja bem-vindo!')

print('Comandos disponíveis: oi, nome, hora, ajuda, sair')

while True:
    comando = input('Digite um comando ou "sair" para encerrar: ').strip().lower()

    if comando == 'sair':
        print('Encerrando a assistente virtual. Até logo!')
        break

    if comando in {'oi', 'olá', 'hello', 'hi'}:
        print(f'Olá, {nome}! Como posso ajudar?')
    elif comando == 'nome':
        print(f'O seu nome é {nome}.')
    elif comando in {'hora', 'horario'}:
        from datetime import datetime
        print(f'Agora são {datetime.now().strftime("%H:%M:%S")}')
    elif comando == 'ajuda':
        print('Comandos disponíveis: oi, nome, hora, ajuda, sair')
    else:
        print(f'Você digitou o comando: {comando}')
        print('Ainda estou aprendendo a responder a esse comando.')
        

