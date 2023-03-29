"""Faça um programa que mostre uma contagem regressiva na tela para o estouro de fogos de artifício, indo de 10 até 0,
com uma pausa de 1 segundo entre eles."""
import emoji
from time import sleep

print('\033[36m-=' * 20)
print('\033[31m         CONTAGEM REGRESSIVA')
print('\033[36m-=' * 20)
print('\033[36m=\033[m' * 40)
for c in range(10, -1, -1):
    print('\033[1m', c)
    sleep(1)
print('\033[36m=\033[m' * 20)
print(emoji.emojize('Feliz ano novo :boom:', language='alias'))
print('\033[36m=\033[m' * 20)
