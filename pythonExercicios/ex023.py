"""Faça um programa que leia um número de 0 a 9999 e mostre na tela cada um dos dígitos separados."""
print('\033[36m-=' * 20)
print('\033[31m           ANALISANDO UM NÚMERO')
print('\033[36m-=' * 20)
print('\033[31mIMPORTANDO FUNÇÃO DO MÓDULO SLEEP')
from time import sleep
num = int(input('\033[1;34mDIGITE UM NUMERO DE 0 à 9999: '))
u = num // 1 % 10
d = num // 10 % 10
c = num // 100 % 10
m = num // 1000 % 10
print('\033[35mAnalisando o numero {}...'.format(num))
sleep(3)
print('\033[36m=\033[m' * 60)
print('\033[1mUnidade: {}'.format(u))
print('Dezena: {}'.format(d))
print('Centena: {}'.format(c))
print('Milhar: {}'.format(m))
print('\033[36m=\033[m' * 60)
