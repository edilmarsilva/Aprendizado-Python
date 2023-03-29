"""Faça um programa que tenha uma função chamada contador(),
que receba três parâmetros: início, fim e passo.
Seu programa tem que realizar três contagens através da
função criada:
a) de 1 até 10, de 1 em 1
b) de 10 até 0, de 2 em 2
c) uma contagem personalizada"""
from time import sleep
def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)


def contador(i, f, p):
    if p < 0:
        p *= -1
    if p == 0:
        p= 1
    print('\033[1;35m-=\033[m' * 25)
    print(f'\033[1;34mContagem de {i} até {f} de {p} em {p}')
    sleep(2.5)
    if i < f:
        cont = i
        while cont <= f:
            print(f'\033[1;36m{cont} ', end='')
            sleep(1)
            cont += p
        print('FIM')
    else:
        cont = i
        while cont >= f:
            print(f'\033[1;36m{cont} ', end='')
            sleep(1)
            cont -= p
        print('FIM')


#Programa Principal
titulo('Função de Contador')
contador(1, 10, 1)
contador(10, 0, 2)
print('\033[1;35m-=\033[m' * 25)
print(f'\033[1;34m{"AGORA É SUA VEZ DE PERSONALIZAR A CONTAGEM":^50}')
inicio = int(input('\033[1;34mInício: '))
fim = int(input('Fim:       '))
passo = int(input('Passo:   '))
contador(inicio, fim, passo)
