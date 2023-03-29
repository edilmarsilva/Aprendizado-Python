"""Faça um programa que leia uma frase pelo teclado e mostre quantas vezes aparece a letra “A”, em que posição ela
aparece a primeira vez e em que posição ela aparece a última vez."""
print('\033[36m-=' * 30)
print('\033[31mPROCURANDO UMA LETRA NA FRASE E MOSTRANDO A POSIÇÕES DELA')
print('\033[36m-=' * 30)
frase = str(input('\033[1;34mDigite uma frase: ')).upper().strip()
print('\033[36m=\033[m' * 50)
print('\033[1mA letra A aparece {} vezes na frase.'.format(frase.count('A')))
print('A primeira letra A apareceu na posição {}'.format(frase.find('A') + 1))
print('A última letra A apareceu na posição {}'.format(frase.rfind('A') + 1))
print('\033[36m=\033[m' * 50)
