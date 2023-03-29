"""Aprimore o desafio anterior, mostrando no final:
A) A soma de todos os valores pares digitados.
B) A soma dos valores da terceira coluna.
C) O maior valor da segunda linha."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Mais sobre Matriz em Python":^50}')
print('\033[35m-*\033[m' * 25)
matriz = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
pares = tc = msc = 0
for l in range(0, 3):
    for c in range(0, 3):
        matriz[l][c] = int(input(f'\033[1;34mDigite um valor para a posição [{l}, {c}]: '))
print('\033[1;35m-=\033[m' * 30)
for l in range(0, 3):
    for c in range(0, 3):
        print(f'\033[1m[{matriz[l][c]:^5}]', end='')
        if matriz[l][c] % 2 == 0:
            pares += matriz[l][c]
    print()
for l in range(0, 3):
    tc += matriz[l][2]
for c in range(0, 3):
    if c == 0:
        msc = matriz[1][c]
    elif matriz[1][c] > msc:
        msc = matriz[1][c]
print('\033[1;35m-=\033[m' * 30)
print(f'\033[1mA soma dos valores pares é: {pares}')
print(f'A soma dos valores da terceira coluna é: {tc}')
print(f'O maior valor da segunda linha é: {msc}')
print('\033[1;35m-=\033[m' * 30)
