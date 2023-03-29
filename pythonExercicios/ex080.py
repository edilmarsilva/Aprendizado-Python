"""Crie um programa onde o usuário possa digitar cinco valores numéricos e
cadastre-os em uma lista, já na posição correta de inserção (sem usar o sort()).
No final, mostre a lista ordenada na tela."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Lista ordenada sem repetições":^50}')
print('\033[35m-*\033[m' * 25)
numeros = []
for c in range(0, 5):
    num = int(input('\033[1;34mDigite um valor: '))
    if c == 0 or num > numeros[-1]:
        numeros.append(num)
        print('\033[1;33mAdicionado ao final da lista...')
    else:
        pos = 0
        while pos < len(numeros):
            if num <= numeros[pos]:
                numeros.insert(pos, num)
                print(f'\033[1;33mAdicionado na posição {pos}')
                break
            pos += 1
print('\033[1;35m-=\033[m' * 30)
print(f'\033[1mOs valores digitados em ordem foram: {numeros}')
print('\033[1;35m-=\033[m' * 30)
