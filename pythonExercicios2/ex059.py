"""
Criando um Menu de Opções
Crie um programa que leia dois valores e mostre um menu na tela:
[ 1 ] somar
[ 2 ] multiplicar
[ 3 ] maior
[ 4 ] novos números
[ 5 ] sair do programa
Seu programa deverá realizar a operação solicitada em cada caso.
"""

from time import sleep

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Criando um Menu de Opções ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

resp = 0

n1 = int(input('Digite o primeiro número: '))
n2 = int(input('Digite o segundo número: '))
print('\033[36m=\033[m' * 42)

while resp != 5:
    print('''[ 1 ] Somar
[ 2 ] Multiplicar
[ 3 ] Maior
[ 4 ] Novos Números
[ 5 ] Sair do Programa
    ''')
    resp = int(input('Escolha uma opção: '))
    print('\033[36m=\033[m' * 42)
    if resp == 1:
        print(f'A soma de {n1} + {n2} = {n1 + n2}')
        print('\033[36m=\033[m' * 42)
    elif resp == 2:
        print(f'A multiplicação de {n1} x {n2} = {n1 * n2}')
        print('\033[36m=\033[m' * 42)
    elif resp == 3:
        if n1 > n2:
            maior = n1
        else:
            maior = n2
        print(f'Entre {n1} e {n2} o maior número é {maior}')
        print('\033[36m=\033[m' * 42)
    elif resp == 4:
        n1 = int(input('Digite o primeiro número: '))
        n2 = int(input('Digite o segundo número: '))
        print('\033[36m=\033[m' * 42)
    elif resp == 5:
        print('FINALIZANDO...')
        sleep(2)
    else:
        print('\033[31mOPÇÃO INVÁLIDA. TENTE NOVAMENTE!\033[3m')
        print('\033[36m=\033[m' * 42)
    sleep(3)
print('\033[36m=\033[m' * 42)
print('VOLTE SEMPRE')
print('\033[36m=\033[m' * 42)
