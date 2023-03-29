"""Exercício Python 006: Crie um algoritmo que leia um número e mostre o seu dobro, triplo e raiz quadrada."""
n = float(input('\033[1;32mDigite um número:\033[m '))
print(f'\033[35mO dobro de {n} vale {n * 2}\033[m')
print(f'\033[35mO triplo de {n} vale {n * 3}\033[m')
print(f'\033[35mA raiz quadrada de {n} é igual a {n ** (1/2):.2f}\033[m')
print(f'\033[35mA metade de {n} é igual a {n / 2}\033[m')
n = float(input('\033[1;30mDigite um número:\033[m '))
d = n*2
t = n*3
r = n**(1/2)
m = n/2
print(f'\033[43mO dobro de {n} é igual a {d}\033[m')
print(f'\033[43mO triplo de {n} é igual a {t}\033[m')
print(f'\033[43mA raiz quadrada de {n} é igual a {r:.2f}\033[m')
print(f'\033[43mA metade de {n} é igual a {m}\033[m')
print(f'\033[41m=' * 10, 'FIM', '\033[41m=\033[m' * 10)
