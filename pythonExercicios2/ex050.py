"""
Soma dos pares
Desenvolva um programa que leia seis números inteiros e mostre a soma apenas daqueles que forem pares.
Se o valor digitado for ímpar, desconsidere-o.
"""

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{" Soma dos pares ":+^40}')
print('\033[1;33m-=\033[m' * 20)

totpar = 0
cont = 0
for c in range(1, 7):
    num = int(input(f'Digite o {c}° valor: '))
    if num % 2 == 0:
        totpar += num
        cont += 1

print('\033[36m=\033[m' * 40)
print(f'Foram digitados {cont} números pares e a soma entre eles é {totpar}')
print('\033[36m=\033[m' * 40)
