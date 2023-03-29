"""Crie um programa onde o usuário digite uma expressão qualquer que use parênteses.
Seu aplicativo deverá analisar se a expressão passada está
com os parênteses abertos e fechados na ordem correta."""
print('\033[35m-*\033[m' * 25)
print(f'\033[1;34m{"Validando expressões matemáticas":^50}')
print('\033[35m-*\033[m' * 25)
expressao = str(input('\033[1;34mDigite uma expressão: '))
pilha = []
for digito in expressao:
    if digito == '(':
        pilha.append('(')
    elif digito == ')':
        if len(pilha) > 0:
            pilha.pop()
        else:
            pilha.append(')')
print('\033[1;35m-=\033[m' * 30)
if len(pilha) == 0:
    print('\033[1;32mExpressão válida !!!')
else:
    print('\033[1;31mExpressão inválida !!!')
print('\033[1;35m-=\033[m' * 30)
