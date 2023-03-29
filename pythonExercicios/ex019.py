"""Um professor quer sortear um dos seus quatro alunos para apagar o quadro. Faça um programa que ajude ele, lendo o
nome dos alunos e escrevendo na tela o nome do escolhido."""
print('\033[33mCONHECENDO O MÓDULO RANDOM')
print('\033[36m-=' * 20)
print('\033[31m           SORTEANDO UM ALUNO')
print('\033[36m-=' * 20)
import random
print('\033[31mIMPORTANDO O MÓDULO RANDOM')
a1 = str(input('\033[1;34mPrimeiro aluno: '))
a2 = str(input('Segundo aluno: '))
a3 = str(input('Terceiro aluno: '))
a4 = str(input('Quarto aluno: '))
lista = [a1, a2, a3, a4]
escolhido = random.choice(lista)
print('\033[36m=\033[m' * 60)
print('\033[1mO aluno sorteado foi : {}'.format(escolhido))
print('\033[36m=\033[m' * 60)
from random import choice
print('\033[31mIMPORTANDO A FUNÇÃO CHOICE DO MÓDULO RANDOM')
a1 = str(input('\033[1;34mPrimeiro aluno: '))
a2 = str(input('Segundo aluno: '))
a3 = str(input('Terceiro aluno: '))
a4 = str(input('Quarto aluno: '))
lista = [a1, a2, a3, a4]
escolhido = choice(lista)
print('\033[36m=\033[m' * 60)
print('\033[1mO aluno sorteado foi : {}'.format(escolhido))
print('\033[36m=\033[m' * 60)
