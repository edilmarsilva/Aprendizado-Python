'''
Desenvolva um programa que leia o comprimento de três retas e diga ao usuário se elas
podem ou não formar um triângulo.
DICA: para que 3 segmentos possam formar um triângulo o maior segmento não pode ser maior
que a soma dos outros dois segmentos
'''

r1 = float(input('Digite o comprimento da primeira reta: '))
r2 = float(input('Digite o comprimento da segunda reta: '))
r3 = float(input('Digite o comprimento da terceira reta: '))

if r1 + r2 < r3 and r1 + r3 < r2 and r2 + r3 < r1:
    print('As retas podem formar um triângulo.')
else:
    print('As retas não podem formar um triângulo.')