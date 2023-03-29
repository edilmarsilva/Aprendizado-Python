"""Refaça o DESAFIO 35 dos triângulos, acrescentando o recurso de mostrar
que tipo de triângulo será formado:
–EQUILÁTERO: todos os lados iguais
–ISÓSCELES: dois lados iguais, um diferente
–ESCALENO: todos os lados diferentes"""
print('\033[36m-=' * 20)
print('\033[31m       VERIFICADOR DE TRIÂNGULO 2.0')
print('\033[36m-=' * 20)
r1 = float(input('Primeiro segmento: '))
r2 = float(input('Segundo segmento: '))
r3 = float(input('Terceiro segmento: '))
print('\033[36m=\033[m' * 70)
if r1 + r2 > r3 and r1 + r3 > r2 and r2 + r3 > r1:
    print('\033[1mOs segmentos digitados PODEM FORMAR um triângulo', end='')
    if r1 == r2 and r1 == r3 and r2 == r3:
        print('do TIPO EQUILÁTERO !!!')
    elif r1 == r2 or r1 == r3 or r2 == r3:
        print('do TIPO ISÓSCELES !!!')
    elif r1 != r2 and r1 != r3 and r2 != r3:
        print('do TIPO ESCALENO !!!')
else:
    print('\033[1mOs segmentos digitados NÃO PODEM FORMAR um triângulo.')
print('\033[36m=\033[m' * 70)
