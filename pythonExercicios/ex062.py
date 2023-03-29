"""Melhore o DESAFIO 61, perguntando para o usuário se ele quer mostrar
mais alguns termos.
O programa encerrará quando ele disser que quer mostrar 0 termos."""
print('\033[36m-=' * 20)
print('\033[31m      Super Progressão Aritmética v3.0')
print('\033[36m-=' * 20)
primeiro = int(input('\033[1;34mDigite o primeiro TERMO: '))
razao = int(input('Qual a RAZÃO: '))
cont = 1
total = 0
novotermo = 10
print('\033[36m=\033[m' * 70)
while novotermo != 0:
    total += novotermo
    while cont <= total:
        print(''f'\033[1m{primeiro}', end='')
        if cont < total:
            print(' → ', end='')
        else:
            print(' PAUSA ')
        primeiro += razao
        cont += 1
    print('\033[36m=\033[m' * 70)
    novotermo = int(input('Quantos termos você quer mostrar a mais? '))
print(''f'Progressão finalizada com {total} termos mostrados.')
