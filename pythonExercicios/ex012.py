"""Faça um algoritmo que leia o preço de um produto e mostre o seu novo preço, com 5% de desconto."""
print('\033[36m-=' * 20)
print('\033[31m         CONCEDENDO DESCONTO')
print('\033[36m-=' * 20)
prec = float(input('\033[1;34mQual o preço da mercadoria R$\033[m '))
desc = prec * 5 / 100
nprec = prec - desc
print('\033[36m#\033[m'*90)
print('\033[1mComprando hoje você terá um desconto de 5% que é de R$ {:.2f} e pagará apenas R$ {:.2f} !!!\033[m'.format(desc, nprec))
print('\033[36m#\033[m'*90)
