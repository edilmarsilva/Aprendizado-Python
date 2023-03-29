"""Escreva um programa que pergunte o salário de um funcionário e calcule o valor do seu aumento. Para salários
superiores a R$1250,00, calcule um aumento de 10%. Para os inferiores ou iguais, o aumento é de 15%."""
print('\033[36m-=' * 20)
print('\033[31m         AUMENTO SALARIAL')
print('\033[36m-=' * 20)
sal = float(input('\033[1;34mQual o salário do funcionário? R$ '))
print('\033[36m=\033[m' * 80)
if sal <= 1250.00:
    nsal = sal + (sal * 15 / 100)
    print('\033[1mQuem ganhava R$ {:.2f} teve 15% de aumento e passa a ganhar R$ {:.2f}'.format(sal, nsal))
else:
    nsal = sal + (sal * 10 / 100)
    print('\033[1mQuem ganhava R$ {:.2f} teve 10% de aumento e passa a ganhar R$ {:.2f}'.format(sal, nsal))
print('\033[36m=\033[m' * 80)
