"""Faça um programa que mostre a tabuada de vários números,
um de cada vez, para cada valor digitado pelo usuário.
O programa será interrompido quando o número solicitado
for negativo."""
print('\033[35m-*\033[m' * 15)
print('\033[1;33m   Tabuada v3.0  ')
print('\033[35m-*\033[m' * 15)
while True:
    num = int(input('\033[1;34mDigite um número para ver a sua TABUADA: '))
    if num < 0:
        break
    print('\033[35m#-\033[m' * 8)
    for c in range(1, 11):
        print(f'{num} x {c:2} = {num * c}')
        c += 1
    print('\033[35m#-\033[m' * 8)
print('\033[36m=\033[m' * 60)
print('\033[33mPROGRAMA ENCERRADO.')
print('\033[36m=\033[m' * 60)
