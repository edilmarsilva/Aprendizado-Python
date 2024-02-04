i = int(input('Digite o ínicio: '))
f = int(input('Digite o fim: '))
p = int(input('Digite o passo: '))
for c in range(i, f + 1, p):
    print(f'{c}', end=' - ')