"""Crie um programa que leia nome e duas notas de vários alunos e guarde tudo
em uma lista composta. No final, mostre um boletim contendo a média de cada um e
permita que o usuário possa mostrar as notas de cada aluno individualmente."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Boletim com listas compostas":^50}')
print('\033[35m-*\033[m' * 25)
boletim = []
while True:
    resp = ' '
    nome = str(input('\033[1;34mNOME: '))
    n1 = float(input('NOTA 1: '))
    n2 = float(input('NOTA 2: '))
    media = (n1 + n2) / 2
    boletim.append([nome, [n1, n2], media])
    while resp not in 'SN':
        resp = str(input('\033[1;35mQuer continuar? [S/N] ')).strip().upper()[0]
    if resp == 'N':
        break
print('\033[1;35m-=\033[m' * 25)
print(f'\033[1;36m{"Nº":<4}{"NOME":<10}{"MÉDIA":>8}')
print('\033[1;35m-=\033[m' * 25)
for i, a in enumerate(boletim):
    print(f'\033[1m{i:<4}{a[0]:<10}{a[2]:>8.1f}')
print('\033[1;35m-=\033[m' * 25)
while True:
    opc = int(input('\033[1;33mQuer ver as notas de qual aluno? [999 PARA SAIR] '))
    print('\033[1;35m-=\033[m' * 25)
    if opc <= len(boletim):
        print(f'\033[1mNOTAS DE {boletim[opc][0]} são {boletim[opc][1]}')
        print('\033[1;35m-=\033[m' * 25)
    if opc == 999:
        print('\033[1;32mFINALIZANDO BOLETIM...')
print('<<<VOLTE SEMPRE>>>')
print('\033[1;35m-=\033[m' * 25)
