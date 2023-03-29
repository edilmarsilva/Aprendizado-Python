"""Desenvolva um programa que leia as duas notas de um aluno, calcule e mostre a sua média."""
print('\033[36m-=' * 20)
print('\033[31m         CALCULANDO SUA MÉDIA')
print('\033[36m-=' * 20)
n = str(input('\033[36mDIGITE SEU NOME: '))
n1 = float(input('\033[35mPRIMEIRA NOTA: '))
n2 = float(input('\033[35mSEGUNDA NOTA: '))
m = (n1+n2) / 2
print(f'\033[35m{n} sua média das notas {n1:.1f} e {n2:.1f} é {m:.1f}!\033[m')
print(f'\033[36m-=' * 20)
