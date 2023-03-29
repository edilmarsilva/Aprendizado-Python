"""Escreva um programa que leia a velocidade de um carro. Se ele ultrapassar 80Km/h, mostre uma mensagem dizendo que ele
foi multado. A multa vai custar R$ 7,00 por cada km acima do limite."""
print('\033[36m-=' * 20)
print('\033[31m     RADAR DE VELOCIDADE TABAJARA')
print('\033[36m-=' * 20)
velocidade = float(input('\033[1;34mQual é a velocidade atual do carro? '))
print('\033[36m=\033[m' * 50)
if velocidade <= 80:
    print('\033[1mTenha um bom dia! Dirija com segurança')
else:
    multa = float(velocidade - 80) * 7
    print('\033[1;41mMULTADO ! Você excedeu o limte de velocidade que é de 80 km/h\033[m')
    print('\033[1;41mO valor da sua multa é de R$ {:.2f}\033[m'.format(multa))
print('\033[32mRESPEITE O LIMITE DE VELOCIDADE')
print('\033[36m=\033[m' * 50)
