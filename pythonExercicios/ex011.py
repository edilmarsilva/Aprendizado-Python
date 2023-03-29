"""Faça um programa que leia a largura e a altura de uma parede em metros, calcule a sua área e a quantidade de tinta
necessária para pintá-la, sabendo que cada litro de tinta pinta uma área de 2 metros quadrados."""
print('\033[36m-=' * 20)
print('\033[31m         PINTANDO UMA PAREDE')
print('\033[36m-=' * 20)
larg = float(input('\033[1;34mQUAL A LARGURA DA PAREDE:\033[m '))
alt = float(input('\033[1;34mQUAL A ALTURA DA PAREDE:\033[m '))
area = larg * alt
d = area / 2
lt = d * 35.98
print('\033[36m#\033[m'*90)
print('\033[1mSua parede tem a dimensão de {:.3f} x {:.3f} e sua área é de {:.3f}'.format(larg, alt, area))
print('Para pintar uma parede com a área de {:.3f} precisará de {:.3f} litros de tinta !!!'.format(area, d))
print('Com o litro da tinta custando R$ 35.98 gastará R$ {:.2f} para pintar a parede'.format(lt))
print('\033[36m#'*90)
