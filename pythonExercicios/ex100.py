"""Faça um programa que tenha uma lista chamada números e duas funções chamadas
sorteia() e somaPar(). A primeira função vai sortear 5 números e vai colocá-los
dentro da lista e a segunda função vai mostrar a soma entre todos os valores
pares sorteados pela função anterior."""


def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)


from random import randint
from time import sleep


def sorteia(lista):
    print('\033[1;35m-=\033[m' * 25)
    print('\033[1mSorteando 5 valores da lista: ', end='')
    for c in range(0, 5):
        n = randint(1, 10)
        lista.append(n)
        print(f'{n} ', end='')
        sleep(0.5)
    print('PRONTO')
    print('\033[1;35m-=\033[m' * 25)

def somaPar(lista):
    print('\033[1;35m-=\033[m' * 25)
    totpar = 0
    for n in lista:
        if n % 2 == 0:
            totpar += n
    print(f'\033[1mA soma dos valores pares da lista {lista} é igual a {totpar}.')
    print('\033[1;35m-=\033[m' * 25)


numeros = list()
titulo('Funções para sortear e somar')
sorteia(numeros)
somaPar(numeros)
