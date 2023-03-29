"""Elabore um programa que calcule o valor a ser pago por um produto,
considerando o seu preço normal e condição de pagamento:
–à vista dinheiro/cheque: 10% de desconto
–à vista no cartão: 5% de desconto
–em até 2x no cartão: preço formal
–3x ou mais no cartão: 20% de juros"""
print('\033[36m-=' * 20)
print('\033[31m *********LOJA ARTES EM PANOS*********')
print('\033[36m-=' * 20)
total = float(input('\033[1;34mValor total das compras: R$ '))
print('''\033[35mESCOLHA A FORMA DE PAGAMENTO
\033[1;34m[1] À VISTA DINHEIRO OU PIX
[2] À VISTA NO CARTÃO
[3] Em 2x NO CARTÃO
[4] Em 3x ou MAIS NO CARTÃO
[5] CANCELAR A COMPRA !!!''')
escolha = int(input('\033[35mQual a forma de pagamento? '))
print('\033[36m=\033[m' * 70)
if escolha == 1:
    print('\033[1mVocê recebeu 10% de desconto.')
    print('Valor Total à pagar R$ {:.2f}'.format(total - (total * 10 / 100)))
elif escolha == 2:
    print('\033[1mVocê recebeu 5% de desconto.')
    print('Valor Total à pagar R$ {:.2f}'.format(total - (total * 5 / 100)))
elif escolha == 3:
    print('\033[1mParcelamento SEM JUROS.')
    print('Valor total das compras R$ {:.2f} em 2x sem JUROS de R$ {:.2f}'.format(total, total / 2))
elif escolha == 4:
    print('\033[1mParcelamento COM JUROS.')
    parcelas = int(input('EM QUANTAS VEZES QUER PARCELAR: '))
    if parcelas == 1:
        novo_total = total - (total * 5 / 100)
        print('\033[1mValor total das compras R$ {:.2f} com desconto de 5% em {}x SEM JUROS de R$ {:.2f}'.format(total, parcelas, (novo_total / parcelas)))
    elif parcelas == 2:
        print('\033[1mValor total das compras R$ {:.2f} em {}x SEM JUROS de R$ {:.2f}'.format(total, parcelas, (total / parcelas)))
    elif parcelas >= 3:
        novo_total = total + (total * 20 / 100)
        print('\033[1mValor total das compras R$ {:.2f} em {}x de R$ {:.2f} com JUROS de 20%'.format(total, parcelas, (novo_total / parcelas)))
elif escolha == 5:
    print('\033[1mCOMPRA CANCELADA !!! TENHA UM BOM DIA !!!')
else:
    print('OPÇÃO INVÁLIDA. TENTE NOVAMENTE')
    print('Sua compra de R$ {:.2f} ESTÁ AGUARDANDO PAGAMENTO'.format(total))
print('==========VOLTE SEMPRE !!!==========')
print('\033[36m=\033[m' * 70)
