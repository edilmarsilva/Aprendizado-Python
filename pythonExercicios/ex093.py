"""Crie um programa que gerencie o aproveitamento de um
jogador de futebol. O programa vai ler o nome do jogador e
quantas partidas ele jogou. Depois vai ler a quantidade
de gols feitos em cada partida. No final, tudo isso
será guardado em um dicionário, incluindo o total de gols feitos
durante o campeonato."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Cadastro de Jogador de Futebol":^50}')
print('\033[35m-*\033[m' * 25)
aproveitamento = {}
gol = []
aproveitamento['nome'] = str(input('\033[1;33mJOGADOR: '))
partidas = int(input(f'Quantas partidas {aproveitamento["nome"]} jogou? '))
for c in range(0, partidas):
    gol.append(int(input(f'     Quantos gols na partida {c + 1}? ')))
aproveitamento['gols'] = gol[:]
aproveitamento['total'] = sum(gol)
print('\033[1;35m-=\033[m' * 25)
print(aproveitamento)
print('\033[1;35m-=\033[m' * 25)
for k, v in aproveitamento.items():
    print(f'\033[1mO campo {k} tem o valor {v}')
print('\033[1;35m-=\033[m' * 25)
print(f'\033[1mO jogador {aproveitamento["nome"]} jogou {len(aproveitamento["gols"])} partidas.')
for c in range(0, partidas):
    print(f'    ==> Na partida {c + 1}, fez {gol[c]} gols')
print(f'Foi um total de {aproveitamento["total"]} gols.')
print('\033[1;35m-=\033[m' * 25)
