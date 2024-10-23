"""
Crie um programa que leia números inteiros pelo teclado.
O programa só vai parar quando o usuário digitar o valor 999,
que é a condição de parada. No final, mostre quantos números foram digitados
e qual foi a soma entre elas (desconsiderando o flag).
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Vários números com flag ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

cont = soma = 0
while True:
    num = int(input('Digite um número [999 para PARAR]: '))
    if num == 999:
        break
    else:
        soma += num
        cont += 1
print(f'Você digitou {cont} números e a soma é {soma}')
print('\033[36m=\033[m' * 42)
