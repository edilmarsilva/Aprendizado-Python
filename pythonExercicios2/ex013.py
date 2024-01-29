"""
Reajuste Salarial
Faça um algoritmo que leia o salário de um funcionário e mostre seu novo salário, com 15% de aumento.
"""
nome = str(input('Digite seu nome: '))
salario = float(input('Digite seu salário atual: R$ '))
novoSal = salario + (salario * 15 / 100)
print('==================================================================')
print(f'{nome} seu novo salário após o aumento de 15%, será de R$ {novoSal:.2f}')
print('==================================================================')
