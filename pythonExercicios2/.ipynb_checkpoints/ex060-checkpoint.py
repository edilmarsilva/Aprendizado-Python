"""
Cálculo do Fatorial
Faça um programa que leia um número qualquer e mostre o seu fatorial. Exemplo:

5! = 5 x 4 x 3 x 2 x 1 = 120
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Cálculo do Fatorial ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

num = int(input('Digite um número para calcular seu fatorial: '))
c = num
fat = 1
print(f'Calculando o fatorial de {num}! = ', end='')
while c > 0:
    print(f'{c}', end='')
    if c > 1:
        print(' x ', end='')
    else:
        print(' = ', end='')
    fat = fat * c
    c -= 1
print(fat)
print('\033[36m=\033[m' * 42)
