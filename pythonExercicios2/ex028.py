"""
Jogo da Adivinhação v.1.0
Escreva um programa que faça o computador “pensar” em um número inteiro entre 0 e 5
e peça para o usuário tentar descobrir qual foi o número escolhido pelo computador.
O programa deverá escrever na tela se o usuário venceu ou perdeu.
"""
from random import randint
from time import sleep
print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Jogo da Adivinhação v.1.0":^40}')
print('\033[1;33m-=\033[m' * 20)
pc = randint(0, 5)
escolha = int(input('\033[1;34mPensei em um número, tente adivinhar qual foi: \033[m'))
print('\033[1;35mPROCESSANDO...\033[m')
sleep(2)
if escolha == pc:
    print(f'\033[1;32mParabéns, você acertou. Incrível, você é bruxo!')
else:
    print(f'\033[1;31;40mVocê errou!!!')
