"""Crie um programa onde o usuário possa digitar sete valores numéricos
 e cadastre-os em uma lista única que mantenha separados os valores pares e ímpares.
 No final, mostre os valores pares e ímpares em ordem crescente."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Listas com pares e ímpares":^50}')
print('\033[35m-*\033[m' * 25)
numeros = [[], []]
for c in range(1, 8):
    num = int(input(f'\033[1;34mDigite o {c}º valor: '))
    if num % 2 == 0:
        numeros[0].append(num)
    else:
        numeros[1].append(num)
print('\033[1;35m-=\033[m' * 30)
numeros[0].sort()
numeros[1].sort()
print(f'\033[1mOs valore pares digitados foram {numeros[0]}')
print(f'Os valores ímpares digitados foram {numeros[1]}')
print('\033[1;35m-=\033[m' * 30)
