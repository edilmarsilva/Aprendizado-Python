"""Escreva um programa que leia um número N inteiro qualquer e
mostre na tela os N primeiros elementos de uma Sequência de Fibonacci. Exemplo:
0 – 1 – 1 – 2 – 3 – 5 – 8"""
print('\033[36m-=' * 20)
print('\033[31m      Sequência de Fibonacci v1.0')
print('\033[36m-=' * 20)
termo = int(input('\033[1;34mQuantos termos você quer mostrar? '))
c = 0
primeiro = 0
segundo = 1
proximo = 0
print('\033[36m=\033[m' * 60)
print(''f'\033[1m{primeiro} → {segundo} → ', end='')
while c <= termo + 2:
    proximo = primeiro + segundo
    print(proximo, end='')
    primeiro = segundo
    segundo = proximo
    c += 1
    if c <= termo + 2:
        print(' → ', end='')
    else:
        print(' #ACABOU#')
print(''f'Terminei de mostrar {termo} termos da sequência FINONACCI.')
print('\033[36m=\033[m' * 60)
