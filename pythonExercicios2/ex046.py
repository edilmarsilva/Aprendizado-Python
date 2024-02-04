"""
Contagem regressiva
Faça um programa que mostre na tela uma contagem regressiva para o estouro de fogos de artifício,
indo de 10 até 0, com uma pausa de 1 segundo entre eles.
"""

from time import sleep

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Contagem regressiva ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

print('\033[36m=\033[m' * 42)
for c in range(10, 0 - 1, -1):
    print(f'{c}', end=' - ')
    sleep(0.7)
print()
print('\033[36m=\033[m' * 42)
