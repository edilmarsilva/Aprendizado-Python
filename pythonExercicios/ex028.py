"""Escreva um programa que faça o computador “pensar” num número
inteiro entre 0 e 5 e peça para o usuário tentar descobrir qual foi o número
escolhido pelo computador. O programa deverá escrever na tela se o usuário venceu ou perdeu."""
from random import randint
from time import sleep
print('\033[36m-=' * 20)
print('\033[31m         JOGO DE ADIVINHAÇÃO')
print('\033[36m-=' * 20)
computador = randint(1, 5)
print('\033[35mLOADING...')
sleep(1.5)
print('\033[1;34mEstou pensando em um número entre 1 e 5. Tente adivinhar.')
print('\033[35mUM MOMENTO ESTOU PENSANDO...')
sleep(1.5)
print('\033[36m-=-\033[m' * 20)
print('\033[35mESTÁ PRONTO?')
sleep(1)
while True:
    jogador = int(input('\033[1;34mEm quem número pensei? '))
    if jogador < 0 or jogador > 5:
        print('\033[31mNÚMERO INVÁLIDO !!!')
    else:
        print('\033[32mVERIFICANDO...')
        sleep(3)
        print('\033[36m=\033[m' * 50)
        if jogador == computador:
            print('\033[42mPARABÉNS! Você conseguiu adivinhar que eu pensei no Nº {}\033[m'.format(computador))
        else:
            print('\033[41mERROU !!! Na verdade eu pensei no Nº {}\033[m'.format(computador))
        print('\033[36m=\033[m' * 50)
        break

