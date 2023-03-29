"""Faça um programa que tenha uma função chamada maior(), que receba vários
parâmetros com valores inteiros. Seu programa tem que analisar todos os valores
e dizer qual deles é o maior."""
from time import sleep
def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)


def maior(*num):
    cont = mais = 0
    print('\033[1;35m-=\033[m' * 25)
    print('\033[1;33mAnalisando os valores passados...\033[m')
    sleep(1)
    for n in num:
        print(f'{n} ', end='')
        sleep(0.4)
        if cont == 0:
            mais = n
        else:
            if n > mais:
                mais = n
        cont += 1
    print(f'\033[1mforam informados {cont} ao todo.')
    print(f'O maior valor informado foi {mais}')


#Programa Principal
titulo('Função que descobre o maior')
maior(2, 9, 4, 5, 7, 1)
maior(4, 7, 0)
maior(1, 2)
maior(6)
maior()
