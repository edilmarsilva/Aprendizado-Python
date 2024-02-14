"""
Escreva um programa que leia a velocidade de um carro.
Se ele ultrapassar 80Km/h, mostre uma mensagem dizendo que ele foi multado.
A multa vai custar R$7,00 por cada Km acima do limite
e mais 10% caso a velocidade ultrapasse 120 km/h.
"""

velocidade = int(input('Informe a velocidade em km/h: '))
if 80 < velocidade <= 120:
    print(f'Você foi multado. Valor da multa R$ {(velocidade - 80) * 7:.2f}')
elif velocidade > 120:
    print(f'Você foi multado com agravante de 10%. Valor da multa R$ {((velocidade - 80) * 7) + 10/100:.2f}')
else:
    print('VELOCIDADE NORMAL!!!')
print('DIRIJA COM SEGURANÇA')
