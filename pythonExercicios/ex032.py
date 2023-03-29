"""Faça um programa que leia um ano qualquer e mostre se ele é bissexto."""
print('\033[36m-=' * 20)
print('\033[31m         ANO BISSEXTO')
print('\033[36m-=' * 20)
from datetime import date
ano = int(input('\033[1;34mDigite um ano qualquer ou coloque 0 para analisar o ano atual: '))
print('\033[36m=\033[m' * 50)
if ano == 0:
    ano = date.today().year
if ano % 4 == 0 and ano % 100 != 0 or ano % 400 == 0:
    print('\033[1mO ano {} é um ano BISSEXTO'.format(ano))
else:
    print('\033[1mO ano {} não é um ano BISSEXTO'.format(ano))
print('\033[36m=\033[m' * 50)
