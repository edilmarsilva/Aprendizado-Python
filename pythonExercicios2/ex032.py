"""
Ano Bissexto
Faça um programa que leia um ano qualquer e mostre se ele é bissexto.
"""
print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Ano Bissexto":^40}')
print('\033[1;33m-=\033[m' * 20)

from datetime import date

ano = int(input('Digite um ano qualquer ou 0 para o ano atual: '))
if ano == 0:
    ano = date.today().year
if ano % 4 == 0 and ano % 100 != 0 or ano % 400 == 0:
    print(f'O ano {ano} é BISSEXTO.')
else:
    print(f'O ano {ano} não é BISSEXTO.')
