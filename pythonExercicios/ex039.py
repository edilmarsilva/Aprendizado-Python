"""Faça um programa que leia o ano de nascimento de um jovem e informe,
conforme a sua idade, se ele ainda vai se alistar ao serviço militar,
se é a hora exata de se alistar ou se já passou do tempo do alistamento.
O seu programa também deverá mostrar o tempo que falta ou que passou do prazo."""
from datetime import date
from time import sleep
print('\033[36m-=' * 20)
print('\033[31m         JUNTA MILITAR')
print('\033[36m-=' * 20)
nome = str(input('\033[1;34mInforme seu nome: '))
nasc = int(input('Agora informe seu ano de nascimento {}: '.format(nome)))
print('''SEXO
[1] MASCULINO
[2] FEMININO''')
escolha = int(input('OPÇÃO: '))
idade = date.today().year - nasc
if escolha == 1:
    print('\033[31m{} SEU ALISTAMENTO É OBRIGATÓRIO'.format(nome))
else:
    print('\033[32m{} SEU ALISTAMENTO NÃO É OBRIGATÓRIO'.format(nome))
sleep(3)
print('\033[36m=\033[m' * 70)
if idade < 17:
    print('\033[1m{} você tem apenas {} anos de idade e ainda faltam {} anos para se alistar'.format(nome, idade, 17 - idade))
    print('AGUARDAREMOS SUA PRESENÇA NA JUNTA MILITAR em {}. ATÉ LÁ!!!'.format(date.today().year + (17 - idade)))
elif idade == 17:
    print('\033[1mO dever chama soldado. Parabéns pelos 17 anos. Se apresente a JUNTA MILITAR DE SUA CIDADE')
elif idade >= 18:
    print('\033[1mNesse momento você já deve ter se apresentado à \033[4mJUNTA MILITAR\033[m')
    print('\033[35mSua PÁTRIA AGRADECE, OBRIGADO PELO SEU SERVIÇO')
print('\033[36m=\033[m' * 70)
