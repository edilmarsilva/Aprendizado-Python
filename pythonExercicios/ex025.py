"""Crie um programa que leia o nome de uma pessoa e diga se ela tem “SILVA” no nome."""
print('\033[36m-=' * 20)
print('\033[31mPROCURANDO UM SOBRENOME')
print('\033[36m-=' * 20)
nome = str(input('\033[1;34mDIGITE SEU NOME COMPLETO: ')).strip()
print('\033[36m=\033[m' * 60)
print('\033[1mSeu nome tem Silva? \033[4m{}\033[m'.format('SILVA' in nome.upper()))
print('\033[36m=\033[m' * 60)
