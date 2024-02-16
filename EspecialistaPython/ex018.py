"""
Escreva um programa que leia dois números inteiros e compare-os. mostrando na tela uma mensagem:

O primeiro valor é maior
O segundo valor é maior
Não existe valor maior, os dois são iguais
"""

from time import sleep

n1 = int(input('Informe um número: '))
n2 = int(input('Informe outro número: '))

print('Analisando os números...')
sleep(2)
if n1 > n2:
    maior = n1
    print(f'Dos números digitados o {n1} é MAIOR.')
elif n2 > n1:
    maior = n2
    print(f'Dos números digitados o {n2} é MAIOR.')
else:
    print('Não existe número maior, porque eles são IGUAIS.')