"""Crie um programa que leia a idade e o sexo de várias pessoas.
A cada pessoa cadastrada, o programa deverá perguntar
se o usuário quer ou não continuar. No final, mostre:
A) quantas pessoas tem mais de 18 anos.
B) quantos homens foram cadastrados.
C) quantas mulheres tem menos de 20 anos."""
print('\033[35m-*\033[m' * 15)
print('\033[1;33m   Análise de dados do grupo ')
print('\033[35m-*\033[m' * 15)
maiores = homem = mulher20 = tot = 0
while True:
    print('\033[36m#\033[m' * 25)
    print('\033[1;32m   CADASTRE UMA PESSOA')
    print('\033[36m#\033[m' * 25)
    idade = int(input('\033[1;34mIdade: '))
    sexo = ' '
    while sexo not in 'MF':
        sexo = str(input('\033[1;34mSexo: [M/F] ')).strip().upper()[0]
    tot += 1
    if idade >= 18:
        maiores += 1
    if sexo == 'M':
        homem += 1
    if sexo == 'F' and idade < 20:
        mulher20 += 1
    resp = ' '
    while resp not in 'SN':
        resp = str(input('\033[35mQuer continuar cadastrando: [S/N] ')).strip().upper()[0]
    if resp == 'N':
        break
print('\033[35m#-\033[m' * 30)
print(f'\033[1mAo todo foram cadastradas {tot} PESSOAS.')
print(f'\033[1mTemos um total de {maiores} pessoas cadastradas com mais de 18 anos.')
print(f'Foram cadastradados {homem} homens.')
print(f'E {mulher20} mulheres com menos de 20 anos.')
print('\033[35m#-\033[m' * 30)
