"""
Conversor de Bases Numéricas
Escreva um programa em Python que leia um número inteiro qualquer e peça para o usuário
escolher qual será a base de conversão: 1 para binário, 2 para octal e 3 para hexadecimal.
"""

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Conversor de Bases Numéricas":^40}')
print('\033[1;33m-=\033[m' * 20)

num = int(input('Digite um número inteiro: '))

print("""
Escolha uma das bases para conversão:
[ 1 ] Converter para BINÁRIO
[ 2 ] Converter para OCTAL
[ 3 ] Converter para HEXADECIMAL
""")
escolha = int(input('Sua opção: '))
print('\033[36m=\033[m' * 50)
if escolha == 1:
    print(f'O número {num} convertido para BINÁRIO é {bin(num)[2:]}')
elif escolha == 2:
    print(f'O número {num} convertido para OCTAL é {oct(num)[2:]}')
elif escolha == 3:
    print(f'O número {num} convertido para HEXADECIMAL é {hex(num)[2:]}')
else:
    print('Opção Inválida')
print('\033[36m=\033[m' * 50)
