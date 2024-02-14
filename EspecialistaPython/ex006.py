'''
Escreva um programa que leia um número digitado pelo usuário e retorne o seu antecessor
e o seu sucessor.
Vamos considerar como antecessor o número inteiro imediatamente inferior ao número digitado e
como sucessor o inteiro imediatamente superior ao número digitado
'''

num = int(input('Digite um número para ver seu sucessor e seu antecessor: '))
print(f'O sucessor de {num} é {num + 1} e seu antecessor é {num - 1}.')
