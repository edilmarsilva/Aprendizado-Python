"""
Pintando Parede
Faça um programa que leia a largura e a altura de uma parede em metros, calcule a sua área e a quantidade de tinta
necessária para pintá-la, sabendo que cada litro de tinta pinta uma área de 2 metros quadrados.
"""
largura = float(input('Largura da parede: '))
altura = float(input('Altura da parede: '))
area = largura * altura
tinta = area / 2
print(f'Sua parede tem a dimensão de {largura:.2f} x {altura:.2f} e sua área é de {area:.2f}m²')
print(f'Para pintar essa parede, vodê precisará de {tinta:.2f}l de tinha.')
