"""Adicione o módulo moeda.py criado nos desafios anteriores, uma função chamada resumo(),
que mostre na tela algumas informações geradas pelas funções que já temos no módulo criado até aqui."""
from ex111 import moeda


def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)



titulo('Reduzindo ainda mais seu programa')
preco = float(input('Digite o preço: R$ '))
moeda.resumo(preco, 80, 35)
