"""Crie um programa que tenha uma Tupla totalmente preenchida
com uma contagem por extenso, de zero até vinte.
Seu programa deverá ler um número pelo teclado (entre 0 e 20)
e mostrá-lo por extenso."""
print('\033[35m-*\033[m' * 25)
print('\033[1;33m{:-^50}'.format('Número por Extenso'))
print('\033[35m-*\033[m' * 25)
extenso = 'Zero', 'Um', 'Dois', 'Trez', 'Quatro', 'Cinco', 'Seis', \
          'Sete', 'Oito', 'Nove', 'Dez', 'Onze', 'Doze', 'Treze', \
          'Quatorze', 'Quinze', 'Dezesseis', 'Dezessete', \
          'Dezoito', 'Dezenove', 'Vinte'
while True:
    while True:
        num = int(input('\033[1;34mDigite um número entre 0 e 20: '))
        if 0 < num <= 20:
            break
        else:
            print('\033[1;34mTente Novamente. ', end='')
    print('\033[35m-=\033[m' * 25)
    for c in range(0, len(extenso)):
        if c == num:
            print(f'\033[1mO número {num} por extenso é \033[4m{extenso[c]}\033[m')
    print('\033[35m-=\033[m' * 25)
    print('\033[1;33m{:-^50}'.format('RESPOSTA DO PROFESSOR'))
    print('\033[35m-=\033[m' * 25)
    print(f'\033[1mO número {num} por extenso é \033[4m{extenso[num]}\033[m')
    print('\033[35m-=\033[m' * 25)
    resp = ' '
    while resp not in 'SN':
        resp = str(input('\033[1;36mQuer continuar? [S/N] ')).strip().upper()[0]
    if resp == 'N':
        break
print('\033[1;33m{:-^50}'.format('FIM DO PROGRAMA. VOLTE SEMPRE'))