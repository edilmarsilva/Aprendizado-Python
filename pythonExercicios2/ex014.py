"""
Conversor de Temperaturas
Escreva um programa que converta uma temperatura digitando em graus Celsius e converta para graus Fahrenheit.
"""
celsius = float(input('Informe a temperatura em graus celsius ºC: '))
fahrenheit = celsius * 1.8 + 32
print(f'A temperatura de {celsius:.1f}ºC corresponde a {fahrenheit:.1f}ºF')
