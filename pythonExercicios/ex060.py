"""Faça um programa que leia um número qualquer e mostre o seu fatorial. Exemplo:
5! = 5 x 4 x 3 x 2 x 1 = 120"""
print('\033[36m-=' * 20)
print('\033[31m      Cálculo do Fatorial')
print('\033[36m-=' * 20)
print('\033[32mImportando a função FACTORIAL')
from math import factorial
n = int(input('\033[1;34mDigite um número para calcular seu fatorial: '))
f = factorial(n)
print('\033[36m=\033[m' * 30)
print(''f'O fatorial de {n} é {f}.')
print('\033[36m=\033[m' * 30)
print('\033[32mModo Tradicional')
num = int(input('''\033[1;34mVamos calcular um FATORIAL
Digite um número: '''))
c = num
f = 1
print('\033[36m=\033[m' * 40)
print(''f'\033[1mCalculando {num}! ', end='')
while c > 0:
    print(''f'{c}', end='')
    if c > 1:
        print(' x ', end='')
    else:
        print(' = ', end='')
    f *= c
    c -= 1
print(''f'{f}')
print('\033[36m=\033[m' * 40)
print('\033[32mDESAFIO - Utilizando \033[4mFOR\033[m')
num = int(input('\033[1;34mDigite um número: '))
c = num
f = 1
print('\033[36m=\033[m' * 40)
print(''f'\033[1mCalculando {num}! ', end='')
for c in range(num, 0, -1):
    print(''f'{c}', end='')
    if c > 1:
        print(' x ', end='')
    else:
        print(' = ', end='')
    f *= c
    c -= 1
print(''f'{f}')
print('\033[36m=\033[m' * 40)
