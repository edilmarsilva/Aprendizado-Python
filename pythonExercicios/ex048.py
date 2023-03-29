"""Faça um programa que calcule a soma entre todos os números que são
múltiplos de três e que se encontram no intervalo de 1 até 500."""
c = 0
soma = 0
print('\033[36m-=' * 20)
print('\033[31m         SOMANDO OS MULTIPLOS DE 3')
print('\033[36m-=' * 20)
print('\033[36m=\033[m' * 50)
for cont in range(1, 501):
    if cont % 3 == 0:
        c = c + 1
        soma = soma + cont
print('\033[1mA soma de todos os {} valore solicitados é {}'.format(c, soma))
print('\033[36m=\033[m' * 50)
