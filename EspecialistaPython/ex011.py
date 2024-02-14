"""
Escreva um programa que pergunte a quantidade de Km percorridos por um carro alugado,
a quantidade de dias pelos quais ele foi alugado e se o cliente faz parte do programa de fidelidade
da loja. Calcule o preço a pagar, sabendo que o carro custa R$ 60 por dia e R$ 0,15 por Km rodado
para clientes não participantes do programa de fidelidade e R$ 58 a diária mais R$0,05 por Km
rodado para clientes participantes do programa de fidelidade.
"""

km = float(input('Informe a quantidade de km percorrido com o vaículo: '))
dias = int(input('Quantos dias ficou com o veículo: '))
resp = str(input('Tem programa de fidelidade? [S/N] ')).strip().upper()[0]

print(f'{"RELATÓRIO FINAL":=^50}')

if resp == 'S':
    print(f'O valor do aluguel é R$ {dias * 58:.2f}')
    print(f'Você percorreu {km} km e será cobrado o valor de R$ {km * 0.05:.2f}')
    print(f'TOTALIZANDO R$ {(dias * 58) + (km * 0.05):.2f}')
else:
    print(f'O valor do aluguel é R$ {dias * 60:.2f}')
    print(f'Você percorreu {km} km e será cobrado o valor de R$ {km * 0.15:.2f}')
    print(f'TOTALIZANDO R$ {(dias * 60) + (km * 0.15):.2f}')
print(f'{"VOLTE SEMPRE":=^50}')
