"""Crie um programa que leia o ano de nascimento de sete pessoas. No final,
mostre quantas pessoas ainda não atingiram a maioridade e quantas já são maiores."""
print('\033[36m-=' * 20)
print('\033[31m           TESTE DE MAIORIDADE')
print('\033[36m-=' * 20)
from datetime import date
maior = 0
menor = 0
for c in range(1, 8):
    anonasc = int(input('\033[1;34mEm que ano a {}ª pessoa nasceu? '.format(c)))
    idade = date.today().year - anonasc
    if idade >= 18:
        maior = maior + 1
    elif idade < 18:
        menor = menor + 1
print('\033[36m=\033[m' * 45)
print('\033[1mAo todo tivemos {} pessoas maiores de idade.'.format(maior))
print('E também tivemos {} pessoas menores de idade.'.format(menor))
print('\033[36m=\033[m' * 45)
