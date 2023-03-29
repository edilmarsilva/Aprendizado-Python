"""Desenvolva uma lógica que leia o peso e a altura de uma pessoa,
calcule o seu Índice de Massa Corporal (IMC) e mostre seu status,
conforme a tabela abaixo:
–IMC abaixo de 18,5: Abaixo do Peso
–Entre 18,5 e 25: Peso Ideal
–25 até 30: Sobrepeso
–30 até 40: Obesidade
–Acima de 40: Obesidade Mórbida"""
print('\033[36m-=' * 20)
print('\033[31m       CALCULADORA DE IMC')
print('\033[36m-=' * 20)
peso = float(input('\033[1;34mDigite o seu peso em Kg.: '))
altura = float(input('Digite a sua altura: '))
print('\033[36m=\033[m' * 50)
imc = peso / (altura * altura)
print('\033[35mSeu IMC é de {:.2f}'.format(imc))
if imc <= 18.5:
    print('\033[31mVocê está ABAIXO DO PESO!!!')
elif 18.5 < imc < 25:
    print('\032[35mVocê está no seu PESO IDEAL!!!')
elif 25 <= imc < 30:
    print('\033[33mVocê está com SOBREPESO!!!')
elif 30 <= imc < 40:
    print('\033[31mCUIDADO !!! Você está com OBESIDADE !!!')
elif imc >= 40:
    print('\033[30;41mPROCURE UM MÉDIDO !!! Você está com OBESIDADE MÓRBIDA!!!\033[m')
print('\033[36m=\033[m' * 50)
