"""Crie um programa onde 4 jogadores joguem um dado e tenham resultados aleatórios.
Guarde esses resultados em um dicionário em Python.
No final, coloque esse dicionário em ordem, sabendo que o vencedor
tirou o maior número no dado."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Jogo de Dados em Python":^50}')
print('\033[35m-*\033[m' * 25)
from random import randint
from time import sleep
from operator import itemgetter
resultados = {}
ranking = []
for c in range(1, 5):
    resultados[f'jogador{c}'] = int(randint(1, 6))
print('\033[1;35m-=\033[m' * 25)
print('\033[1;35m===VALORES SORTEADOS===\033[1m')
for k, v in resultados.items():
    print(f'\033[1m{k} tirou {v} no dado.')
    sleep(1)
print('\033[1;35m-=\033[m' * 25)
print('\033[1;35===RANKING DOS JOGADORES===')
ranking = sorted(resultados.items(), key=itemgetter(1), reverse=True)
for i, v in enumerate(ranking):
    print(f'\033[1m{i + 1}º lugar: {v[0]} com {v[1]}')
    sleep(1)
print('\033[1;35m-=\033[m' * 25)
