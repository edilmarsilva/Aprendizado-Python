"""Crie um programa que tenha uma tupla única com nomes de produtos
e seus respectivos preços, na sequência. No final, mostre uma listagem
de preços, organizando os dados em forma tabular."""
print('\033[35m-*\033[m' * 25)
print('\033[1;33m{:-^50}'.format('Lista de Preços com Tupla'))
print('\033[35m-*\033[m' * 25)
produtos = 'Lápis', 1.75, \
           'Borracha', 2, \
           'Caderno', 15.90, \
           'Estojo', 25, \
           'Transferidor', 4.2, \
           'Compasso', 9.99, \
           'Mochila', 120.32, \
           'Caneta', 22.3, \
           'Livro', 34.9
print('\033[1;35m=' * 50)
print(f'\033[1;34m{"LISTAGEM DE PREÇOS":^50}')
print('\033[1;35m=\033[m' * 50)
for pos in range(0, len(produtos)):
    if pos % 2 == 0:
        print(f'\033[1m{produtos[pos]:_<39}', end=' ')
    else:
        print(f'\033[1mR$ {produtos[pos]:>7.2f}')
print('\033[1;35m-=\033[m' * 25)