"""
Faça um programa que leia o ano de nascimento de um jovem e informe, de acordo com a sua idade,
se ele ainda vai se alistar ao serviço militar, se é a hora exata de se alistar
ou se já passou do tempo do alistamento. Seu programa também deverá mostrar
o tempo que falta ou que passou do prazo.
"""

from datetime import date

nome = str(input('Informe seu nome: '))
ano = int(input('Ano de Nascimento: '))
idade = date.today().year - ano

if idade < 18:
    print(f'{nome} está cedo para seu alistamento.')
    print(f'Procure uma JUNTA MILITAR daqui {18 - idade} anos.')
elif idade == 18:
    print(f'{nome} chegou a hora de se alistar, dirija-se até a JUNTA MILITAR IMEDIATAMENTE.')
else:
    print(f'{nome} espero que já tenha se alistado, pois deveria ter se alistado {idade - 18} anos atrás.')
print('OBRIGADO POR SERVIR O PAÍS')
