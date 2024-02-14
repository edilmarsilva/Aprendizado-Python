'''
Escreva um programa que leia um número inteiro digitado pelo usuário e retorne a sua tabuada
'''

num = int(input('Digite um número para ver sua tabuada: '))

for c in range(1, 11):
    print(f'{num} x {c} = {num * c}')
print('FIM DO PROGRAMA')