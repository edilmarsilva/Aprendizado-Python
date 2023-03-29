"""Desenvolva um programa que pergunte a distância de uma viagem em km. Calcule o preço da passagem, cobrando
R$ 0,50 por km para viagens de até 200Km e R$0,45 para viagens mais longas."""
print('\033[36m-=' * 20)
print('\033[31m    RODOVIÁRIA ===> BILHETERIA')
print('\033[36m-=' * 20)
from time import sleep
local = str(input('\033[1;34mQual o destino da sua viagem? '))
distancia = float(input('Qual é a distância da dua viagem? '))
print('\033[35m*' * 75)
print('\033[33mVocê está prestes a começar sua viagem com destino à {} de {:.1f} km'.format(local, distancia))
print('Aguarde enquanto calculamos o valor da sua passagem...')
print('\033[35m*' * 75)
sleep(6)
print('\033[36m=\033[m' * 65)
if distancia <= 200:
    preco = float(distancia * 0.50)
    print('\033[1mO preço da sua passagem com destino à {} é de R$ {:.2f}'.format(local, preco))
else:
    preco = float(distancia * 0.45)
    print('\033[1mO preço da sua passagem com destino à {} é de R$ {:.2f}'.format(local, preco))
print('\033[36m=\033[m' * 65)
print('-=' * 10, '\033[1;42mTENHA UMA BOA VIAGEM\033[m', '-=' * 10)
