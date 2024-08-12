"""
Refaça o DESAFIO 51, lendo o primeiro termo e a razão de uma PA, mostrando
os 10 primeiros termos da progressão usando a estrutura while.
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Progressão Aritmética v2.0 ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

termo = 0

pt = int(input('Digite o primeiro termo: '))
razao = int(input('Razão: '))

while termo < 10:
    print(f'{pt} -> ', end=' ')
    pt = pt + razao
    termo += 1
print('FIM')




print('\033[36m=\033[m' * 42)