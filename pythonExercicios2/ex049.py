"""
Tabuada v.2.0
Refaça o DESAFIO 9, mostrando a tabuada de um número que o usuário escolher,
só que agora utilizando um laço for.
"""

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{" Tabuada v.2.0 ":+^40}')
print('\033[1;33m-=\033[m' * 20)

num = int(input('Quer ver a tabuada de qual número: '))
print('\033[36m=\033[m' * 40)
for c in range(1, 11):
    print(f'{num} x {c:>2} = {num * c} ')
print('\033[36m=\033[m' * 40)
