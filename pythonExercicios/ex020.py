"""O mesmo professor do desafio 19 quer sortear a ordem de apresentação de trabalhos dos alunos.
Faça um programa que leia o nome dos quatro alunos e mostre a ordem sorteada."""
print('\033[36m-=' * 20)
print('\033[31m           ORDEM DE APRESENTAÇÃO')
print('\033[36m-=' * 20)
print('\033[31mIMPORTANDO O MÓDULO RANDOM')
import random
a1 = str(input('\033[1;34mPrimeiro aluno: '))
a2 = str(input('Segundo aluno: '))
a3 = str(input('Teceiro aluno: '))
a4 = str(input('Quarto aluno: '))
lista = [a1, a2, a3, a4]
random.shuffle(lista)
print('\033[36m=\033[m' * 60)
print('\033[1mA ordem de apresentação será: {}'.format(lista))
print('\033[36m=\033[m' * 60)
print('\033[31mIMPORTANDO A FUNÇÃO SHUFFLE DO MÓULO RANDOM')
from random import shuffle
a1 = str(input('\033[1;34mPrimeiro aluno: '))
a2 = str(input('Segundo aluno: '))
a3 = str(input('Teceiro aluno: '))
a4 = str(input('Quarto aluno: '))
lista = [a1, a2, a3, a4]
shuffle(lista)
print('\033[36m=\033[m' * 60)
print('\033[1mA ordem de apresentação será: {}'.format(lista))
print('\033[36m=\033[m' * 60)
