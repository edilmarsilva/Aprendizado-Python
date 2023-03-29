"""Crie um programa que leia números inteiros pelo teclado.
O programa só vai parar quando o usuário digitar o valor 999, que é a condição de parada.
No final, mostre quantos números foram digitados e
qual foi a soma entre elas (desconsiderando o flag)."""
"""Crie um programa que leia números inteiros pelo teclado.
O programa só vai parar quando o usuário digitar o valor 999,
que é a condição de parada. No final, mostre quantos números
foram digitados e qual foi a soma
entre elas (desconsiderando o flag)."""
print('\033[35m-*\033[m' * 15)
print('\033[1;33m   Vários números com flag  ')
print('\033[35m-*\033[m' * 15)
cont = soma = 0
while True:
    num = int(input('\033[1;34mDigite um número [999 PARA SAIR]: '))
    if num == 999:
        break
    soma += num
    cont += 1
print('\033[36m=\033[m' * 60)
print(f'\033[1mForam digitados {cont} valores e a soma entre eles é igual a {soma}')
print('\033[36m=\033[m' * 60)
