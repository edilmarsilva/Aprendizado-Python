"""Crie um programa que tenha uma tupla com várias palavras
(não usar acentos). Depois disso, você deve mostrar, para
cada palavra, quais são as suas vogais."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Contando vogais em Tupla":^50}')
print('\033[35m-*\033[m' * 25)
palavras = 'Aprender', 'Programar', 'Linguagem', 'Phithon', 'Curso', \
           'Gratis', 'Estudar', 'Praticar', 'Trabalhar', 'Mercado', \
           'Programador', 'Futuro', 'Frango', 'Peito', 'Embraco', \
           'Faturamento', 'Aumento'
print('\033[1;35m-=\033[m' * 25)
for p in palavras:
    print(f'\033[1m\nNa palvra {p.upper()} temos as seguintes vogais: ', end='')
    for letra in p:
        if letra.lower() in 'aeiou':
            print(letra.lower(), end=' ')
print('')
print('\033[1;35m-=\033[m' * 25)
