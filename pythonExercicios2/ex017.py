"""
Catetos e Hipotenusa
Faça um programa que leia o comprimento do cateto oposto e do cateto adjacente de um triângulo retângulo.
Calcule e mostre o comprimento da hipotenusa.
"""

from math import hypot
co = float(input('Digite o comprimento do cateto oposto: '))
ca = float(input('Digite o comprimento do cateto adjacente: '))
hip = hypot(co, ca)
hip2 = (co**2 + ca**2) ** 0.5
print(f'A hipotenusa vai medir {hip}')
print(f'A hipotenusa vai medir {hip2}')
