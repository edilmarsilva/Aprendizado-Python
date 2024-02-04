"""
Maior e menor da sequência
Faça um programa que leia o peso de cinco pessoas.
No final, mostre qual foi o maior e o menor peso lidos.
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Maior e menor da sequência ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

maior = 0
menor = 0

for c in range(1, 6):
    peso = float(input(f'Digite o peso da {c}ª PESSOA: '))
    if menor == 0 and maior == 0:
        maior = peso
        menor = peso
    else:
        if peso > maior:
            maior = peso
        elif peso < menor:
            menor = peso
print('\033[36m=\033[m' * 42)
print(f'O maior peso digitado foi {maior},\nE o menor peso digitado foi {menor}')
print('\033[36m=\033[m' * 42)
