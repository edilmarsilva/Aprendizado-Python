"""
Par ou Ímpar?
Crie um programa que leia um número inteiro e mostre na tela se ele é PAR ou ÍMPAR.
"""
print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Par ou Ímpar?":^40}')
print('\033[1;33m-=\033[m' * 20)
num = int(input('\033[1;35mDigite um número qualquer: '))
if num % 2 == 1:
    print(f'O número {num} é \033[1;34mÍMPAR\033[m!')
else:
    print(f'O número {num} é \033[1;34mPAR\033[m!')
