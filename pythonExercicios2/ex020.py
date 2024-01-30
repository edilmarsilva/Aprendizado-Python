"""
Sorteando uma ordem na lista
O mesmo professor do desafio 19 quer sortear a ordem de apresentação de trabalhos dos alunos.
Faça um programa que leia o nome dos quatro alunos e mostre a ordem sorteada.
"""
import random
aluno1 = str(input('Primeiro aluno: '))
aluno2 = str(input('Segundo aluno: '))
aluno3 = str(input('Terceiro aluno: '))
aluno4 = str(input('Quarto aluno: '))
alunos = [aluno1, aluno2, aluno3, aluno4]
random.shuffle(alunos)
print(f'Os trabalhos serão apresentados na seguinte ordem: {alunos}')

