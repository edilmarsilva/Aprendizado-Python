"""
Validação de Dados
Faça um programa que leia o sexo de uma pessoa, mas só aceite os valores ‘M’ ou ‘F’.
Caso esteja errado, peça a digitação novamente até ter um valor correto.
"""

print('\033[1;33m-=' * 21)
print(f'=\033[1;34m{" Validação de Dados ":+^40}\033[1;33m=')
print('\033[1;33m-=\033[m' * 21)

sexo = str(input('Informe seu sexo: [M/F] ')).strip().upper()[0]
while sexo not in 'MF':
    sexo = str(input('Dados inválidos. Por favor, informe seu sexo: [M/F] ')).strip().upper()[0]

if sexo == 'M':
    sexo = 'MASCULINO'
else:
    sexo = 'FEMININO'

print(f'Sexo {sexo} registrado com sucesso.')
print('\033[36m=\033[m' * 42)
