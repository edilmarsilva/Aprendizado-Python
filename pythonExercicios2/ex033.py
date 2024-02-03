"""
Maior e menor valores
Faça um programa que leia três números e mostre qual é o maior e qual é o menor.
"""
print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Maior e menor valores":^40}')
print('\033[1;33m-=\033[m' * 20)
n1 = int(input('\033[1mDigite o primeiro valor: '))
n2 = int(input('Digite o segundo valor: '))
n3 = int(input('Digite o terceiro valor: '))
if n1 > n2 and n1 > n3:
    maior = n1
if n2 > n1 and n2 > n3:
    maior = n2
if n3 > n1 and n3 > n2:
    maior = n3
if n1 < n2 and n1 < n3:
    menor = n1
if n2 < n1 and n2 < n3:
    menor = n2
if n3 < n1 and n3 < n2:
    menor = n3
print('\033[36m=\033[m' * 50)
print(f'\033[1mO maior valor digitado foi {maior}')
print(f'O menor valor digitado foi {menor}')
print('\033[36m=\033[m' * 50)

