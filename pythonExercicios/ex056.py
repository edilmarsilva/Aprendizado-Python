"""Desenvolva um programa que leia o nome, idade e sexo de 4 pessoas.
No final do programa, mostre: a média de idade do grupo, qual é o nome do homem mais velho
e quantas mulheres têm menos de 20 anos."""
print('\033[36m-=' * 20)
print('\033[31m           CLASSIFICANDO PESSOAS')
print('\033[36m-=' * 20)
somaidade = 0
mediaidade = 0
velho = 0
nomevelho = ''
contmulher = 0
for c in range(1, 5):
    print('\033[1;35m'f'----- {c}ª PESSOA-----')
    nome = str(input('\033[1;34mNOME: ')).strip()
    idade = int(input('IDADE: '))
    sexo = str(input('SEXO: [M/F] ')).strip()
    somaidade = somaidade + idade
    if c == 1 and sexo in 'Mm':
        velho = idade
        nomevelho = nome
    if sexo in 'Mm' and idade > velho:
        velho = idade
        nomevelho = nome
    if sexo in 'Ff' and idade < 20:
        contmulher += 1
mediaidade = somaidade / 4
print('\033[36m=\033[m' * 50)
print('\033[1m'f'A média de idade do grupo é de {mediaidade} anos.')
print(''f'O homem mais velho tem {velho} anos e se chama {nomevelho}.')
print(''f'Temos um total de {contmulher} mulheres com menos de 20 anos. ')
print('\033[36m=\033[m' * 50)
