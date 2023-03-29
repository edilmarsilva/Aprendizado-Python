"""Crie um programa que tenha a função leiaInt(), que vai funcionar de forma semelhante
‘a função input() do Python, só que fazendo a validação para aceitar apenas um valor numérico.
Ex: n = leiaInt(‘Digite um n: ‘)"""
def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)


#Solução do Guanabara.
def leiaint(msg):
    ok = False
    valor = 0
    while True:
        num = str(input(msg))
        if num.isnumeric():
            valor = int(num)
            ok = True
        else:
            print('\033[1;31mERRO! Digite um número inteiro válido.\033[m')
        if ok:
            break
    return valor

def leiaint(msg):
    while True:
        num = str(input(msg))
        if num.isnumeric():
            return num
            break
        else:
            print('\033[1;31mERRO! Digite um número inteiro válido.\033[m')


# Programa Principal
titulo('Validando entrada de dados em Python')
n = leiaint('Digite um número: ')
print(f'Você acabou de digitar o número {n}')
