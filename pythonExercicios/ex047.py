"""Crie um programa que mostre na tela todos os números pares que estão no intervalo entre 1 e 50."""
print('\033[36m-=' * 20)
print('\033[31m         CONTAGEM DE PARES')
print('\033[36m-=' * 20)
print('\033[36m=\033[m' * 102)
for c in range(2, 51, +2):
    print('\033[1m', c, end=' ')
print('ACABOU')
print('\033[36m=\033[m' * 102)
