from kivymd.app import MDApp
from kivymd.uix.label import MDLabel




def h11(medida):
    if 1 <= medida < 3:
        medida_final = medida - 0.06
        return medida_final
    if 3 <= medida < 6:
        medida_final = medida - 0.075
        return medida_final
    if 6 <= medida < 10:
        medida_final = medida - 0.09
        return medida_final
    if 10 <= medida < 18:
        medida_final = medida - 0.11
        return medida_final
    if 18 <= medida < 30:
        medida_final = medida - 0.13
        return medida_final
    if 30 <= medida < 50:
        medida_final = medida - 0.16
        return medida_final
    if 50 <= medida < 80:
        medida_final = medida - 0.19
        return medida_final
    if 80 <= medida < 120:
        medida_final = medida - 0.22
        return medida_final


def h10(medida):
    if 1 <= medida < 3:
        medida_final = medida - 0.04
        return medida_final
    if 3 <= medida < 6:
        medida_final = medida - 0.048
        return medida_final
    if 6 <= medida < 10:
        medida_final = medida - 0.058
        return medida_final
    if 10 <= medida < 18:
        medida_final = medida - 0.070
        return medida_final
    if 18 <= medida < 30:
        medida_final = medida - 0.084
        return medida_final
    if 30 <= medida < 50:
        medida_final = medida - 0.10
        return medida_final
    if 50 <= medida < 80:
        medida_final = medida - 0.12
        return medida_final
    if 80 <= medida < 120:
        medida_final = medida - 0.14
        return medida_final


def h9(medida):
    if 1 <= medida < 3:
        medida_final = medida - 0.025
        return medida_final
    if 3 <= medida < 6:
        medida_final = medida - 0.030
        return medida_final
    if 6 <= medida < 10:
        medida_final = medida - 0.036
        return medida_final
    if 10 <= medida < 18:
        medida_final = medida - 0.043
        return medida_final
    if 18 <= medida < 30:
        medida_final = medida - 0.052
        return medida_final
    if 30 <= medida < 50:
        medida_final = medida - 0.062
        return medida_final
    if 50 <= medida < 80:
        medida_final = medida - 0.074
        return medida_final
    if 80 <= medida < 120:
        medida_final = medida - 0.087
        return medida_final


def h8(medida):
    if 1 <= medida < 3:
        medida_final = medida - 0.014
        return medida_final
    if 3 <= medida < 6:
        medida_final = medida - 0.018
        return medida_final
    if 6 <= medida < 10:
        medida_final = medida - 0.022
        return medida_final
    if 10 <= medida < 18:
        medida_final = medida - 0.027
        return medida_final
    if 18 <= medida < 30:
        medida_final = medida - 0.033
        return medida_final
    if 30 <= medida < 50:
        medida_final = medida - 0.039
        return medida_final
    if 50 <= medida < 80:
        medida_final = medida - 0.046
        return medida_final
    if 80 <= medida < 120:
        medida_final = medida - 0.054
        return medida_final


def h7(medida):
    if 1 <= medida < 3:
        medida_final = medida - 0.010
        return medida_final
    if 3 <= medida < 6:
        medida_final = medida - 0.012
        return medida_final
    if 6 <= medida < 10:
        medida_final = medida - 0.015
        return medida_final
    if 10 <= medida < 18:
        medida_final = medida - 0.018
        return medida_final
    if 18 <= medida < 30:
        medida_final = medida - 0.021
        return medida_final
    if 30 <= medida < 50:
        medida_final = medida - 0.025
        return medida_final
    if 50 <= medida < 80:
        medida_final = medida - 0.030
        return medida_final
    if 80 <= medida < 120:
        medida_final = medida - 0.035
        return medida_final


def titulo(txt):
    print('\033[35m-*\033[m' * 25)
    print(f'\033[1;34m{txt:^50}')
    print('\033[35m-*\033[m' * 25)


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


def leiaFloat(msg):
    valido = False
    while not valido:
        entrada = str(input(msg)).replace(',', '.').strip()
        if entrada.isalpha() or entrada == '':
            print(f'\033[0;31mERRO! \"{entrada}\" é uma medida inválida.\033[m')
        else:
            valido = True
            return float(entrada)


#Programa Principal
class MainApp(MDApp):
    def build(self):
        return MDLabel(text="Hello, World", halign="center")


MainApp().run()



resp = 'S'
while True:
    titulo('TOLERÂNCIA DE MEDIDAS v1')
    if resp == 'S':
        while True:
            bitola = leiaFloat('\033[1mDIGITE A MEDIDA FINAL: ')
            if bitola < 1 or bitola > 120:
                print('\033[31mNÃO TRABALHAMOS COM ESSA MEDIDA\033[m')
            else:
                break
        print('''\033[33m 
[1] h11
[2] h10
[3]  h9
[4]  h8
[5]  h7\033[m''')
        while True:
            escolha = leiaint('\033[1mQUAL A TOLERÂNCIA: ')
            if escolha < 1 or escolha > 5:
                print('\033[31mOPÇÃO INVÁLIDA\033[m')
            else:
                break

        if escolha == 1:
            mf = h11(bitola)
            print('\033[35m-*\033[m' * 30)
            print(f'\033[1;34mA medida final para bitola {bitola:.2f} h11 é de {mf:.3f} à {bitola:.3f}\033[m')
            print('\033[35m-*\033[m' * 30)

        elif escolha == 2:
            mf = h10(bitola)
            print('\033[35m-*\033[m' * 30)
            print(f'\033[1;34mA medida final para bitola {bitola:.2f} h10 é de {mf:.3f} à {bitola:.3f}\033[m')
            print('\033[35m-*\033[m' * 30)

        elif escolha == 3:
            mf = h9(bitola)
            print('\033[35m-*\033[m' * 30)
            print(f'\033[1;34mA medida final para bitola {bitola:.2f} h9 é de {mf:.3f} à {bitola:.3f}\033[m')
            print('\033[35m-*\033[m' * 30)

        elif escolha == 4:
            mf = h8(bitola)
            print('\033[35m-*\033[m' * 30)
            print(f'\033[1;34mA medida final para bitola {bitola:.2f} h8 é de {mf:.3f} à {bitola:.3f}\033[m')
            print('\033[35m-*\033[m' * 30)

        elif escolha == 5:
            mf = h7(bitola)
            print('\033[35m-*\033[m' * 30)
            print(f'\033[1;34mA medida final para bitola {bitola:.2f} h7 é de {mf:.3f} à {bitola:.3f}\033[m')
            print('\033[35m-*\033[m' * 30)

    resp = str(input('\033[7;40mQuer continuar? [S/N] \033[m')).strip().upper()[0]
    if resp == 'N':
        print('\033[1m***ENCERRANDO O SISTEMA TOLERÂNCIA v1***')
        break
