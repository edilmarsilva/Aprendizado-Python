"""
Radar eletrônico
Escreva um programa que leia a velocidade de um carro. Se ele ultrapassar 80Km/h,
mostre uma mensagem dizendo que ele foi multado.
A multa vai custar R$7,00 por cada Km acima do limite.
"""
print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Radar eletrônico":^40}')
print('\033[1;33m-=\033[m' * 20)
km = int(input('\033[1;35mInforme a velocidade atual do carro: '))
if km <= 80:
    print('\033[1;32mTenha um bom dia! Dirija com segurança!')
elif km > 80:
    print('\033[1;31;40mVocê foi multado! Velocidade máxima é de 80km/h')
    multa = (km - 80) * 7
    print(f'\033[1;31;40mValor da multa: R$ {multa:.2f}')
