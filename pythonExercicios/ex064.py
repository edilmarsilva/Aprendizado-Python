"""Crie um programa que leia vários números inteiros pelo teclado.
O programa só vai parar quando o usuário digitar o valor 999, que é a condição de parada.
No final, mostre quantos números foram digitados e
qual foi a soma entre eles (desconsiderando o flag)."""
print('\033[36m-=' * 20)
print('\033[31m      Tratando vários valores v1.0')
print('\033[36m-=' * 20)
num = 0
soma = 0
cont = 0
while num != 999:
    num = int(input('\033[1;34mDigite um número [Para sair 999] → '))
    if num != 999:
        soma += num
        cont += 1
print('\033[36m=\033[m' * 50)
print(''f'\033[1mVoce digitou {cont} números e a soma entre eles foi {soma}.')
print('\033[36m=\033[m' * 50)
