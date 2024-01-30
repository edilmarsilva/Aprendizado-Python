"""
Seno, Cosseno e Tangente
Faça um programa que leia um ângulo qualquer e mostre na tela
 o valor do seno, cosseno e tangente desse ângulo.
"""
import math
ang = float(input('Digite o angulo que você deseja: '))
sen = math.sin(math.radians(ang))
cos = math.cos(math.radians(ang))
tan = math.tan(math.radians(ang))
print(f'O ângulo de {ang}º tem o SENO de {sen:.2f}')
print(f'O ângulo de {ang}º tem o COSSENO de {cos:.2f}')
print(f'O ângulo de {ang}º tem a TANGENTE de {tan:.2f}')
