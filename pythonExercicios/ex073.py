"""Crie uma tupla preenchida com os 20 primeiros colocados
da Tabela do Campeonato Brasileiro de Futebol,
na ordem de colocação. Depois mostre:
a) Os 5 primeiros times.

b) Os últimos 4 colocados.

c) Times em ordem alfabética.

d) Em que posição está o time da Chapecoense."""
print('\033[35m-*\033[m' * 25)
print('\033[1;33m{:-^50}'.format('Tuplas com Times de Futebol'))
print('\033[35m-*\033[m' * 25)
tabela = 'Corinthians', 'Palmeiras', 'Santos', 'Grêmio', 'Cruzeiro', \
         'Flamengo', 'Vasco da Gama', 'Chapecoense', 'Atlético - MG', \
         'Botafogo', 'Athletico -PR', 'Bahia', 'São Paulo', \
         'Fluminense', 'Sport Recife', 'EC Vitória', 'Coritiba', \
         'Avaí', 'Ponte Preta', 'Atlético - GO'
print('\033[35m-=\033[m' * 25)
print(f'\033[1mLista de times do BRASILEIRÃO: {tabela}')
print('\033[35m-=\033[m' * 25)
print(f'\033[1mOs 5 primeiros são: {tabela[0:5]}')
print('\033[35m-=\033[m' * 25)
print(f'\033[1mOs 4 últimos são: {tabela[-4:]}')
print('\033[35m-=\033[m' * 25)
print(f'\033[1mTimes em ordem alfabética: {sorted(tabela)}')
print('\033[35m-=\033[m' * 25)
for pos, time in enumerate(tabela):
    if time == 'Chapecoense':
        print(f'\033[1mA Chapecoense está na {pos + 1}ªposição.')
print('\033[1;35m{:-^50}'.format('FIM DA CLASSIFICAÇÃO'))
