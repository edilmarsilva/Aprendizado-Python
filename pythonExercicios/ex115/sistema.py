from ex115.lib.interface import *
from time import sleep
from ex115.lib.arquivo import *

arq = 'cursoemvideo.txt'

if not arquivoExiste(arq):
    criarArquivo(arq)

while True:
    resposta = menu(['CONSULTAR', 'INCLUIR', 'SAIR'])
    if resposta == 1:
        lerArquivo(arq)
    elif resposta == 2:
        cabecalho('NOVO CADASTRO')
        nome = str(input('NOME: '))
        idade = leiaInt('IDADE: ')
        cadastrar(arq, nome, idade)
    elif resposta == 3:
        cabecalho('SAINDO DO SISTEMA...ATÉ LOGO')
        break
    else:
        print(f'\033[31mERRO! OPÇÃO INVÁLIDA !!!\033[m')
    sleep(2)
