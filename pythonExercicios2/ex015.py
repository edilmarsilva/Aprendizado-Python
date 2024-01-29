"""
Aluguel de Carros
Escreva um programa que pergunte a quantidade de Km percorridos por um carro alugado e a
quantidade de dias pelos quais ele foi alugado. Calcule o preço a pagar,
sabendo que o carro custa R$60 por dia e R$0,15 por Km rodado.
"""
dias = int(input('Quantos dias ficou com o carro: '))
km = float(input('Quantoas quilomentros foram percorridos: '))
aluguel = dias * 60
adicional = km * 0.15
print('================================')
print('         RESUMO DAS DESPESAS         ')
print(f'Total à pagar de aluguel é de R$ {aluguel:.2f}')
print(f'Adiconal referente aos {km}km percorridos é de R$ {adicional:.2f}')
print(f'Totalizando__________________R$ {aluguel + adicional:.2f}')
print(f'Para pagamento à vista com 10% de desconto o valor é R$ {(aluguel + adicional) - ((aluguel + adicional) * 10 / 100):.2f}')
print('================================')
