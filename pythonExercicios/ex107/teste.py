"""Crie um módulo chamado moeda.py que tenha as funções incorporadas aumentar(),
diminuir(), dobro() e metade(). Faça também um programa que importe esse módulo e
use algumas dessas funções."""
from ex107 import moeda


def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)



titulo('Exercitando módulos em Python')
preco = float(input('Digite o preço: R$ '))
print(f'A metade de R$ {preco:.2f} é R$ {moeda.metade(preco):.2f}')
print(f'O dobro de R$ {preco:.2f} é R$ {moeda.dobro(preco):.2f}')
print(f'Aumentando 10% em R$ {preco:.2f} temos R$ {moeda.aumentar(preco, 10):.2f}')
print(f'Reduzindo 13% em R$ {preco:.2f} temos R$ {moeda.diminuir(preco, 13):.2f}')
