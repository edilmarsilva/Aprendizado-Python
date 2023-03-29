"""Crie um programa que leia nome, sexo e idade de várias
pessoas, guardando os dados de cada pessoa em um dicionário e
todos os dicionários em uma lista. No final, mostre:
A) Quantas pessoas foram cadastradas
B) A média de idade
C) Uma lista com as mulheres
D) Uma lista de pessoas com idade acima da média"""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Unindo dicionários e listas":^50}')
print('\033[35m-*\033[m' * 25)
galera = []
pessoa = {}
soma = media = 0
while True:
    pessoa.clear()
    pessoa['nome'] = str(input('\033[1;33mNOME: '))
    while True:
        pessoa['sexo'] = str(input('SEXO: [M/F]')).strip().upper()[0]
        if pessoa['sexo'] in 'MF':
            break
        print('\033[1;31mERRO! Por favor digite apenas M ou F\033[1;33m')
    pessoa['idade'] = int(input('IDADE: '))
    soma += pessoa['idade']
    galera.append(pessoa.copy())
    while True:
        resp = str(input('Quer continuar? [S/N] ')).strip().upper()[0]
        if resp in 'SN':
            break
        print('\033[1;31mERRO! Responda apenas S ou N.\033[1;33m')
    if resp == 'N':
        break
print('\033[1;35m-=\033[m' * 25)
print(galera)
print('\033[1;35m-=\033[m' * 25)
print(f'\033[1mA) Ao todo temos {len(galera)} pessoas cadastradas.')
print('\033[1;35m-=\033[m' * 25)
media = soma / len(galera)
print(f'\033[1mB) A média de idade é de {media:5.2f} anos.')
print('\033[1;35m-=\033[m' * 25)
print('\033[1mC) As mulheres cadastradas foram ', end='')
for p in galera:
    if p["sexo"] == 'F':
        print(f'{p["nome"]}', end=' ')
print()
print('\033[1;35m-=\033[m' * 25)
print('\033[1mD) Listas das pessoas que estão acima da média: ')
for p in galera:
    if p["idade"] >= media:
        print('     ', end='')
        for k, v in p.items():
            print(f'{k} = {v} ', end='')
        print()
print(f'\033[1;35m{"<<<ENCERRADO>>>":^50}')
print('\033[1;35m-=\033[m' * 25)
