"""
Gerenciador de Pagamentos
Elabore um programa que calcule o valor a ser pago por um produto,
considerando o seu preço normal e condição de pagamento:

– à vista dinheiro/cheque: 10% de desconto

– à vista no cartão: 5% de desconto

– em até 2x no cartão: preço formal

– 3x ou mais no cartão: 20% de juros
"""

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{" Gerenciador de Pagamentos ":+^40}')
print('\033[1;33m-=\033[m' * 20)

valor = float(input('\033[1mQual o valor total das compras: R$ '))
print('''
FORMAS DE PAGAMENTO
[ 1 ] À VISTA DINHEIRO OU PIX
[ 2 ] À VISTA CARTÃO DE CRÉDITO
[ 3 ] 2x NO CARTÃO
[ 4 ] 3x OU MAIS NO CARTÃO
''')

opcao = int(input('\033[1mEscolha a forma de pagamento: '))

print('\033[36m=\033[m' * 50)
if opcao == 1:
    print(f'\033[1mVocê ganhou 10% de desconto, total à pagar R$ {valor - (valor * 10 / 100):.2f}')
elif opcao == 2:
    print(f'\033[1mVocê ganhou 5% de desconto, total à pagar R$ {valor - (valor * 5 / 100):.2f}')
elif opcao == 3:
    print(f'\033[1mParcelado em 2x SEM JUROS')
    print(f'PARCELA 1: R$ {valor / 2:.2f}')
    print(f'PARCELA 2: R$ {valor / 2:.2f}')
elif opcao == 4:
    print(f"""\033[1m
        3  x R$ {(valor + (valor * 20 / 100)) / 3:.2f}
        4  x R$ {(valor + (valor * 20 / 100)) / 4:.2f}
        5  x R$ {(valor + (valor * 20 / 100)) / 5:.2f}
        6  x R$ {(valor + (valor * 20 / 100)) / 6:.2f}
        7  x R$ {(valor + (valor * 20 / 100)) / 7:.2f}
        8  x R$ {(valor + (valor * 20 / 100)) / 8:.2f}
        9  x R$ {(valor + (valor * 20 / 100)) / 9:.2f}
        10 x R$ {(valor + (valor * 20 / 100)) / 10:.2f}
        """)
    parcelas = int(input('\033[1mEm quantas vezes deseja parcelar? '))
    print('\033[36m=\033[m' * 50)
    if parcelas == 3:
        print(f'\033[1mCompra parcelada em {parcelas}x de R$ {(valor + (valor * 20 / 100)) / 3:.2f}')
    elif parcelas == 4:
        print(f'\033[1mCompra parcelada em {parcelas}x de R$ {(valor + (valor * 20 / 100)) / 4:.2f}')
    elif parcelas == 5:
        print(f'\033[1mCompra parcelada em {parcelas}x de R$ {(valor + (valor * 20 / 100)) / 5:.2f}')
    elif parcelas == 6:
        print(f'\033[1mCompra parcelada em {parcelas}x de R$ {(valor + (valor * 20 / 100)) / 6:.2f}')
    elif parcelas == 7:
        print(f'\033[1mCompra parcelada em {parcelas}x de R$ {(valor + (valor * 20 / 100)) / 7:.2f}')
    elif parcelas == 8:
        print(f'\033[1mCompra parcelada em {parcelas}x de R$ {(valor + (valor * 20 / 100)) / 8:.2f}')
    elif parcelas == 9:
        print(f'\033[1mCompra parcelada em {parcelas}x de R$ {(valor + (valor * 20 / 100)) / 9:.2f}')
    elif parcelas == 10:
        print(f'\033[1mCompra parcelada em {parcelas}x de R$ {(valor + (valor * 20 / 100)) / 10:.2f}')
    else:
        print('\033[1;31mOPÇÃO INVÁLIDA. Fale com o vendedor.\033[m')
else:
    print('\033[1;31mOPÇÃO INVÁLIDA. Fale com o vendedor.\033[m')
print('\033[1mVOLTE SEMPRE !!!')
