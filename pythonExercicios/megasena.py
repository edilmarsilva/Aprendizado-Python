import customtkinter as ctk
from tkinter import messagebox
from random import sample

# Aparência
ctk.set_appearance_mode("dark")      # dark, light ou system
ctk.set_default_color_theme("blue")  # blue, green, dark-blue


def gerar():
    try:
        quantidade = int(entry.get())

        if quantidade <= 0:
            messagebox.showerror("Erro", "Digite um número maior que zero.")
            return

        textbox.configure(state="normal")
        textbox.delete("1.0", "end")

        for i in range(quantidade):
            jogo = sorted(sample(range(1, 61), 6))

            numeros = "  ".join(f"{n:02d}" for n in jogo)

            textbox.insert(
                "end",
                f"🎲 Jogo {i+1:02d}   ➜   {numeros}\n\n"
            )

        textbox.insert("end", "\n🍀 Boa sorte! 🍀")
        textbox.configure(state="disabled")

    except ValueError:
        messagebox.showerror("Erro", "Digite apenas números.")


def copiar():
    texto = textbox.get("1.0", "end")
    app.clipboard_clear()
    app.clipboard_append(texto)
    messagebox.showinfo("Copiado", "Os jogos foram copiados para a área de transferência.")


# ==========================
# Janela
# ==========================

app = ctk.CTk()
app.title("Mega-Sena Premium")
app.geometry("700x650")
app.resizable(False, False)

titulo = ctk.CTkLabel(
    app,
    text="🎰 GERADOR DE PALPITES DA MEGA-SENA",
    font=("Segoe UI", 24, "bold")
)
titulo.pack(pady=(20, 10))

subtitulo = ctk.CTkLabel(
    app,
    text="Escolha quantos jogos deseja gerar",
    font=("Segoe UI", 15)
)
subtitulo.pack()

entry = ctk.CTkEntry(
    app,
    width=220,
    height=40,
    justify="center",
    font=("Segoe UI", 18),
    placeholder_text="Ex: 10"
)
entry.pack(pady=20)

btn = ctk.CTkButton(
    app,
    text="🎲 Gerar Jogos",
    width=220,
    height=45,
    font=("Segoe UI", 16, "bold"),
    command=gerar
)
btn.pack()

textbox = ctk.CTkTextbox(
    app,
    width=620,
    height=360,
    font=("Consolas", 16)
)
textbox.pack(pady=25)

copiar_btn = ctk.CTkButton(
    app,
    text="📋 Copiar Jogos",
    width=220,
    height=40,
    command=copiar
)
copiar_btn.pack()

rodape = ctk.CTkLabel(
    app,
    text="Desenvolvido em Python",
    font=("Segoe UI", 12)
)
rodape.pack(pady=15)

app.mainloop()