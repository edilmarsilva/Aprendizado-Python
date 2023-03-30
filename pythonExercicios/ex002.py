"""Faça um programa que leia o nome de uma pessoa e mostre uma mensagem de boas-vindas."""
from datetime import date

nome = input('\033[1;33mQUAL O SEU NOME? ')
print(f'\033[1;30;41mSeja bem vindo {nome} ao seu curso de \033[4;30;41mPYTHON !!!\033[m')
ano_nasc = int(input('\033[1;33mDigite seu ano de nascimento: '))
print(f'Agora já sei que seu nome é {nome} e sua idade é {date.today().year - ano_nasc}')
