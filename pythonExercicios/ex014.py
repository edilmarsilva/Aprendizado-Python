"""Escreva um programa que converta uma temperatura digitando em graus Celsius e converta para graus Fahrenheit."""
print('\033[36m-=' * 20)
print('\033[31m         CONVERTENDO TEMPERATURAS')
print('\033[36m-=' * 20)
c = float(input("\033[1;34mInforme a temperatura em °C: "))
f = (c * 9 / 5) + 32
print('\033[36m*\033[m' * 40)
print('\033[1;mA tempertura de {:.1f}°C é de {:.1f}°F'.format(c, f))
print('\033[36m*\033[m' * 40)
