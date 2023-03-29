"""Faça um programa que leia nome e média de um aluno, guardando também a
situação em um dicionário. No final, mostre o conteúdo da estrutura na tela."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Dicionário em Python":^50}')
print('\033[35m-*\033[m' * 25)
aluno = {}
aluno['nome'] = str(input('\033[1;34mNOME: '))
aluno['media'] = float(input(f'MÉDIA DE {aluno["nome"]}: '))
print('\033[1;35m-=\033[m' * 25)
if aluno['media'] <= 4.9:
    aluno['situação'] = 'REPROVADO'
elif 5 <= aluno['media'] <= 6.9:
    aluno['situação'] = 'EM RECUPERAÇÃO'
elif aluno['media'] >= 7:
    aluno['situação'] = 'APROVADO'
for k, v in aluno.items():
    print(f'\033[1m- {k} é igual a {v}')
print('\033[1;35m-=\033[m' * 25)
