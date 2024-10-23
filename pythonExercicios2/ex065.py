"""
Crie um programa que leia vários números inteiros pelo teclado. No final da execução,
mostre a média entre todos os valores e qual foi o maior e o menor valores lidos.
O programa deve perguntar ao usuário se ele quer ou não continuar a digitar valores.
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Maior e Menor valores ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

resp = 'S'
cont = soma = 0
while resp == 'S':
    num = int(input('Digite um valor: '))
    cont += 1
    soma += num
    if cont == 1:
        maior = menor = num
    else:
        if num >= maior:
            maior = num
        else:
            menor = num
    resp = str(input('Quer continuar? [S/N]: ')).strip().upper()[0]
media = soma / cont
print(f'A média entre os valores digitados é {media}')
print(f'Foram digitados {cont} valores.')
print(f'O maior número digitado foi {maior} e o menor foi {menor}.')
print('\033[36m=\033[m' * 42)
