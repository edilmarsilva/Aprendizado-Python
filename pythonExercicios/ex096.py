"""Faça um programa que tenha uma função chamada área(), que receba as dimensões
de um terreno retangular (largura e comprimento) e mostre a área do terreno."""

def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)


def area(l, c):
    areat = l * c
    print('\033[1;35m-=\033[m' * 25)
    print(f'\033[1mA área de um terreno {l:.1f} x {c:.1f} é de {areat:.1f}m².')
    print('\033[1;35m-=\033[m' * 25)


#Programa Principal
titulo('Função que calcula área')
largura = float(input('\033[1;36mLARGURA (m): '))
comprimento = float(input('\033[1;36mCOMPRIMENTO (m): '))
area(largura, comprimento)
