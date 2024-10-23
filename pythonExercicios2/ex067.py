"""
Faça um programa que mostre a tabuada de vários números, um de cada vez,
para cada valor digitado pelo usuário. O programa será interrompido quando o número solicitado
for negativo.
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Tabuada v3.0 ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

while True:
    num = int(input('Qual número deseja ver a tabuada? '))
    if num < 0:
        print('Programa de Tabuada Encerrado. Volte Sempre !!!')
        break
    limite = int(input('Até quantos quer ver a multiplicação: '))
    for cont in range(1, limite + 1):
        print(f'{num} x {cont} = {num * cont}')
print('\033[36m=\033[m' * 42)
