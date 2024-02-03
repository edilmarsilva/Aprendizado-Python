"""
Analisando Triângulos v2.0
Refaça o DESAFIO 35 dos triângulos, acrescentando o recurso de mostrar
que tipo de triângulo será formado:

Triângulo escaleno: triângulo que possui todos os lados com medidas diferentes.
Triângulos isósceles: triângulo que possui dois lados com medidas iguais.
Triângulo equilátero: triângulo que possui todos os lados com medidas iguais.
"""
from time import sleep

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Analisando Triângulos v2.0":^40}')
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
    if reta1 != reta2 and reta1 != reta3 and reta2 != reta3:
        print('\033[1mE o triangulo formado será o ESCALENO!')
    elif reta1 == reta2 and reta1 != reta3 or reta1 == reta3 and reta1 != reta2 or reta2 == reta3 and reta2 != reta1:
        print('\033[1mE o triangulo formado será o ISÓSCELES!')
    elif reta1 == reta2 and reta1 == reta3:
        print('\033[1mE o triangulo formado será o EQUILATERO!')
else:
    print('\033[1mAs medidas das retas \033[1;31mNÃO PODEM\033[m formar um triangulo.')
print('\033[36m=\033[m' * 50)
