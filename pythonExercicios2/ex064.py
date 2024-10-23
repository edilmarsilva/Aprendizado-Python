"""
Crie um programa que leia vários números inteiros pelo teclado.
O programa só vai parar quando o usuário digitar o valor 999,
que é a condição de parada. No final, mostre quantos números
foram digitados e qual foi a soma entre eles (desconsiderando o flag).
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Tratando vários valores v1.0 ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

num = 0
cont = 0
soma = 0
while num != 999:
    num = int(input('Digite um número [999 PARA PARAR]: '))
    if num == 999:
        break
    else:
        soma += num
        cont += 1
print(f'Foram digitados {cont} números e a soma é de {soma}')
print('\033[36m=\033[m' * 42)
