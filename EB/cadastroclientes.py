import mysql.connector

#################################################################################################
# CONECTANDO COM O SERVIDOR MySQL
#################################################################################################
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='embraco',
)
cursor = conexao.cursor()

#################################################################################################
######################          INCLUINDO CLIENTE           #####################################
#################################################################################################


cnpj = str(input('CNPJ: ')).replace('.', '').replace('/', '').replace('-', '')
razao = str(input('RAZÃO SOCIAL: ')).strip()
endereco = str(input('ENDEREÇO: ')).strip()
numero = int(input('NÚMERO: '))
bairro = str(input('BAIRRO: ')).strip()
codmun = int(input('CODIGO IBGE MUNICIPIO: '))
cidade = str(input('CIDADE: '))
uf = str(input('UF: '))
cep = str(input('CEP: ')).replace('-', '').strip()
telefone = str(input('TELEFONE: ')).replace('(', '').replace(')', '').replace('-', '')
ie = str(input('INSCRICAO ESTADUAL: '))
obs = str(input('OBSERVAÇÃO: '))

comando = f'insert into cadastrocliente values (default, "{cnpj}", "{razao}", "{endereco}", {numero}, "{bairro}",\n' \
          f' {codmun}, "{cidade}", "{uf}", "{cep}", "{telefone}", "{ie}", "{obs}")'

cursor.execute(comando)
conexao.commit()

cursor.close()
conexao.close()
