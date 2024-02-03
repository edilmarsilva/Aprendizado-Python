"""
Analisando Triângulo v1.0
Desenvolva um programa que leia o comprimento de três retas e diga ao usuário
se elas podem ou não formar um triângulo.
"""

from time import sleep

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Analisando Triângulo v1.0":^40}')
print('\033[1;33m-=\033[m' * 20)

reta1 = float(input('\033[1mDigite o comprimento da primeira reta: '))
reta2 = float(input('Digite o comprimento da segunda reta: '))
reta3 = float(input('Digite o comprimento da terceira reta: '))
print('\033[36m=\033[m' * 50)
print('\033[1mEstou analisando se as retas podem formar um triângulo...')
sleep(3)
print('Estou finalizando...')
sleep(2)
print('\033[36m=\033[m' * 50)
if reta1 < reta2 + reta3 and reta2 < reta1 + reta3 and reta3 < reta1 + reta2:
    print('\033[1mAs medidas das retas \033[1;32mPODEM\033[m formar um triângulo.')
else:
    print('\033[1mAs medidas das retas \033[1;31mNÃO PODEM\033[m formar um triangulo.')
print('\033[36m=\033[m' * 50)
