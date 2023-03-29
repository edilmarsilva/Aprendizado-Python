"""Crie um programa que faça o computador jogar Jokenpô com você."""
from random import randint
from time import sleep
print('\033[36m-=' * 20)
print('\033[31m         BRINCADEIRA DE CRIANÇA')
print('\033[36m-=' * 20)
itens = ('PEDRA', 'PAPEL', 'TESOURA')
computador = randint(0, 2)
print('''\033[35mEscolha uma das opções abaixo: 
[0] PEDRA
[1] PAPEL
[2] TESOURA''')
jogador = int(input('\033[1;34mQual é a sua jogada? '))
print('JO')
sleep(0.5)
print('KEN')
sleep(0.5)
print('PO...')
sleep(0.5)
print('\033[36m=\033[m' * 40)
print('Jogador jogou {}'.format(itens[jogador]))
sleep(2)
print('Computador jogou {}'.format(itens[computador]))
print('\033[36m=\033[m' * 40)
if computador == 0:
    if jogador == 0:
        sleep(2)
        print('\033[33mEMPATE\033[m')
    elif jogador == 1:
        sleep(2)
        print('\033[32mPARABÉNS !!! Você ganhou\033[m')
    elif jogador == 2:
        sleep(2)
        print('\033[31mDERROTA !!! O Computador venceu\033[m')
    else:
        sleep(2)
        print('OPÇÃO INVÁLIDA. FIM DE JOGO')
elif computador == 1:
    if jogador == 0:
        sleep(2)
        print('\033[31mDERROTA !!! O Computador venceu\033[m')
    elif jogador == 1:
        sleep(2)
        print('\033[33mEMPATE\033[m')
    elif jogador == 2:
        sleep(2)
        print('\033[32mPARABÉNS !!! Você ganhou\033[m')
    else:
        sleep(2)
        print('OPÇÃO INVÁLIDA. FIM DE JOGO')
elif computador == 2:
    if jogador == 0:
        sleep(2)
        print('\033[32mPARABÉNS !!! Você ganhou\033[m')
    elif jogador == 1:
        sleep(2)
        print('\033[31mDERROTA !!! O Computador venceu\033[m')
    elif jogador == 2:
        sleep(2)
        print('\033[33mEMPATE\033[m')
    else:
        sleep(2)
        print('OPÇÃO INVÁLIDA. FIM DE JOGO')
print('\033[36m=\033[m' * 40)
