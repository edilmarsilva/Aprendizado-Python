"""Faça um programa que jogue par ou ímpar com o computador.
O jogo só será interrompido quando o jogador perder,
mostrando o total de vitórias consecutivas que ele conquistou
no final do jogo."""
from random import randint
from time import sleep
print('\033[35m-*\033[m' * 15)
print('\033[1;33m   Jogo do Par ou Ímpar ')
print('\033[35m-*\033[m' * 15)
vitoria = 0
while True:
    jogador = int(input('\033[1;34mEscolha um número: '))
    computador = randint(0, 10)
    res = jogador + computador
    escolha = ' '
    while escolha not in 'PI':
        escolha = str(input('Par ou Ímpar? [P/I] ')).upper()[0].strip()
    print(f'Você escolheu {jogador} e COMPUTADOR {computador}. Total de \033[4m{res}\033[m.')
    if res % 2 == 0:
        print('\033[1mDEU PAR')
    else:
        print('\033[1mDEU ÍMPAR')
    if escolha == 'I':
        if res % 2 == 0:
            print('\033[31mVocê PERDEU !!!')
            print('\033[35mENCERRANDO. CALCULANDO PONTUAÇÃO...')
            sleep(3)
            break
        if res % 2 == 1:
            print('\033[32mVocê GANHOU !!!')
            print('\033[35mVamos jogar novamente...')
            vitoria += 1
            sleep(2)
    if escolha == 'P':
        if res % 2 == 0:
            print('\033[32mVocê GANHOU !!!')
            print('\033[35mVamos jogar novamente...')
            vitoria += 1
            sleep(2)
        if res % 2 == 1:
            print('\033[31mVocê PERDEU !!!')
            print('\033[35mENCERRANDO. CALCULANDO PONTUAÇÃO...')
            sleep(3)
            break
print('\033[35m#-\033[m' * 18)
print(f'\033[1mGAME OVER!!! Você venceu {vitoria} vezes.')
print('\033[35m#-\033[m' * 18)
