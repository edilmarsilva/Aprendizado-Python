"""
Alistamento Militar
Faça um programa que leia o ano de nascimento de um jovem e informe, conforme a sua idade,
se ele ainda vai se alistar ao serviço militar, se é a hora exata de se alistar
ou se já passou do tempo do alistamento.
O seu programa também deverá mostrar o tempo que falta ou que passou do prazo.
"""
from datetime import date

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Alistamento Militar":^40}')
print('\033[1;33m-=\033[m' * 20)

nasc = int(input('Qual o ano do seu nascimento: '))
idade = date.today().year - nasc
print('\033[36m=\033[m' * 50)
if idade < 18:
    print(f'Ainda não é o momento de se alistar, faltam {18 - idade} anos para seu alistamento')
    print(f'Procure uma JUNTA MILITAR em {nasc + 18}')
elif idade == 18:
    print(f'Parabéns! Você tem ou completará 18 anos nesse ano, procure a JUNTA MILITAR de sua cidade ')
elif idade > 18:
    print(f'Avante soldado, você deveria ter se alistado {date.today().year - (nasc + 18)} anos atrás.')
    print(f'Você deveria ter se alistado em  {nasc + 18}')
print('\033[36m=\033[m' * 50)
