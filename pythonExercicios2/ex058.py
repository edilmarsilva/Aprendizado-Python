"""
Jogo da Adivinhação v2.0
Melhore o jogo do DESAFIO 28 onde o computador vai “pensar” em um número entre 0 e 10.
Só que agora o jogador vai tentar adivinhar até acertar,
mostrando no final quantos palpites foram necessários para vencer.
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Jogo da Adivinhação v2.0 ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

from random import randint
from time import sleep

computador = randint(0, 10)
cont = 1

print('Sou seu computador...')
sleep(2)
print('Acabei de pensar em um número entre 0 e 10.')
sleep(2)
print('Será que consegue adivinhar qual foi?')
sleep(2)

resposta = int(input('Qual é o seu palpite? '))
while resposta != computador:
    if resposta > computador:
        resposta = int(input('Menos...Tente mais uma vez '))
        cont += 1
    elif resposta < computador:
        resposta = int(input('Mais...Tente mais uma vez '))
        cont += 1
print(f'PARABÉNS!!! ACERTOU NA {cont}ª TENTATIVA.')
print('GAME OVER')
print('\033[36m=\033[m' * 42)
