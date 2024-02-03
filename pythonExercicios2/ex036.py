"""
Aprovando Empréstimo
Escreva um programa para aprovar o empréstimo bancário para a compra de uma casa.
Pergunte o valor da casa, o salário do comprador e em quantos anos ele vai pagar.
A prestação mensal não pode exceder 30% do salário ou então o empréstimo será negado.
"""

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Aprovando Empréstimo":^40}')
print('\033[1;33m-=\033[m' * 20)

casa = float(input('\033[1mQual o valor da casa que deseja comprar: R$ '))
sal = float(input('Informe o valor do seu salário: R$ '))
prazo = int(input('Em quantos anos deseja quitar o financiamento: '))
prestacao = casa / (prazo * 12)
print('\033[36m=\033[m' * 50)
print(f'Para financiar uma casa de R$ {casa:.2f} em {prazo} anos, o valor da prestação será de R$ {prestacao:.2f} ')
print('\033[36m=\033[m' * 50)
if prestacao > sal * 0.30:
    print(f'\033[1mFinanciamento \033[1;31mREPROVADO\033[m pois o valor da parcela de R$ {prestacao:.2f} excede 30% do seu salário.')
elif prestacao <= sal * 0.30:
    print(f'\033[1mFinanciamento \033[1;32mAPROVADO\033[m.')
print('\033[36m=\033[m' * 50)
