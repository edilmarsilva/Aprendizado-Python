def leiaFloat(msg):
    valido = False
    while not valido:
        entrada = str(input(msg)).replace(',', '.').strip()
        if entrada.isalpha() or entrada == '':
            print(f'\033[0;31mERRO! \"{entrada}\" é uma medida inválida.\033[m')
        else:
            valido = True
            return float(entrada)


def leiaint(msg):
    ok = False
    valor = 0
    while True:
        num = str(input(msg))
        if num.isnumeric():
            valor = int(num)
            ok = True
        else:
            print('\033[1;31mERRO! Digite um número inteiro válido.\033[m')
        if ok:
            break
    return valor


parada = []
print('\033[36m-*\033[m' * 18)
print(f'\033[1;34m            DADOS DO FRETE')
print('\033[36m-*\033[m' * 18)

placa1 = str(input('\033[1;35mPLACA CARRETA: '))

placa2 = str(input('\033[1;35mPLACA CAVALO: '))

rota = leiaint('\033[1;35mQUANTAS PARADAS: ')
for c in range(1, rota + 1):
    parada.append(str(input(f'\033[1;34mDigite a {c}ª PARADA: ')))

conferente = str(input('\033[1;35mCONFERENTE / ARRUMADOR: '))

motorista = str(input('\033[1;35mMOTORISTA: '))

print('\033[1;33m[1] JURÍDICO: ')
print('\033[1;33m[2] FISÍCO: ')
while True:
    escolha = leiaint('\033[1mESCOLHA UMA OPÇÃO: ')
    if escolha < 1 or escolha > 2:
        print('\033[31mOPÇÃO INVÁLIDA\033[m')
    else:
        break

fone = str(input('\033[1;35mTELEFONE: '))

km = leiaFloat('\033[1;35mQUILOMENTRAGEM RODADA: ')

valorkm = leiaFloat('\033[1;35mPREÇO POR km: R$ ')

desgarga = leiaFloat('\033[1;35mBONUS DE DESGARGA: R$ ')


print('\033[35m-*\033[m' * 28)
print(f'\033[1;34m               INTINERÁRIO DE FRETE')
print('\033[35m-*\033[m' * 28)
print(f'\033[1m{"PLACA CARRETA":_<40} {placa1:>15}')
print(f'{"PLACA CAVALO":_<40} {placa2:>15}')
print(f'{"PARADAS":_<40} {rota:>15}')
print(f'PARADAS {parada}')
print(f'{"CONFERENTE / ARRUMADOR":_<40} {conferente:>15}')
print(f'{"MOTORISTA":_<40} {motorista:>15}')
frete = valorkm * km + desgarga
if escolha == 2:
    inss = float(frete) * (7 / 100)
    print(f'{"JURÍDICO / FÍSICA":_<40} R$ {inss:>15.2f}')
else:
    inss = 0
    print(f'{"JURÍDICO / FÍSICA":_<40} R$ {inss:>15.2f}')
print(f'{"TELEFONE":_<40} {fone:>15}')
print(f'{"FRETE":_<40} R$ {frete:>15.2f}')
adiantamento = (valorkm * km + desgarga) * (70 / 100)
print(f'{"ADIANTAMENTO":_<40} R$ {adiantamento:>15.2f}')
taxa_por_entrega = 80 * rota
print(f'{"TAXA POR ENTREGAS":_<40} R$ {taxa_por_entrega:>15.2f}')
tot_frete = frete + taxa_por_entrega - inss
print(f'{"TOTAL DO FRETE":_<40} R$ {tot_frete:>15.2f}')
saldo = frete + taxa_por_entrega - inss - adiantamento
print(f'{"SALDO":_<40} R$ {saldo:>15.2f}')
print('\033[35m-*\033[m' * 28)
