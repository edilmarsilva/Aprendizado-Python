"""Faça um programa que calcule a faixa de pagamento para horas extras
-De 00 à 25 horas 50%
-De 26 à 40 horas 60%
-De 41 à 60 horas 80%"""


#def horaextra (horas):
#    if horas < 25:
#        return horas
#    if horas > 25.01 and horas < 40:
#        hora60 = horas - 25
#        return hora60
#    if horas > 40.01 and horas < 60:
#        hora80 = horas - 40
#        return hora80









#Programa principal

def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)

titulo('CÁLCULO DE HORAS EXTRAS')

horas = float(input('\033[1mDigite a quantidade de horas feitas: '))
if horas > 60:
    hora100 = horas - 60
    print(f'\033[1;36mTotal de horas à 50% 25.0 horas')
    print(f'Total de horas à 60% 15.0 horas')
    print(f'Total de horas à 80% 20.0 horas')
    print(f'Total de horas à 100% {hora100} horas')
if horas > 40 and horas <= 60:
    hora80 = horas - 40
    print(f'\033[1;36mTotal de horas à 50% 25.0 horas')
    print(f'Total de horas à 60% 15.0 horas')
    print(f'Total de horas à 80% {hora80} horas')
if horas > 25 and horas <= 40:
    hora60 = horas - 25
    print(f'\033[1;36mTotal de horas à 50% 25.0 horas')
    print(f'Total de horas à 60% {hora60} horas')
if horas > 0 and horas <= 25:
    print(f'Total de horas à 50% {horas} horas')
if horas ==0:
    print(f'Vamos parar de preguiça e vir fazer hora extra!')
if horas <0:
    print('Tá de brinqueixon whith me?')

print("MOSTRANDO PRO AMÓS O GIT")
