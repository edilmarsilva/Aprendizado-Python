"""Faça um programa que leia o peso de cinco pessoas.
No final, mostre qual foi o maior e o menor peso lidos."""
print('\033[36m-=' * 20)
print('\033[31m           BALANÇA DIGITAL')
print('\033[36m-=' * 20)
maior = 0
menor = 0
for c in range(1, 6):
    peso = float(input('\033[1;34mDigite o peso da {}ª pessoa: '.format(c)))
    if c == 1:
        maior = peso
        menor = peso
    else:
        if peso > maior:
            maior = peso
        if peso < menor:
            menor = peso
print('\033[36m=\033[m' * 40)
print('O maior peso digitado foi de {:.2f} kg'.format(maior))
print('O menor peso digitado foi de {:.2f} kg'.format(menor))
print('\033[36m=\033[m' * 40)
