"""Escreva um programa que leia dois números inteiros e compare-os.
Mostrando uma mensagem na tela:
–O primeiro valor é maior
–O segundo valor é maior
–Não existe valor maior, os dois são iguais"""
print('\033[36m-=' * 20)
print('\033[31m         QUAL O MAIOR VALOR?')
print('\033[36m-=' * 20)
n1 = int(input('\033[1;34mPRIMEIRO NÚMERO: '))
n2 = int(input('SEGUNDO NÚMERO: '))
print('\033[36m=\033[m' * 40)
if n1 > n2:
    print('\033[1mO primeiro valor digitado é o maior')
elif n2 > n1:
    print('\033[1mO segundo valor digitado é o maior')
else:
    print('\033[1mOs números digitados são IGUAIS')
print('\033[36m=\033[m' * 40)
