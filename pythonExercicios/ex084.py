"""Faça um programa que leia nome e peso de várias pessoas, guardando tudo em uma lista.
No final, mostre:
A) Quantas pessoas foram cadastradas.
B) Uma listagem com as pessoas mais pesadas.
C) Uma listagem com as pessoas mais leves."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Lista composta e análise de dados":^50}')
print('\033[35m-*\033[m' * 25)
pessoas = []
dados = []
pesadas = leves = 0
while True:
    resp = ' '
    dados.append(str(input('\033[1;34mNOME: ')))
    dados.append(float(input('PESO: KG ')))
    if len(pessoas) == 0:
        pesadas = leves = dados[1]
    else:
        if dados[1] > pesadas:
            pesadas = dados[1]
        if dados[1] < leves:
            leves = dados[1]
    pessoas.append(dados[:])
    dados.clear()
    while resp not in 'SN':
        resp = str(input('\033[1;35mQuer continuar? [S/N] ')).strip().upper()[0]
    if resp == 'N':
        break
print('\033[1;35m-=\033[m' * 30)
print(f'\033[1mForam cadastradas {len(pessoas)} pessoas no total.')
print(f'O maior peso foi de {pesadas} Peso de ', end='')
for p in pessoas:
    if p[1] == pesadas:
        print(f'{p[0]} ... ', end='')
print()
print(f'O menor peso foi de {leves} Peso de ', end='')
for p in pessoas:
    if p[1] == leves:
        print(f'{p[0]} ... ', end='')
print()
print('\033[1;35m-=\033[m' * 30)
