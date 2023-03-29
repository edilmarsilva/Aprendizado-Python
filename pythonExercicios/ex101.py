"""Crie um programa que tenha uma função chamada voto() que vai receber como
parâmetro o ano de nascimento de uma pessoa, retornando um valor literal
indicando se uma pessoa tem voto NEGADO, OPCIONAL e OBRIGATÓRIO nas eleições."""
def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)


def voto(ano):
    from datetime import date
    idade = date.today().year - ano
    if idade < 16:
        msg = str(f'Com {idade} anos: NÃO VOTA!!!')
        return msg
    if 16 <= idade < 18 or idade >= 65:
        msg = str(f'Com {idade} anos: VOTO OPCIONAL !!!')
        return msg
    if 18 <= idade < 65:
        msg = str(f'Com {idade} anos: VOTO OBRIGATÓRIO !!!')
        return msg


#Programa Principal
titulo('Funções para votação')
anonasc = int(input('Em que ano você nasceu? '))
resp = voto(anonasc)
print(resp)
