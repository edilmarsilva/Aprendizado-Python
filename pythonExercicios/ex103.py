"""Faça um programa que tenha uma função chamada ficha(), que receba dois parâmetros
opcionais: o nome de um jogador e quantos gols ele marcou. O programa deverá ser capaz de
mostrar a ficha do jogador, mesmo que algum dado não tenha sido informado corretamente."""
def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)


def ficha(jog='<Desconhecido>', gol=0):
    print(f'O jogador {jog} fez {gol} no campeonato.')


# Programa Principal
titulo('Ficha do Jogador')
n = str(input('Digite o nome do jogador: '))
g = str(input('Número de gols: '))
if g.isnumeric():
    g = int(g)
else:
    g = 0
if n.strip() == '':
    ficha(gol=g)
else:
    ficha(n, g)
