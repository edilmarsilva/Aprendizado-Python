"""Reescreva a função leiaInt() que fizemos no desafio 104, incluindo agora a
possibilidade da digitação de um número de tipo inválido. Aproveite e crie também uma
função leiaFloat() com a mesma funcionalidade."""
def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)


#Solução do Guanabara.
def leiaint(msg):
    while True:
        try:
            num = int(input(msg))
        except (ValueError, TypeError):
            print('\033[0;31mERRO ! Por favor digite um número inteiro válido.\033[m')
            continue
        except (KeyboardInterrupt):
            print('\033[0;31mNenhum valor digitado !!!\033[m')
            return 0
        else:
            return num


def leiaFloat(msg):
    while True:
        try:
            num = float(input(msg.replace(',', '.')))
        except (ValueError, TypeError):
            print('\033[0;31mPor favor, digite um número real válido.\033[m')
            continue
        except (KeyboardInterrupt):
            print('Nenhuma valor digitado')
            return 0
        else:
            return num




#def leiaint(msg):
#    while True:
#        num = str(input(msg))
#        if num.isnumeric():
#            return num
#            break
#        else:
#            print('\033[1;31mERRO! Digite um número inteiro válido.\033[m')


# Programa Principal
titulo('Funções aprofundadas em Python')
n1 = leiaint('Digite um número: ')
n2 = leiaFloat('Digite um número REAL: ')
print(f'O valor INTEIRO foi {n1} e o REAL foi {n2}')
