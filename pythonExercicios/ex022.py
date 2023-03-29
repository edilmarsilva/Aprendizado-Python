"""Crie um programa que leia o nome completo de uma pessoa e mostre:
–O nome com todas as letras maiúsculas e minúsculas.
— Quantas letras tem sem considerar os espaços.
— Quantas letras tem o primeiro nome."""
from time import sleep
print('\033[33mINTRODUÇÃO DE ÁNALISE DE STRING')
print('\033[36m-=' * 20)
print('\033[31m           ANALISANDO UM NOME')
print('\033[36m-=' * 20)
nome = str(input('\033[1;34mDIGITE SEU NOME COMPLETO: ')).strip()
print('\033[35mAnalisando seu nome...')
sleep(4)
print('\033[36m=\033[m' * 60)
print('\033[1mSeu nome em maiúsculas é \033[4m{}\033[m'.format(nome.upper()))
print('\033[1mSeu nome em minúsculas é \033[4m{}\033[m'.format(nome.lower()))
print('\033[35mContando quantas letras tem seu nome...\033[m')
sleep(3)
print('\033[1mSeu nome tem ao todo \033[4m{}\033[m letras.'.format(len(nome) - nome.count(' ')))
pnome = nome.split()
print('\033[1mSeu primeiro nome é \033[4m{}\033[m e ele tem \033[4m{}\033[1m letras.'.format(pnome[0], len(pnome[0])))
print('\033[36m=\033[m' * 60)
