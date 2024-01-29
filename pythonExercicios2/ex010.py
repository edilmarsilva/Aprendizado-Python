"""
Conversor de Moedas
Crie um programa que leia quanto dinheiro uma pessoa tem na carteira e mostre quantos dólares ela pode comprar.
"""
# Cotação do dólar em 26/01/2024
real = float(input('Quanto dinheiro você tem na carteira? R$ '))
dolar = real / 4.91
print(f'Com R$ {real:.2f} você pode comprar US$ {dolar:.2f}')
