"""
Detector de Palíndromo
Crie um programa que leia uma frase qualquer e diga se ela é um palíndromo,
desconsiderando os espaços. Exemplos de palíndromos:

APOS A SOPA, A SACADA DA CASA, A TORRE DA DERROTA, O LOBO AMA O BOLO, ANOTARAM A DATA DA MARATONA.
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Detector de Palíndromo ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

frase = str(input('Digite algo: ')).strip().upper()
normal = frase.split()
junto = ''.join(normal)
inverso = ''

print('\033[36m=\033[m' * 42)
for letra in range(len(junto) - 1, -1, -1):
    inverso += junto[letra]
print(f'O inverso de {junto} é {inverso}.')
if inverso == junto:
    print('Temos um palíndromo')
else:
    print('Não temos um palíndromo')
print('\033[36m=\033[m' * 42)
