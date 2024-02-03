import tkinter as tk

# Conversor de polegadas para milímetros

# Fator de conversão
CONVERSAO_FACTOR = 25.4


# Função para converter polegadas em milímetros
def converter_polegadas_em_milimetros():
    # Pega o valor em polegadas do usuário
    polegadas = float(entrada_polegadas.get())

    # Converte para milímetros
    milimetros = polegadas * CONVERSAO_FACTOR

    # Exibe o resultado
    resultado_label.config(text=f"{polegadas} polegadas é igual a {milimetros} milímetros.")


# Cria a janela principal
janela = tk.Tk()
janela.title("Conversor de Polegadas para Milímetros")

# Cria o rótulo e a entrada de dados para polegadas
rotulo_polegadas = tk.Label(janela, text="Insira o valor em polegadas:")
rotulo_polegadas.pack()

entrada_polegadas = tk.Entry(janela)
entrada_polegadas.pack()

# Cria o botão para iniciar a conversão
botao_converter = tk.Button(janela, text="Converter", command=converter_polegadas_em_milimetros)
botao_converter.pack()

# Cria o rótulo para exibir o resultado
resultado_label = tk.Label(janela, text="")
resultado_label.pack()

# Inicia o loop principal do Tkinter
janela.mainloop()
