"""
Refaça o exercício 6 dos triângulos, acrescentando o recurso de mostrar que tipo de
triângulo que será formado a partir dos segmentos informados pelo usuário:

EQUILÁTERO: todos os lados iguais
ISÓSCELES: dois lados iguais, um diferente
ESCALENO: todos os lados diferentes
"""

r1 = float(input('Digite o comprimento da primeira reta: '))
r2 = float(input('Digite o comprimento da segunda reta: '))
r3 = float(input('Digite o comprimento da terceira reta: '))

if r1 + r2 > r3 and r1 + r3 > r2 and r2 + r3 > r1:
    print('As retas podem formar um triângulo.')
    if r1 == r2 and r2 == r3:
        print('E FORMAM UM TRIÂNGULO EQUILÁTERO.')
    elif r1 == r2 or r1 == r3 or r3 == r2:
        print('E FORMAM UM TRIÂNGULO ISÓSCELES.')
    elif r1 != r2 and r1 != r3 and r2 != r3:
        print('E FORMAM UM TRIÂNGULO ESCALENO.')
else:
    print('As retas não podem formar um triângulo.')
