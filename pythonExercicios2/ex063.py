"""
Escreva um programa que leia um número N inteiro qualquer
e mostre na tela os N primeiros elementos de uma Sequência de Fibonacci. Exemplo:

0 – 1 – 1 – 2 – 3 – 5 – 8
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Sequência de Fibonacci v1.0 ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

num = int(input('Quantos termos você quer mostrar? '))

cont = 1
pt = 0
st = 1

while cont <= num - 2:
    if cont == 1:
        print(f'{pt} - {st}', end='')
        cont += 1
        tt = pt + st
        print(f' - {tt}', end='')
        pt = st
        st = tt
    else:
        cont += 1
        tt = pt + st
        print(f' - {tt}', end='')
        pt = st
        st = tt
print(' - FIM')
print('\033[36m=\033[m' * 42)
