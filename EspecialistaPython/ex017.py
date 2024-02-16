"""
Escreva um programa para aprovar o empréstimo bancário para a compra de uma casa.
Pergunte o valor da casa, o salário do comprador e em quantos anos ele vai pagar.
A prestação mensal não pode exceder 30% do salário ou então o empréstimo será negado.
"""

casa = float(input('Qual o valor do imóvel: R$ '))
salario = float(input('Qual seu salário: R$ '))
anos = int(input('Em quantos anos vai parcelar: '))
prazo = anos * 12
prestacao = casa / prazo

if prestacao <= salario * (30/100):
    print('\033[32mEMPRÉSTIMO APROVADO\033[m')
    print(f'VALOR DO IMÓVEL R$ {casa:.2f}')
    print(f'FINANCIAMENTO EM {prazo} meses')
    print(f'PRESTAÇÃO R$ {prestacao:.2f}')
    print('PARABÉNS')
else:
    print('\033[31mEMPRÉSTIMO NEGADO\033[m')
    print(f'VALOR DO IMÓVEL R$ {casa:.2f}')
    print(f'FINANCIAMENTO EM {prazo} meses')
    print(f'PRESTAÇÃO R$ {prestacao:.2f}')
    print('O VALOR DA PRESTAÇÃO SUPERA 30% DE SEU SALÁRIO')
    print(f'Valor máximo de prestação para aprovação R$ {salario * (30/100):.2f}')
