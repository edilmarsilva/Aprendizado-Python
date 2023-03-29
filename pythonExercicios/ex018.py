"""Faça um programa que leia um ângulo qualquer e mostre na tela o valor do seno, cosseno e tangente desse ângulo."""
print('\033[31mIMPORTANDO O MÓDULO MATH')
print('\033[36m-=' * 20)
print('\033[31m CALCULANDO O SENO, COSSENO E TANGENTE')
print('\033[36m-=' * 20)
import math
an = float(input('\033[1;34mDigite o ângulo que você deseja: '))
"""A medida passada está em graus, e o módulo passa como referência em radiano, portanto temos que converter em radiano
 a medida passada."""
se = math.sin(math.radians(an))
co = math.cos(math.radians(an))
ta = math.tan(math.radians(an))
print('\033[36m=\033[m' * 60)
print('\033[1mO ângulo de {:.1f}° tem o SENO de : {:.2f}'.format(an, se))
print('O ângulo de {:.1f}° tem o COSSENO de : {:.2f}'.format(an, co))
print('O ângulo de {:.1f}° tem a TANGENTE de : {:.2f}'.format(an, ta))
print('\033[36m=\033[m' * 60)
print('\033[31mIMPORTANDO APENAS AS FUNÇÕES DE SENO, COSSENO, TANGENTE E RADIANO')
from math import sin, cos, tan, radians
an = float(input('\033[1;34mDigite o ângulo que você deseja: '))
se = sin(radians(an))
co = cos(radians(an))
ta = tan(radians(an))
print('\033[36m=\033[m' * 60)
print('\033[1mO ângulo de {:.1f}° tem o SENO de : {:.2f}'.format(an, se))
print('O ângulo de {:.1f}° tem o COSSENO de : {:.2f}'.format(an, co))
print('O ângulo de {:.1f}° tem a TANGENTE de : {:.2f}'.format(an, ta))
print('\033[36m=\033[m' * 60)
