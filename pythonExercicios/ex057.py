"""Faça um programa que leia o sexo de uma pessoa, mas só aceite os valores ‘M’ ou ‘F’.
Caso esteja errado, peça a digitação novamente até ter um valor correto."""
print('\033[36m-=' * 20)
print('\033[31m        PRIMEIRA VALIDAÇÃO DE DADOS')
print('\033[36m-=' * 20)
sexo = str(input('\033[1;34mInforme seu sexo: [M/F] ')).upper()[0].strip()
while sexo not in 'FM':
    sexo = str(input('Dados inválidos. Por favor, informe seu sexo: ')).upper()[0].strip()
print('\033[36m=\033[m' * 30)
print(''f'Sexo {sexo} registrado com sucesso.')
print('\033[36m=\033[m' * 30)
