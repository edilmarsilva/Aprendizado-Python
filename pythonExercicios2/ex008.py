"""
Conversor de Medidas
Escreva um programa que leia um valor em metros e o exiba convertido em centímetros e milímetros.
"""
m = float(input('Digite uma distância em metros: '))
km = m / 1000
hm = m / 100
dam = m / 10
dm = m * 10
cm = m * 100
mm = m * 1000
print(f'{m} metro(s) correspondem a {km} km (quilometro)')
print(f'{m} metro(s) correspondem a {hm} hm (hectômetro)')
print(f'{m} metro(s) correspondem a {dam} dam (decâmentro)')
print(f'{m} metro(s) correspondem a {dm} dm (decímetro)')
print(f'{m} metro(s) correspondem a {cm} cm (centímetro)')
print(f'{m} metro(s) correspondem a {mm} mm (milimetro).')
