"""Crie um programa que leia dois valores e mostre um menu na tela:
[1] somar
[2] multiplicar
[3] maior
[4] novos números
[5] sair do programa
O seu programa deverá realizar a operação solicitada em cada caso."""
from time import sleep
print('\033[36m-=' * 20)
print('\033[31m      Criando um Menu de Opções')
print('\033[36m-=' * 20)

n1 = int(input('\033[1;34mDigite um valor: '))
n2 = int(input('Digite outro valor: '))
opcao = 0
while opcao != 5:
    print('\033[36m-*\033[m' * 15)
    print('''\033[35m[1] SOMAR
[2] MULTIPLICAR
[3] MAIOR
[4] NOVOS VALORES
[5] SAIR DO PROGRAMA''')
    print('\033[36m-*\033[m' * 15)
    opcao = int(input('Qual é a sua opção? '))
    if opcao == 1:
        soma = n1 + n2
        print('\033[36m=\033[m' * 30)
        print(''f'A SOMA entre {n1} + {n2} é igual {soma}.')
        print('\033[36m=\033[m' * 30)
    elif opcao == 2:
        mult = n1 * n2
        print('\033[36m=\033[m' * 30)
        print(''f'O produto entre {n1} x {n2} é igual {mult}.')
        print('\033[36m=\033[m' * 30)
    elif opcao == 3:
        if n1 > n2:
            maior = n1
            print('\033[36m=\033[m' * 30)
            print(''f'Entre {n1} e {n2} o {maior} foi o MAIOR número digitado.')
            print('\033[36m=\033[m' * 30)
        else:
            maior = n2
            print('\033[36m=\033[m' * 30)
            print(''f'Entre {n1} e {n2} o {maior} foi o MAIOR número digitado.')
            print('\033[36m=\033[m' * 30)
    elif opcao == 4:
        print('Informe os números novamente: ')
        n1 = int(input('\033[1;34mDigite um valor: '))
        n2 = int(input('Digite outro valor: '))
        print('\033[36m-*\033[m' * 15)
    elif opcao == 5:
        print('Obrigago. Volte Sempre !!!')
    else:
        print('Opção inválida. Tente novamente.')
    sleep(3)
print('FINALIZANDO...')
sleep(2)
print('\033[36m=\033[m' * 30)
print(' FIM DO PROGRAMA ')
print('\033[36m=\033[m' * 30)
