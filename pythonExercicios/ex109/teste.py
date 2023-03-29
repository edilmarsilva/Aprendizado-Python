"""Modifique as funções que form criadas no desafio 107 para que elas aceitem um parâmetro
a mais, informando se o valor retornado por elas vai ser ou não formatado pela função moeda(),
desenvolvida no desafio 108."""
from ex109 import moeda


def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)



titulo('Formatando Moedas em Python')
preco = float(input('Digite o preço: R$ '))
print(f'A metade de {moeda.moeda(preco)} é {moeda.metade(preco, True)}')
print(f'O dobro de {moeda.moeda(preco)} é {moeda.dobro(preco, True)}')
print(f'Aumentando 10% em {moeda.moeda(preco)} temos {moeda.aumentar(preco, 10, True)}')
print(f'Reduzindo 13% em {moeda.moeda(preco)} temos {moeda.diminuir(preco, 13, True)}')
