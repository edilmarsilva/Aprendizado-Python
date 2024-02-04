"""
Grupo da Maioridade
Crie um programa que leia o ano de nascimento de sete pessoas.
No final, mostre quantas pessoas ainda não atingiram a maioridade e quantas já são maiores.
"""

from datetime import date

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Grupo da Maioridade ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

maior = 0
menor = 0

print('\033[36m=\033[m' * 42)
for c in range(1, 8):
    ano = int(input(f'Digite o ano de nascimento da {c}ª PESSOA: '))
    if date.today().year - ano < 18:
        menor += 1
    else:
        maior += 1

print(f'A lista contém {maior} pessoas de maior e {menor} pessoas menores de idade.')
print('\033[36m=\033[m' * 42)
