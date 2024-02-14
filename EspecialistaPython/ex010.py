'''
Faça um programa que leia a largura e a altura de uma parede em metros,
calcule a sua área e a quantidade de tinta necessária para pintá-la,
sabendo que cada litro de tinta pinta uma área de 2 metros quadrados.
'''

largura = float(input('Digite a largura da parede: '))
altura = float(input('Digite a altura da parede: '))
area = altura * largura
tinta = area / 2
print(f'Para uma pintura que a parede tem {largura} x {altura}m totalizado {area}m de área.')
print(f'Precisará de {tinta} litros de tinta.')
