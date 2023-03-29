"""Faça um programa que leia o nome completo de uma pessoa, mostrando em seguida o primeiro
e o último nome separadamente."""
print('\033[36m-=' * 30)
print('\033[31m   MOSTRANDO PRIMEIRO E ÚLTIMO NOME DE UMA PESSOA')
print('\033[36m-=' * 30)
nome = str(input('\033[1;34mDIGITE SEU NOME COMPLETO: ')).strip()
pnome = nome.split()
print('\033[36m=\033[m' * 60)
print('\033[1mMuito prazer em te conhecer !!!')
print('Seu primeiro nome é {}'.format(pnome[0]))
print('Seu último nome é {}'.format(pnome[len(pnome)-1]))
print('\033[36m=\033[m' * 60)
