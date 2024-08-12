import pandas as pd

# Carregue os dados da planilha para um DataFrame
df = pd.read_csv('EB01080.xlsx', sep='\t')  # Altere 'planilha.csv' para o nome real do seu arquivo

# Agrupe por nota e some os valores
df_agrupado = df.groupby('NOTA')['VALOR'].sum().reset_index()

# Imprima o DataFrame agrupado
print(df_agrupado)
