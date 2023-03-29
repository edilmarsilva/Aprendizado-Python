"""Desenvolva um programa que leia seis números inteiros e mostre a soma apenas daqueles que forem pares.
Se o valor digitado for ímpar, desconsidere-o."""
print('\033[36m-=' * 20)
print('\033[31m      SOMANDO APENAS OS PARES')
print('\033[36m-=' * 20)
cont = 0
soma = 0
for c in range(1, 7):
    num = int(input('\033[1;34mDigite o {}º número: '.format(c)))
    if num % 2 == 0:
        cont = cont + 1
        soma = soma + num
print('\033[36m=\033[m' * 75)
print('Ao todo foram digitados {} números pares e a soma entre eles é igual a {}'.format(cont, soma))
print('\033[36m=\033[m' * 75)
