"""Faça um programa que ajude um jogador da MEGA SENA a criar palpites.
O programa vai perguntar quantos jogos serão gerados
e vai sortear 6 números entre 1 e 60 para cada jogo,
cadastrando tudo em uma lista composta."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"PALPITES DA MEGA-SENA":^50}')
print('\033[35m-*\033[m' * 25)
palpites = []
dados = []
from random import randint
from time import sleep
resp = int(input('\033[1;33mQuantos jogos deseja gerar: '))
tot = 1
while tot <= resp:
    cont = 0
    while True:
        num = (randint(1, 60))
        if num not in dados:
            dados.append(num)
            cont += 1
        if cont >= 6:
            break
    palpites.append(dados[:])
    dados.clear()
    tot += 1
print('\033[1;35m-=\033[m' * 25)
print(f'\033[1;36m{f"SORTEANDO {resp} JOGOS":^50}\033[m')
for c in range(0, len(palpites)):
    palpites[c].sort()
    print(f'\033[1mJOGO {c + 1}: {palpites[c]}')
    sleep(1.0)
print(f'\033[1;32m{"BOA SORTE":^50}')
print('\033[1;35m-=\033[m' * 25)
