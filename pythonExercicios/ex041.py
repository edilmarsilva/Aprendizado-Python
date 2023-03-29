"""A Confederação Nacional de Natação precisa de um programa
que leia o ano de nascimento de um atleta e mostre a sua categoria,
conforme a idade:
–Até 9 anos: MIRIM
–Até 14 anos: INFANTIL
–Até 19 anos: JÚNIOR
–Até 25 anos: SÊNIOR
–Acima de 25 anos: MASTER"""
from datetime import date
print('\033[36m-=' * 20)
print('\033[31m         CATEGORIZANDO O ATLETA')
print('\033[36m-=' * 20)
nasc = int(input('\033[1;34mDigite o ano do seu nascimento: '))
idade = date.today().year - nasc
print('\033[36m=\033[m' * 30)
print('\033[1mO atleta tem {} anos de idade.'.format(idade))
if idade <= 9:
    print('\033[44mCATEGORIA: MIRIM\033[m')
elif 9 < idade <= 14:
    print('\033[44mCATEGORIA: INFANTIL\033[m')
elif 14 < idade <= 19:
    print('\033[44mCATEGORIA: JUNIOR\033[m')
elif 19 < idade <= 25:
    print('\033[44mCATEGORIA: SENIOR\033[m')
elif idade > 25:
    print('\033[44mCATEGORIA: MASTER\033[m')
print('\033[36m=\033[m' * 30)
