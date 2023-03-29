"""Exercício Python 17: Faça um programa que leia o comprimento do cateto oposto e do cateto adjacente de um triângulo
retângulo. Calcule e mostre o comprimento da hipotenusa.
Com método nativo do PYTHON"""


print('\033[31mCOM FUNÇÕES NATIVAS DO PYTHON')
print('\033[36m-=' * 20)
print('\033[31m CALCULANDO A HIPOTENUSA')
print('\033[36m-=' * 20)
co = float(input('\033[1;34mDigite o comprimento do CATETO OPOSTO: '))
ca = float(input('Digite o comprimento do CATETO ADJACENTE: '))
hi = (co ** 2 + ca ** 2) ** (1/2)


print('\033[36m=\033[m' * 60)
print('\033[1mA HIPOTENUSA vai medir {:.2f}'.format(hi))
print('\033[36m=\033[m' * 60)
print('\033[31mCom o modulo MATH')
import math
co = float(input('\033[1;34mDigite o comprimento do CATETO OPOSTO: '))
ca = float(input('Digite o comprimento do CATETO ADJACENTE: '))
hi = math.hypot(co, ca)


print('\033[36m=\033[m' * 60)
print('\033[1mA HIPOTENUSA vai medir {:.2f}'.format(hi))
print('\033[36m=\033[m' * 60)
print('\033[31mCom apenas uma função do módulo MATH')
from math import hypot
co = float(input('\033[1;34mDigite o comprimento do CATETO OPOSTO: '))
ca = float(input('Digite o comprimento do CATETO ADJACENTE: '))
hi = hypot(co, ca)
print('\033[36m=\033[m' * 60)
print('\033[1mA HIPOTENUSA vai medir {:.2f}'.format(hi))
print('\033[36m=\033[m' * 60)
