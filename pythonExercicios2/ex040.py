"""
Aquele clássico da Média
 Crie um programa que leia duas notas de um aluno e calcule a sua média,
 mostrando uma mensagem no final, conforme a média atingida:

– Média abaixo de 5,0: REPROVADO

– Média entre 5,0 e 6,9: RECUPERAÇÃO

– Média 7.0 ou superior: APROVADO
"""

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Aquele clássico da Média":^40}')
print('\033[1;33m-=\033[m' * 20)

n1 = float(input('\033[1mDigite a primeira nota: '))
n2 = float(input('Digite a segunda nota: '))
media = (n1 + n2) / 2

print('\033[36m=\033[m' * 50)
if 0 < media < 5:
    print(f'\033[1;31mALUNO REPROVADO!\033[m Média {media:.1f}, estude mais!!! ')
elif 5 <= media < 7:
    print(f'\033[1;33mALUNO EM RECUPERAÇÃO!\033[m Média {media:.1f}, você ainda pode passar.')
elif media >= 7:
    print(f'\033[1;32mPARABÉNS, ALUNO APROVADO!!!\033[m Média {media:.1f}, precisamos de mais alunos como você')
elif media == 0:
    print(f'\033[1;30;41mMedia {media:.1f}\033[m, você sequer tentou?')
else:
    print('\033[1mNão sei como, mas você conseguiu ficar mais burro!!!')
print('\033[36m=\033[m' * 50)
