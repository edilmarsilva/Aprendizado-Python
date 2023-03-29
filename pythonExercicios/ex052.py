"""Faça um programa que leia um número inteiro e diga se ele é ou não um número primo"""
print('\033[36m-=' * 20)
print('\033[31m      VERIFICADOR DE NÚMERO PRIMO')
print('\033[36m-=' * 20)
num = int(input('\033[1;34mDigite um número: '))
cd = 0
print('\033[36m=\033[m' * 55)
for c in range(1, num + 1):
    if num % c == 0:
        print('\033[4;33m', c, end=' \033[m')
        cd = cd + 1
    else:
        print('\033[31m', c, end=' ')
print('')
print('\033[36m=\033[m' * 55)
print('\033[1mO número {} foi divisível {} vezes'.format(num, cd))
if cd == 2:
    print('E por isso ele é PRIMO')
else:
    print('E por isso ele NÃO É PRIMO')
print('\033[36m=\033[m' * 55)
