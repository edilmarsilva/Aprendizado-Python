"""Crie um programa que vai gerar cinco números aleatórios e
colocar em uma tupla. Depois disso, mostre a listagem de
números gerados e também indique o menor e o maior valor
que estão na tupla."""
print('\033[35m-*\033[m' * 25)
print('\033[1;33m{:-^50}'.format('Maior e menor valores em Tupla'))
print('\033[35m-*\033[m' * 25)
from random import randint
print('\033[35m-=\033[m' * 25)
num = randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10), \
      randint(1, 10)
print('\033[1mOs números sorteados foram: ', end='')
for n in num:
    print(f'{n} ', end='')
print(f'\n\033[1mO maior número sorteado foi: {max(num)}')
print(f'E o menor número sorteado foi: {min(num)}')
print('\033[35m-=\033[m' * 25)