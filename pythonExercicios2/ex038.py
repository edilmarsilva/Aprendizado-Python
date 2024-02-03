"""
Comparando números
Escreva um programa que leia dois números inteiros e compare-os. Mostrando uma mensagem na tela:

– O primeiro valor é maior

– O segundo valor é maior

– Não existe valor maior, os dois são iguais
"""

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Comparando números":^40}')
print('\033[1;33m-=\033[m' * 20)

n1 = int(input('Primeiro número: '))
n2 = int(input('Segundo número:'))
print('\033[36m=\033[m' * 50)
if n1 > n2:
    print('O primeiro valor digitado é maior')
elif n2 > n1:
    print('O segundo valor digitado é maior')
elif n1 == n2:
    print('Não existe número maior, os dois são iguais')
print('\033[36m=\033[m' * 50)
