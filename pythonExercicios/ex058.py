"""Melhore o jogo do DESAFIO 28 onde o computador vai “pensar” num número entre 0 e 10.
Só que agora o jogador vai tentar adivinhar até acertar, mostrando no final
quantos palpites foram necessários para vencer."""
from random import randint
from time import sleep
print('\033[36m-=' * 20)
print('\033[31m        JOGO DE ADIVINHAÇÃO v2.0')
print('\033[36m-=' * 20)
palpite = 1
computador = randint(0, 10)
print('\033[35mBem vindo ao JOGO DE ADIVINHAÇÃO v2.0')
sleep(2)
print('\033[35mDessa vez pensarei em um número entre 0 e 10.')
sleep(2)
print('\033[35mSerá que você consegue adivinhar qual foi?')
sleep(2)
print('\033[1;32m=\033[m' * 50)
jogador = int(input('\033[1;34mQual seu palpite? '))
print('\033[1;32m=\033[m' * 50)
while computador != jogador:
    if jogador < computador:
        jogador = int(input('ERROU! O número que estou pensando é maior !!! Tente novamente: '))
        palpite += 1
    if jogador > computador:
        jogador = int(input('ERROU! O número que estou pensando é menor !!! Tente novamente: '))
        palpite += 1
print('\033[36m=\033[m' * 50)
if palpite == 1:
    print(''f'\033[1mVocê Conseguiu com apenas {palpite} tentativa. Troféu MÃE DINÁ !!!')
if 1 < palpite <= 4:
    print(''f'Conseguiu com {palpite} tentativas. Parabens !!! Nada mau')
if 4 < palpite <= 7:
    print(''f'Uffa, {palpite} tentativas, foi foi razoável.')
if palpite > 8:
    print(''f'Com {palpite} tentativas, até minha vó !!!')
if palpite == 10:
    print(''f'Usou todas as {palpite} tentativas, TROFÉU AZARADO !!!')
print('\033[36m=\033[m' * 50)
