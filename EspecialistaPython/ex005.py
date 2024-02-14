'''
 Escreva um programa que leia o nome completo do usuário e retorne ele em maísculas,
 minúsculas, capitalizado e em formatação de título
'''

nome = str(input('Digite seu nome completo: '))
print(f'Seu nome todo em maíúcuslas é {nome.upper()}')
print(f'Seu nome todo em capitalizado é {nome.capitalize()}')
print(f'Seu nome todo como um título é {nome.title()}')
