"""Aprimore o desafio 93 para que ele funcione com vários
jogadores, incluindo um sistema de visualização de
detalhes do aproveitamento de cada jogador."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Aprimorando os Dicionários":^50}')
print('\033[35m-*\033[m' * 25)
time = []
aproveitamento = {}
gol = []
while True:
    gol.clear()
    aproveitamento['nome'] = str(input('\033[1;33mJOGADOR: '))
    partidas = int(input(f'Quantas partidas {aproveitamento["nome"]} jogou? '))
    for c in range(0, partidas):
        gol.append(int(input(f'     Quantos gols na partida {c + 1}? ')))
    aproveitamento['gols'] = gol[:]
    aproveitamento['total'] = sum(gol)
    time.append(aproveitamento.copy())
    while True:
        resp = str(input('Quer continuar? [S/N] ')).strip().upper()[0]
        if resp in 'SN':
            break
    if resp == 'N':
        break
print('\033[1;35m-=\033[m' * 25)
print(f'\033[1m{"COD":<5}', end='')
for i in aproveitamento.keys():
    print(f'\033[1m{i:<15}', end='')
print()
print('\033[1;35m-=\033[m' * 25)
for k, v in enumerate(time):
    print(f'\033[1m{k:>3} ', end='')
    for d in v.values():
        print(f'\033[1m{str(d):<15}', end='')
    print()
print('\033[1;35m-=\033[m' * 25)
while True:
    busca = int(input('\033[1mMostrar os dados de qual jogador?(999 para parar) '))
    if busca == 999:
        break
    if busca >= len(time):
        print(f'\033[1;33mERRO! Não existe jogador com o código {busca}!')
    else:
        print(f'\033[1m-- LEVANTAMENTO DO JOGADOR {time[busca]["nome"]}:')
        for i, g in enumerate(time[busca]['gols']):
            print(f'\033[1m    No jogo {i + 1} fez {g} gols.')
    print('\033[1;35m-=\033[m' * 25)
print('\033[1;35m<<< VOLTE SEMPRE >>>\033[m')
