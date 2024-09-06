"""
Melhore o DESAFIO 61, perguntando para o usuário se ele quer mostrar mais alguns termos.
O programa encerrará quando ele disser que quer mostrar 0 termos.
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Super Progressão Aritmética v3.0 ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)



pt = int(input('\033[1;32mDigite o primeiro termo: '))
razao = int(input('Razão: '))

termo = 0
tot_termo = 0
mais_termo = 10

while mais_termo != 0:
    tot_termo = tot_termo + mais_termo
    while termo < tot_termo:
        print(f'{pt} -> ', end=' ')
        pt = pt + razao
        termo += 1
    print('\033[1;36mPAUSA')
    mais_termo = int(input('Quantos termos quer mostrar a mais? '))
print(f'Progressão finalizada com sucesso e um total de {tot_termo} mostrados.')
print('\033[36m=\033[m' * 42)
