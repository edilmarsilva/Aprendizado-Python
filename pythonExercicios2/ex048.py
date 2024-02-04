"""
Soma ímpares múltiplos de três
Faça um programa que calcule a soma entre todos os números que são múltiplos de três e que se
encontram no intervalo de 1 até 500.
"""

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{" Soma ímpares múltiplos de três ":+^40}')
print('\033[1;33m-=\033[m' * 20)

soma = 0
cont = 0
print('\033[36m=\033[m' * 40)
for c in range(1, 501):
    if c % 3 == 0 and c % 2 == 1:
        soma += c
        cont += 1
print(f'A soma dos {cont} elementos é {soma}')
print('\033[36m=\033[m' * 40)
