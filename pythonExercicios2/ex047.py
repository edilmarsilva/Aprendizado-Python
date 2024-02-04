"""
Contagem de pares
Crie um programa que mostre na tela todos os números pares que estão no intervalo entre 1 e 50.
"""

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{" Contagem de pares ":+^40}')
print('\033[1;33m-=\033[m' * 20)

for c in range(1, 50 + 1):
    if c % 2 == 0:
        print(f'{c}', end=' ')
print()
print(f'{"ACABOU":^40}')
print('\033[36m=\033[m' * 40)
 