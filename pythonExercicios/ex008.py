"""Escreva um programa que leia um valor em metros e o exiba convertido em centímetros e milímetros."""
print('\033[36m-=' * 20)
print('\033[31m         CONVERTENDO MEDIDAS')
print('\033[36m-=' * 20)
m = float(input('Digite a medida em metros: '))
mmm = m*1000
mcm = m*100
mdm = m*10
mdam = m/10
mhm = m/100
mkm = m/1000
print('\033[30;41mA metragem digitada de {}m é {}mm, {}cm {}dm, {}dam, {}hm e {}km\033[m'.format(m, mmm, mcm, mdm, mdam, mhm, mkm))
