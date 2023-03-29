"""Faça um programa que leia três números e mostre qual é o maior e qual é o menor."""
print('\033[36m-=' * 20)
print('\033[31m        SOMENTE O MAIOR E MENOR')
print('\033[36m-=' * 20)
n1 = int(input('\033[1;34mPRIMEIRO VALOR: '))
n2 = int(input('SEGUNDO VALOR: '))
n3 = int(input('TERCEIRO VALOR: '))
if n1 < n2 and n1 < n3:
    menor = n1
if n2 < n1 and n2 < n3:
    menor = n2
if n3 < n1 and  n3 < n2:
    menor = n3
print('\033[36m=\033[m' * 50)
print('\033[1mO menor valor digitado foi {}'.format(menor))
if n1 > n2 and n1 > n3:
    maior = n1
if n2 > n1 and n2 > n3:
    maior = n2
if n3 > n1 and n3 > n2:
    maior = n3
print('\033[1mO maior valor digitado foi {}'.format(maior))
print('\033[36m=\033[m' * 50)
