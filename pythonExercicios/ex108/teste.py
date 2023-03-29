"""Adapte o código do desafio #107, criando uma função adicional
chamada moeda() que consiga mostrar os números como um valor monetário formatado."""
from ex109 import moeda


def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)



titulo('Formatando Moedas em Python')
preco = float(input('Digite o preço: R$ '))
print(f'A metade de {moeda.moeda(preco)} é {moeda.moeda(moeda.metade(preco))}')
print(f'O dobro de {moeda.moeda(preco)} é {moeda.moeda(moeda.dobro(preco))}')
print(f'Aumentando 10% em {moeda.moeda(preco)} temos {moeda.moeda(moeda.aumentar(preco, 10))}')
print(f'Reduzindo 13% em {moeda.moeda(preco)} temos {moeda.moeda(moeda.diminuir(preco, 13))}')
