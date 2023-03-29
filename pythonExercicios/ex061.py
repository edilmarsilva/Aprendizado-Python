"""Refaça o DESAFIO 51, lendo o primeiro termo e a razão de uma PA,
mostrando os 10 primeiros termos da progressão usando a estrutura while."""
print('\033[36m-=' * 20)
print('\033[31m      Progressão Aritmética v2.0')
print('\033[36m-=' * 20)
primeiro = int(input('\033[1;34mDigite o primeiro TERMO: '))
razao = int(input('Qual a RAZÃO: '))
cont = 1
print('\033[36m=\033[m' * 70)
while cont <= 10:
    print(''f'\033[1m{primeiro}', end='')
    if cont < 10:
        print(' → ', end='')
    else:
        print(' ***ACABOU*** ')
    primeiro += razao
    cont += 1
print('\033[36m=\033[m' * 70)
