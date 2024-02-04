"""
Números primos
Faça um programa que leia um número inteiro e diga se ele é ou não um número primo.
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Números primos ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

cont = 0

num = int(input('Digite um número para verificar se ele é PRIMO: '))

print('\033[36m=\033[m' * 42)
for c in range(1, num + 1):
    if num % c == 0:
        cont += 1
        print(f'\033[4;32m{c}\033[m', end=' ')
    else:
        print(f'\033[31m{c}', end=' ')
print()
if cont == 2:
    print(f'\033[mO número {num} foi divisível {cont} vezes e por isso ele é PRIMO')
else:
    print(f'\033[mO número {num} foi divisível {cont} vezes e por isso ele NÃO é PRIMO')
print('\033[36m=\033[m' * 42)
