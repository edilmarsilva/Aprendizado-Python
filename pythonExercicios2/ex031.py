"""
Custo da Viagem
Desenvolva um programa que pergunte a distância de uma viagem em Km.
Calcule o preço da passagem, cobrando R$0,50 por Km para viagens de até 200Km e R$0,45
para viagens mais longas.
"""
print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Custo da Viagem":^40}')
print('\033[1;33m-=\033[m' * 20)
distancia = int(input('\033[1mQuantos quilometros percorrerá em sua viagem: '))
if distancia > 200:
    custo = distancia * 0.45
    print(f'\033[1;33mValor da passagem para sua viagem é R$ {custo:.2f}')
elif distancia <= 200:
    custo = distancia * 0.50
    print(f'O valor da passagem para sua viagem é R$ {custo:.2f}')
print(f'\033[1;36m{"TENHA UMA BOA VIAGEM":^40}')
