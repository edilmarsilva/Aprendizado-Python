"""Crie um programa que leia duas notas de um aluno e calcule a sua média,
mostrando uma mensagem no final, conforme a média atingida:
–Média abaixo de 5,0: REPROVADO
–Média entre 5,0 e 6,9: RECUPERAÇÃO
–Média 7.0 ou superior: APROVADO"""
print('\033[36m-=' * 20)
print('\033[31m         CLÁSSICO DA MÉDIA')
print('\033[36m-=' * 20)
nota1 = float(input('\033[1;34mPRIMEIRA NOTA: '))
nota2 = float(input('SEGUNDA NOTA: '))
media = (nota1 + nota2) / 2
print('\033[36m=\033[m' * 30)
print('\033[35mSUA MÉDIA É: {}'.format(media))
if media < 5:
    print('\033[31mREPROVADO!!! ESTUDE MAIS.')
elif 5 <= media < 7:
    print('\033[33mVOCÊ AINDA TEM CHANCE!!! VÁ PARA RECUPERAÇÃO.')
elif media >= 7:
    print('\033[32mPARABÉNS !!! VOCÊ FOI APROVADO.')
print('\033[36m=\033[m' * 30)
