"""Crie um programa que vai ler vários números e colocar em uma lista.
Depois disso, mostre:
A) Quantos números foram digitados.
B) A lista de valores, ordenada de forma decrescente.
C) Se o valor 5 foi digitado e está ou não na lista."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Extraindo dados de uma Lista":^50}')
print('\033[35m-*\033[m' * 25)
lista = []
while True:
    resp = ' '
    lista.append(int(input('\033[1;34mDigite um valor: ')))
    while resp not in 'SN':
        resp = str(input('\033[1;35mQuer continuar? [S/N] ')).strip().upper()[0]
    if resp == 'N':
        break
print('\033[1;35m-=\033[m' * 30)
print(f'\033[1mForam digitados {len(lista)} valores no total.')
lista.sort(reverse=True)
print(f'Os valores em ordem decrescente são: {lista}')
if 5 in lista:
    print('O valor 5 faz parte da lista')
else:
    print('O valor 5 não faz parte da lista.')
print('\033[1;35m-=\033[m' * 30)
