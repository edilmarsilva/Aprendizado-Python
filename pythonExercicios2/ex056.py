"""
Analisador completo
Desenvolva um programa que leia o nome, idade e sexo de 4 pessoas.
No final do programa, mostre:
a média de idade do grupo,
qual é o nome do homem mais velho
e quantas mulheres têm menos de 20 anos.

"""

from datetime import date

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Analisador completo ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

media = 0
velho = ''
mulher20 = 0
cont = 0
maior = 0

for c in range(1, 5):
    print(f'-----{c}ª PESSOA -----')
    nome = str(input('Nome: ')).strip()
    nasc = int(input('Ano de Nascimento: '))
    idade = date.today().year - nasc
    sexo = str(input('Sexo [M/F]: ')).strip().upper()[0]
    cont += 1
    media += idade
    if sexo == 'M':
        if velho == '':
            velho = nome
            maior = idade
        elif idade > maior:
            velho = nome
            maior = idade
    if sexo == 'F' and idade < 20:
        mulher20 += 1

print('\033[36m=\033[m' * 42)
print(f'A média de idade do grupo é de {int(media / cont)} anos.')
print(f'O homem mais velho é o Sr. {velho} com {maior} anos de idade.')
print(f'O total de mulheres com menos de 20 anos é {mulher20}')
print('\033[36m=\033[m' * 42)
