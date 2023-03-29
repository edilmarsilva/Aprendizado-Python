"""Crie um programa que declare uma matriz de dimensão 3×3 e preencha com valores
lidos pelo teclado. No final, mostre a matriz na tela, com a formatação correta."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Matriz em Python":^50}')
print('\033[35m-*\033[m' * 25)
matriz = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
for l in range(0, 3):
    for c in range(0, 3):
        matriz[l][c] = int(input(f'\033[1;34mDigite um valor para a posição [{l}, {c}]: '))
print('\033[1;35m-=\033[m' * 30)
for l in range(0, 3):
    for c in range(0, 3):
        print(f'\033[1m[{matriz[l][c]:^5}]', end='')
    print()
print('\033[1;35m-=\033[m' * 30)
