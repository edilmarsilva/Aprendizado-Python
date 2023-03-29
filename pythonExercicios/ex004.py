from time import sleep

"""Faça um programa que leia algo pelo teclado e mostre na tela o seu tipo primitivo e todas as
informações possíveis sobre ele."""
a = input('\033[7;40mDIGITE ALGO:\033[m ')
sleep(2)
print('\033[1;35;40mO tipo primitivo digitado é:\033[m ', type(a))
sleep(2)
print('\033[1;35;40mSó tem espaços?\033[m ', a.isspace())
sleep(2)
print('\033[1;35;40mÉ um número?\033[m ', a.isnumeric())
sleep(2)
print('\033[1;35;40mÉ alfabético?\033[m ', a.isalpha())
sleep(2)
print('\033[1;35;40mÉ alfanumérico?\033[m ', a.isalnum())
sleep(2)
print('\033[1;35;40mEstá em maiúsculas?\033[m ', a.isupper())
sleep(2)
print('\033[1;35;40mEstá em minúsculas?\033[m ', a.islower())
sleep(2)
print('\033[1;35;40mEstá capitalizada?\033[m ', a.istitle())

