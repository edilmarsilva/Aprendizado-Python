"""
Primeiro e último nome de uma pessoa
Faça um programa que leia o nome completo de uma pessoa,
mostrando em seguida o primeiro e o último nome separadamente.
"""
nome = str(input('Digite seu nome completo: ')).strip()
separado = nome.split()
print(f'Primeiro nome: {separado[0]}')
print(f'Último nome: {separado[-1]}')
