"""
Progressão Aritmética
Desenvolva um programa que leia o primeiro termo e a razão de uma PA. No final,
mostre os 10 primeiros termos dessa progressão.
"""

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{" Progressão Aritmética ":+^40}')
print('\033[1;33m-=\033[m' * 20)

termo = int(input('Quantos termos quer mostrar: '))
pt = int(input('Primeiro termo: '))
razao = int(input('Razão: '))

print('\033[36m=\033[m' * 40)
for c in range(pt, razao * termo + razao, razao):
    print(c, end=' -> ')
print('ACABOU')
print('\033[36m=\033[m' * 40)
