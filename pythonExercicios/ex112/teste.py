"""Dentro do pacote utilidadesCeV que criamos no desafio 111,
temos um módulo chamado dado. Crie uma função chamada leiaDinheiro()
que seja capaz de funcionar como a função imputa(), mas com uma
validação de dados para aceitar apenas valores que seja monetários."""
from ex112.utilidadesCeV import moeda
from ex112.utilidadesCeV import dado

def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)



titulo('Entrada de dados monetários')
preco = dado.leiaDinheiro('Digite o preço: R$ ')
moeda.resumo(preco, 30, 15)
