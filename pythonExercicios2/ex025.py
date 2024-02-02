"""
Procurando uma string dentro de outra
Crie um programa que leia o nome de uma pessoa e diga se ela tem “SILVA” no nome.
"""
nome = str(input('Digite seu nome completo: ')).strip().upper()
separado = nome.split()
if 'SILVA' in separado:
    print(f"""Você tem em seu sobrenome o SILVA, A origem dos "Silvas" é controversa, 
    mas tudo indica que o sobrenome surgiu no Império Romano para denominar os habitantes 
    de regiões de matas ou florestas, "silva" que, em latim, significa "selva"1. 
    Muitos desses habitantes refugiaram-se do império justamente na península Ibérica1. 
    O sobrenome "Silva" é muito usado em Portugal e também foi dado a milhares de escravos 
    trazidos para o Brasil durante o período colonial""")
else:
    print(f'Você tem um sobrenome comum')