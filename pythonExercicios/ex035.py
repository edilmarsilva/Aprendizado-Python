"""Desenvolva um programa que leia o comprimento de três retas
e diga ao usuário se elas podem ou não formar um triângulo."""
print('\033[36m-=' * 20)
print('\033[31m         VERIFICADOR DE TRIÂNGULO')
print('\033[36m-=' * 20)
r1 = float(input('\033[1;34mPRIMEIRO SEGMENTO: '))
r2 = float(input('SEGUNDO SEGMENTO: '))
r3 = float(input('TERCEIRO SEGMENTO: '))
print('\033[36m=\033[m' * 50)
if r1 + r2 > r3 and r1 + r3 > r2 and r2 + r3 > r1:
    print('\033[1mOs segmentos digitados PODEM FORMAR um triângulo')
else:
    print('\033[1mOs segmentos digitados NÃO PODEM FORMAR um triângulo.')
print('\033[36m=\033[m' * 50)
