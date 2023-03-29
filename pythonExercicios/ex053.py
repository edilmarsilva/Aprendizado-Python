"""Crie um programa que leia uma frase qualquer e diga se ela é um palíndromo, desconsiderando os espaços.
Exemplos de palíndromos:
APOS A SOPA, A SACADA DA CASA, A TORRE DA DERROTA, O LOBO AMA O BOLO, ANOTARAM A DATA DA MARATONA."""
print('\033[36m-=' * 20)
print('\033[31m           É UM PALÍNDROMO?')
print('\033[36m-=' * 20)
frase = str(input('\033[1;34mDigite uma frase: ')).strip().upper()
palavras = frase.split()
junto = ''.join(palavras)
inverso = ''
for letra in range(len(junto) - 1, -1, -1):
    inverso = inverso + junto[letra]
print('\033[35mO inverso de {} é {}'.format(junto, inverso))
print('\033[36m=\033[m' * 35)
if inverso == junto:
    print('\033[1mTemos um PALÍNDROMO')
else:
    print('\033[1mA frase não é um PALÍNDROMO')
print('\033[36m=\033[m' * 35)
