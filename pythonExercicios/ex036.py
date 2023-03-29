"""Escreva um programa para aprovar o empréstimo bancário para a compra de uma casa. Pergunte o valor da casa,
o salário do comprador e em quantos anos ele vai pagar.
A prestação mensal não pode exceder 30% do salário ou então o empréstimo será negado."""
from time import sleep
print('\033[36m-=' * 20)
print('\033[31m         SONHO DA CASA PRÓPRIA')
print('\033[36m-=' * 20)
valor = float(input('\033[1;34mQual o valor da casa R$ '))
sal = float(input('Qual o seu salário mensal R$ '))
prazo = int(input('Em quantos anos pretende quitar esse financiamento? '))
print('\033[35mANALISANDO SEU FINANCIAMENTO...')
sleep(5)
print('\033[36m=\033[m' * 90)
prestacao = valor / (prazo * 12)
print('\033[1mPara comprar uma casa de R$ {:.2f} e pagar em {} anos, sua prestação será de R$ {:.2f}'.format(valor, prazo, prestacao))
print('\033[35mÚLTIMO ESTÁGIO DA ÁNALISE')
sleep(5)
if prestacao < sal * 30 / 100:
    print('\033[32mPARABÉNS !!! SEU EMPRÉSTIMO FOI APROVADO')
else:
    print('\033[31mNÃO FOI DESSA VEZ !!! SEU EMPRÉSTIMO FOI NEGADO')
print('\033[36m=\033[m' * 90)
