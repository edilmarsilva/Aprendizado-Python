"""
Índice de Massa Corporal
Desenvolva uma lógica que leia o peso e a altura de uma pessoa,
calcule o seu Índice de Massa Corporal (IMC)
e mostre o seu status, conforme a tabela abaixo:
– IMC abaixo de 18,5: Abaixo do Peso
– Entre 18,5 e 25: Peso Ideal
– 25 até 30: Sobrepeso
– 30 até 40: Obesidade
– Acima de 40: Obesidade Mórbida
"""

print('\033[1;33m-=' * 20)
print(f'\033[1;34m{"Índice de Massa Corporal":^40}')
print('\033[1;33m-=\033[m' * 20)

peso = float(input('Informe seu peso em kg: '))
altura = float(input('Informe sua altura em metros (m): '))
imc = peso / (altura ** 2)
ideal = 21.75 * (altura ** 2)

print('\033[36m=\033[m' * 50)
if imc < 18.5:
    print(f'Você está ABAIXO DO PESO. Seu IMC é de {imc:.1f}')
    print(f'Seu peso ideal é {ideal:.1f} kg Precisa ganhar mais {ideal - peso:.1f} kg')
elif 18.5 <= imc < 25:
    print(f'Você está no seu PESO IDEAL. Seu IMC é de {imc:.1f}')
elif 25 <= imc < 30:
    print(f'Você está com SOBREPESO. Seu IMC é de {imc:.1f}')
    print(f'Seu peso ideal é {ideal:.1f} kg Precisa emagrecer {peso - ideal:.1f} kg')
elif 30 <= imc < 40:
    print(f'Você está com OBESIDADE. Seu IMC é de {imc:.1f}')
    print(f'Seu peso ideal é {ideal:.1f} kg Precisa emagrecer {peso - ideal:.1f} kg')
elif imc >= 40:
    print(f'Você está com OBESIDADE MÓRBIDA! Procure um médico. Seu IMC é de {imc:.1f}')
    print(f'Seu peso ideal é {ideal:.1f} kg Precisa emagrecer {peso - ideal:.1f} kg')
print('\033[36m=\033[m' * 50)
