"""
Verificando as primeiras letras de um texto
Crie um programa que leia o nome de uma cidade diga se ela começa ou não com o nome “SANTO”.
"""
cidade = str(input('Digite uma cidade: ')).strip().upper()
separado = cidade.split()
if 'SANTO' in separado[0]:
    print(f'A cidade digitada é sagrada.')
else:
    print(f'Essa cidade teve uma nomeação comum')
