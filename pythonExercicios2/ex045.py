"""
GAME: Pedra Papel e Tesoura
Crie um programa que faça o computador jogar Jokenpô com você.
"""
from time import sleep
from random import randint

print('\033[1;33m-=' * 25)
print(f'\033[1;34m{" GAME: Pedra Papel e Tesoura ":+^50}')
print('\033[1;33m-=\033[m' * 25)

print('''Suas opções:
[ 1 ] PEDRA
[ 2 ] PAPEL
[ 3 ] TESOURA''')
print('\033[36m=\033[m' * 50)
computador = randint(1, 3)

escolha = int(input('Qual é a sua jogada: '))
print('\033[36m=\033[m' * 50)
print('JO')
sleep(0.8)
print('KEN')
sleep(0.8)
print('PO !!!')
sleep(0.8)
print('\033[36m=\033[m' * 50)

if computador == 1:
    print('Computador jogou PEDRA')
elif computador == 2:
    print('Computador jogou PAPEL')
elif computador == 3:
    print('Computador jogou TESOURA')
if escolha == 1:
    print('Jogador jogou PEDRA')
elif escolha == 2:
    print('Jogador jogou PAPEL')
elif escolha == 3:
    print('Jogador jogou TESOURA')
else:
    print('OPÇÃO INVÁLIDA !!!')

print('\033[36m=\033[m' * 50)

# Jogador PEDRA
if escolha == 1 and computador == 1:
    print('EMPATOU')
elif escolha == 1 and computador == 2:
    print('JOGADOR PERDEU !!!')
elif escolha == 1 and computador == 3:
    print('JOGADOR VENCEU!!!')
# Jogador PAPEL
elif escolha == 2 and computador == 1:
    print('JOGADOR VENCEU')
elif escolha == 2 and computador == 2:
    print('EMPATOU')
elif escolha == 2 and computador == 3:
    print('JOGADOR PERDEU!!!')
# Jogador TESOURA
elif escolha == 3 and computador == 1:
    print('JOGADOR PERDEU')
elif escolha == 3 and computador == 2:
    print('JOGADOR VENCEU !!!')
elif escolha == 3 and computador == 3:
    print('EMPATOU')

