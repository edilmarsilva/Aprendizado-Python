""""Desenvolva um programa que leia o primeiro termo e a razão de uma PA. No final,
mostre os 10 primeiros termos dessa progressão."""
print('\033[36m-=' * 20)
print('\033[31m      10 TERMOS DE UMA PA')
print('\033[36m-=' * 20)
termo = int(input('\033[1;34mPrimeiro termo: '))
razao = int(input('Razão: '))
dec = termo + (10 - 1) * razao
print('\033[36m=\033[m' * 55)
for c in range(termo, dec + razao, razao):
    print(c, end=' → ')
print('ACABOU')
print('\033[36m=\033[m' * 55)
