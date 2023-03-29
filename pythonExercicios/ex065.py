"""Crie um programa que leia vários números inteiros pelo teclado.
No final da execução, mostre a média entre todos os valores e qual foi o maior
e o menor valores lidos.
O programa deve perguntar ao usuário se ele quer ou não continuar a digitar valores."""
print('\033[36m-=' * 20)
print('\033[31m      Maior e Menor valores')
print('\033[36m-=' * 20)
print('\033[36m=\033[m' * 40)
cont = media = maior = menor = soma = 0
resp = 'S'
while resp in 'S':
    num = int(input('\033[35mDigite um número: '))
    soma += num
    cont += 1
    media = soma / cont
    if cont == 1:
        maior = menor = num
    else:
        if num > maior:
            maior = num
        if num < menor:
            menor = num
    resp = str(input('Quer continuar [S/N] ')).strip()[0].upper()
print('\033[36m=\033[m' * 60)
print(''f'\033[1mVocê digitou {cont} números e a média entre eles foi {media:.2f}')
print(''f'O maior valor digitado foi {maior} e o menor foi {menor}.')
print('\033[36m=\033[m' * 60)
