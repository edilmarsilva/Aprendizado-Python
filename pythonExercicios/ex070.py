"""Crie um programa que leia o nome e o preço de vários produtos.
O programa deverá perguntar se o usuário vai continuar ou não.
No final, mostre:
A) qual é o total gasto na compra.
B) quantos produtos custam mais de R$1000.
C) qual é o nome do produto mais barato."""
from time import sleep
print('\033[35m-*\033[m' * 15)
print('\033[1;33m   Estatísticas em produtos ')
print('\033[35m-*\033[m' * 15)
print('\033[36m=\033[m' * 40)
print('{:-^38}'.format('LOJAS TABAJARA'))
print('\033[36m=\033[m' * 40)
total = mais1000 = barato = cont = 0
while True:
    produto = str(input('\033[1;34mNome do Produto: '))
    preco = float(input('Preço: R$ '))
    resp = ' '
    while resp not in 'SN':
        resp = str(input('\033[35mQuer continuar: [S/N] ')).strip().upper()[0]
    cont += 1
    total += preco
    if preco > 1000:
        mais1000 += 1
    if cont == 1 or preco < barato:
        barato = preco
        prodbarato = produto
    if resp == 'N':
        break
print('\033[36m=\033[m' * 40)
print('{:-^50}'.format('\033[1;33mCALCULANDO AS COMPRAS\033[m'))
sleep(2)
print(f'\033[1mTOTAL DAS COMPRAS {cont} ITENS R$ {total:.2f}')
print(f'Temos {mais1000} produtos custando acima de R$ 1.000,00')
print(f'O produto mais barato foi a {prodbarato} que custa R$ {barato:.2f}')
print('\033[36m=\033[m' * 40)
