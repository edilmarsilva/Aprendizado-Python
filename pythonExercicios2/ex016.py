"""
Quebrando um número
Crie um programa que leia um número Real qualquer pelo teclado e mostre na tela a sua porção Inteira.
"""
import math
from math import trunc

n = float(input('Digite um valor: '))
print(f'O valor digitado foi {n} e sua porção inteira é {math.trunc(n)}.')# com o modulo math
print(f'O valor digitado foi {n} e sua porção inteira é {trunc(n)}.')# com apenas o trunc
print(f'O valor digitado foi {n} e sua porção inteira é {int(n)}.')# sem modulos
