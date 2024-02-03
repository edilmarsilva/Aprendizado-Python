"""
Aumentos múltiplos
Escreva um programa que pergunte o salário de um funcionário e calcule o valor do seu aumento.
Para salários superiores a R$1250,00, calcule um aumento de 10%. Para os inferiores ou iguais,
o aumento é de 15%.
"""
print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Aumentos múltiplos":^40}')
print('\033[1;33m-=\033[m' * 20)

sal = float(input('\033[1;35mQual o salário do funcionário? R$ '))
print('\033[36m=\033[m' * 80)
if sal > 1250:
    print(f'\033[1mQuem ganhava R$ {sal:.2f} receberá 10% de aumento e passará receber R$ {sal + sal*0.10:.2f}')
else:
    print(f'\033[1mQuem ganhava R$ {sal:.2f} receberá 15% de aumento e passará receber R$ {sal + sal*0.15:.2f}')
print('\033[36m=\033[m' * 80)
