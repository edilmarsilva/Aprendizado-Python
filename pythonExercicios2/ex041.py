"""
Classificando Atletas
A Confederação Nacional de Natação precisa de um programa que leia o ano de nascimento de um atleta
e mostre a sua categoria, conforme a idade:

– Até 9 anos:-MIRIM

– Até 14 anos: INFANTIL

– Até 19 anos: JÚNIOR

– Até 25 anos: SÉNIOR

– Acima de 25 anos: MASTER
"""
from datetime import date
from time import sleep

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Classificando Atletas":^40}')
print('\033[1;33m-=\033[m' * 20)

nome = str(input('\033[1mDigite seu nome: ')).strip()
nasc = int(input('Em que ano você nasceu? '))
idade = date.today().year - nasc

print('\033[36m=\033[m' * 50)
print(f'{nome} aguarde um instante, estou verificando sua categoria...')
sleep(3)
if idade <= 9:
    print(f'\033[1mCategoria MIRIM, com {idade} anos de idade.')
elif 9 < idade <= 14:
    print(f'\033[1mCategoria INFANTIL, com {idade} anos de idade.')
elif 14 < idade <= 19:
    print(f'\033[1mCategoria JÚNIOR, com {idade} anos de idade.')
elif 19 < idade <= 25:
    print(f'\033[1mCategoria SÊNIOR, com {idade} anos de idade.')
elif idade > 25:
    print(f'\033[1mCategoria MASTER, com {idade} anos de idade.')
print('\033[35mSEJA BEM VINDO!!!')
print('\033[36m=\033[m' * 50)
