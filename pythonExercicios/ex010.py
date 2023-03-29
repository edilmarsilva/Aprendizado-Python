"""Crie um programa que leia quanto dinheiro uma pessoa tem na carteira e mostre quantos dólares ela pode comprar.
-Considere US$ 4,97
-Considere EUR 5,21"""
print('\033[36m-=' * 20)
print('\033[31m         CONVERTENDO MOEDAS')
print('\033[36m-=' * 20)
r = float(input('\033[1;34mQual o valor que você tem na carteira? R$ '))
d = r / 4.97
e = r / 5.21
print('\033[36m+' * 55)
print('Com R$ {:.2f} você pode comprar um total de US$ {:.2f} !!!'.format(r, d))
print('\033[36m+' * 55)
print('Com R$ {:.2f} você pode comprar um total de EUR$ {:.2f} !!!'.format(r, e))
print('\033[36m+' * 55)

