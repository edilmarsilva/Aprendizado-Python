"""Escreva um programa que pergunte a quantidade de km percorridos por um carro alugado e a quantidade de dias pelos
quais ele foi alugado. Calcule o preço a pagar, sabendo que o carro custa R$60 por dia e R$0,15 por km rodado."""
print('\033[36m-=' * 20)
print('\033[31m         ALUGANDO UM CARRO')
print('\033[36m-=' * 20)
dia = int(input('\033[1;34mQuantos dias o carro ficou alugado? '))
km = float(input('Quantos km foram percorridos? '))
deve = (dia * 60) + (km * 0.15)
print('\033[36m*\033[m' * 40)
print('\033[1mO valor total à pagar é de R$ {:.2f}'.format(deve))
print('\033[36m*\033[m' * 40)
