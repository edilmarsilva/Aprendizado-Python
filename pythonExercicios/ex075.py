"""Desenvolva um programa que leia quatro valores pelo teclado
e guarde-os em uma tupla. No final, mostre:
A) Quantas vezes apareceu o valor 9.

B) Em que posição foi digitado o primeiro valor 3.

C) Quais foram os números pares."""
print('\033[35m-*\033[m' * 25)
print('\033[1;33m{:-^50}'.format('Análise de dados em uma Tupla'))
print('\033[35m-*\033[m' * 25)
num = int(input('\033[1;34mDigite um número: ')), \
      int(input('Digite outro número: ')), \
      int(input('Digite mais um número: ')), \
      int(input('Digite o último número: '))
print('\033[35m-=\033[m' * 25)
print('\033[1mOs números digitados foram: ', end='')
for n in num:
    print(f'{n} ', end=' ')
print('\n')
print('\033[35m-=\033[m' * 25)
if 9 in num:
    print(f'\n\033[1mO número 9 apareceu {num.count(9)} vezes.')
print('\033[35m-=\033[m' * 25)
if 3 in num:
    print(f'\n\033[1mO número 3 apareceu na {num.index(3) + 1}ª posição.')
print('\033[35m-=\033[m' * 25)
contpar = 0
for c, par in enumerate(num):
    if par % 2 == 0:
        c += 1
        contpar += 1
if contpar > 0:
    print(f'\n\033[1mAo todo foram digitados {contpar} valores pares.')
print('\033[35m-=\033[m' * 25)