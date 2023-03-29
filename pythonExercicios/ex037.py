"""Escreva um programa em Python que leia um número inteiro qualquer
e peça para o usuário escolher qual será a base de conversão:
1 para binário,
2 para octal e
3 para hexadecimal."""
print('\033[36m-=' * 20)
print('\033[31m        CONVERTENDO UM NÚMERO')
print('\033[36m-=' * 20)
num = int(input('\033[1;34mDigite um número inteiro: '))
print('''\033[35mEscolha uma das bases para conversão: 
[1] Converter para BINARIO
[2] Converter para OCTAl
[3] Converter para HEXADECIMAL''')
escolha = int(input('\033[1;34mEscolha uma opção: '))
print('\033[36m=\033[m' * 50)
if escolha == 1:
    print('\033[1mO número {} convertido em BINÁRIO é igual a {}'.format(num, bin(num)[2:]))
elif escolha == 2:
    print('\033[1mO número {} convertido em OCTAL é igual a {}'.format(num, oct(num)[2:]))
elif escolha == 3:
    print('\033[1mO número {} convertido em HEXADECIMAL é igual a {}'.format(num, hex(num)[2:]))
else:
    print('\033[31mOPÇÃO INVÁLIDA, TENTE NOVAMENTE')
print('\033[36m=\033[m' * 50)
