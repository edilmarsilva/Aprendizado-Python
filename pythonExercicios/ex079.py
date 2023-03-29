"""Crie um programa onde o usuário possa digitar vários valores numéricos e
cadastre-os em uma lista. Caso o número já exista lá dentro, ele não será adicionado.
No final, serão exibidos todos os valores únicos digitados, em ordem crescente."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Valores únicos em uma Lista":^50}')
print('\033[35m-*\033[m' * 25)
listanum = []
while True:
    resp = ' '
    n = int(input('\033[1;34mDigite um valor: '))
    if n not in listanum:
        listanum.append(n)
        print('\033[1;32mValor adicionado com sucesso.')
    else:
        print('\033[1;31mValor existente. Não adicionado !!!')
    while resp not in 'SN':
        resp = str(input('\033[1;35mQuer continuar? [S/N] ')).strip().upper()[0]
    if resp == 'N':
        break
print('\033[1;35m-=\033[m' * 25)
print(f'Você digitou os valores: {sorted(listanum)}')
print('\033[1;35m-=\033[m' * 25)
