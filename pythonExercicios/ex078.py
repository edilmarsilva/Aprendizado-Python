"""Faça um programa que leia 5 valores numéricos e guarde-os em uma lista.
No final, mostre qual foi o maior e o menor valor digitado e as suas
respectivas posições na lista."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Maior e Menor valores na Lista":^50}')
print('\033[35m-*\033[m' * 25)
num = []
maior = menor = 0
for c in range(0, 5):
    num.append(int(input(f'\033[1;34mDigite um valor na posição {c}: ')))
    if c == 0:
        maior = menor = num[c]
    else:
        if num[c] > maior:
            maior = num[c]
        if num[c] < menor:
            menor = num[c]
print('\033[35m-=\033[m' * 25)
print(f'\033[1mOs números digitados foram {num}')
print(f'O maior número digitado foi {maior} nas posições ', end='')
for i, v in enumerate(num):
    if v == maior:
        print(f'{i} ...', end='')
print()
print(f'O menor número digitado foi {menor} nas posições ', end='')
for i, v in enumerate(num):
    if v == menor:
        print(f'{i} ...', end='')
print()
print('\033[35m-=\033[m' * 25)
