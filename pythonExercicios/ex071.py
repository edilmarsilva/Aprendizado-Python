"""Crie um programa que simule o funcionamento de um caixa eletrônico.
No início, pergunte ao usuário qual será o valor a ser sacado (número inteiro)
e o programa vai informar quantas cédulas de cada valor serão entregues.
OBS: considere que o caixa possui cédulas de R$50, R$20, R$10 e R$1."""
print('\033[35m-*\033[m' * 25)
print('\033[1;33m{:-^50}'.format('Simulador de Caixa Eletrônico'))
print('\033[35m-*\033[m' * 25)
print('\033[36m=\033[m' * 50)
print('\033[1;33m{:-^50}'.format('BANCO SEU DINHEIRO É MEU'))
print('\033[36m=\033[m' * 50)
nota50 = nota20 = nota10 = nota1 = resto = 0
while True:
    dinheiro = float(input('\033[1;34mQue valor quer sacar? R$ '))
    print(f'\033[1;32mO valor solicitado foi R$ {dinheiro:.2f}')
    resp = ' '
    while resp not in 'SN':
        resp = str(input('\033[1;33mCONFIRMA O VALOR SOLICITADO? [S/N] ')).strip().upper()[0]
    if resp == 'S':
        nota50 = dinheiro // 50
        resto = dinheiro % 50
        nota20 = resto // 20
        resto = resto % 20
        nota10 = resto // 10
        resto = resto % 10
        nota1 = resto
        break
    if resp == 'N':
        print('\033[1;35m-=\033[m' * 20)
        print('\033[1;31m       RETIRE CARTÃO. VOLTE SEMPRE')
        print('\033[1;35m-=\033[m' * 20)
        break
if resp == 'S':
    print('\033[1;35m-=\033[m' * 20)
    if nota50 != 0:
        print(f'\033[1mTotal de {nota50:.0f} cédulas de R$ 50,00')
    if nota20 != 0:
        print(f'\033[1mTotal de {nota20:.0f} cédulas de R$ 20,00')
    if nota10 != 0:
        print(f'\033[1mTotal de {nota10:.0f} cédulas de R$ 10,00')
    if nota1 != 0:
        print(f'\033[1mTotal de {nota1:.0f} cédulas de R$ 1,00')
    print('\033[1;35m-=\033[m' * 20)
    print('\033[1;31mRETIRE AS CÉDULAS. VOLTE SEMPRE')
    print('\033[1;35m-=\033[m' * 20)
