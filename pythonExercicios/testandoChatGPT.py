#Classe cliente
class Cliente:
    def __init__(self, nome, sobrenome, idade):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade

#Lista de clientes
clientes = []

#Função para cadastrar um novo cliente
def cadastrar_cliente():
    nome = input("Insira o nome do cliente: ")
    sobrenome = input("Insira o sobrenome do cliente: ")
    idade = input("Insira a idade do cliente: ")
    clientes.append(Cliente(nome, sobrenome, idade))
    print("Cliente cadastrado com sucesso!")

#Função para listar todos os clientes cadastrados
def listar_clientes():
    for i in range(len(clientes)):
        print(f"{i+1} - {clientes[i].nome} {clientes[i].sobrenome}, {clientes[i].idade} anos")

#Loop do programa
while True:
    opcao = input("Escolha uma opção: (C)adastrar, (L)istar, (S)air: ")
    if opcao.upper() == "C":
        cadastrar_cliente()
    elif opcao.upper() == "L":
        listar_clientes()
    elif opcao.upper() == "S":
        break
    else:
        print("Opção inválida.")
