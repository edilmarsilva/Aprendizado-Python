"""Crie um programa que vai ler vários números e colocar em uma lista.
Depois disso, crie duas listas extras que vão conter apenas os valores pares
e os valores ímpares digitados, respectivamente.
Ao final, mostre o conteúdo das três listas geradas."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Dividindo valores em várias listas":^50}')
print('\033[35m-*\033[m' * 25)
lista = []
pares = []
impares = []
while True:
    resp = ' '
    num = int(input('\033[1;34mDigite um valor: '))
    while resp not in 'SN':
        resp = str(input('\033[1;35mQuer continuar? [S/N] ')).strip().upper()[0]
    lista.append(num)
    if num % 2 == 0:
        pares.append(num)
    else:
        impares.append(num)
    if resp == 'N':
        break
print('\033[1;35m-=\033[m' * 30)
print(f'\033[1mA lista completa do números é: {lista}')
print(f'A lista de números pares é: {pares}')
print(f'A lista de números ímpares é: {impares}')
print('\033[1;35m-=\033[m' * 30)
