"""Crie um programa que leia nome, ano de nascimento e carteira de trabalho e
cadastre-o (com idade) em um dicionário. Se por acaso a CTPS for diferente de ZERO,
o dicionário receberá também o ano de contratação e o salário. Calcule e acrescente,
além da idade, com quantos anos a pessoa vai se aposentar."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Cadastro de Trabalhador em Python":^50}')
print('\033[35m-*\033[m' * 25)
from datetime import date
cadastro = {}
cadastro['nome'] = str(input('\033[1;33mNOME: '))
ano = int(input('Ano de Nascimento: '))
cadastro['idade'] = date.today().year - ano
cadastro['ctps'] = int(input('Carteira de Trabalho (0 não tem): '))
if cadastro['ctps'] != 0:
    cadastro['contratacao'] = int(input('Ano de Contratação: '))
    cadastro['salario'] = float(input('Salário: R$ '))
    cadastro['aposentadoria'] = cadastro['idade'] + cadastro['contratacao'] + 35 - date.today().year
    print('\033[1;35m-=\033[m' * 25)
for k, v in cadastro.items():
    print(f'\033[1m- {k} tem o valor {v}.')
print('\033[1;35m-=\033[m' * 25)
