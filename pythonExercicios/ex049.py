print('\033[36m-=' * 20)
print('\033[31m         TABUADA 2.0')
print('\033[36m-=' * 20)
num = int(input('\033[1;34mQuer ver a tabuada de qual numero: '))
print('\033[36m=\033[m' * 15)
for c in range(1, 11):
    print('{} x {:2} = {:2}'.format(num, c, num * c))
print('\033[36m=\033[m' * 15)
