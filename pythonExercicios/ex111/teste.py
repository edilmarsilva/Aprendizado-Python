"""Crie um pacote chamado utilidadesCeV que tenha dois módulos internos chamados moeda e dado.
Transfira todas as funções utilizadas nos desafios 107, 108 e 109 para o primeiro pacote e
mantenha tudo funcionando."""
from ex111.utilidadesCeV import moeda


def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)



titulo('Transformando módulos em pacotes')
preco = float(input('Digite o preço: R$ '))
moeda.resumo(preco, 80, 35)
