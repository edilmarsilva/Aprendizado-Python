"""Crie um programa que leia um número inteiro e mostre na tela se ele é PAR ou ÍMPAR."""
print('\033[36m-=' * 20)
print('\033[31m    CLÁSSICO !!! É PAR OU IMPAR?')
print('\033[36m-=' * 20)
numero = int(input('\033[1;34mDIGITE UM NÚMERO: '))
print('\033[36m=\033[m' * 40)
if numero % 2 == 0:
    print('\033[1mO número que você digitou é PAR')
else:
    print('\033[1mO número que você digitou é IMPAR')
print('\033[36m=\033[m' * 40)
