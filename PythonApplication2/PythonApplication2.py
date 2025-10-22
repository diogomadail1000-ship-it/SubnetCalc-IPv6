import tkinter as tk
from tkinter import ttk, messagebox
import ipaddress

def calcular():
    cidr = entrada.get().strip()
    if not cidr:
        messagebox.showwarning("Aviso", "Introduz uma rede em formato CIDR (ex.: 192.168.1.0/24 ou 2001:db8::/64)")
        return

    try:
        rede = ipaddress.ip_network(cidr, strict=False)
    except ValueError:
        messagebox.showerror("Erro", "Endereço inválido! Usa formato CIDR, ex.: 192.168.1.0/24 ou 2001:db8::/64")
        return

    # --- IPv4 ---
    if isinstance(rede, ipaddress.IPv4Network):
        num_hosts = rede.num_addresses - 2 if rede.prefixlen <= 30 else rede.num_addresses
        primeiro = list(rede.hosts())[0] if num_hosts > 0 else "N/A"
        ultimo = list(rede.hosts())[-1] if num_hosts > 0 else "N/A"
        wildcard = ipaddress.IPv4Address(0xFFFFFFFF ^ int(rede.netmask))

        resultado = f"""
📡 Resultados IPv4

➡ Endereço de Rede   : {rede.network_address}
➡ Máscara de Sub-rede: {rede.netmask}
➡ Wildcard (ACL)     : {wildcard}
➡ Broadcast          : {rede.broadcast_address}
➡ Número de Hosts    : {num_hosts:,}
➡ Primeiro Host      : {primeiro}
➡ Último Host        : {ultimo}
➡ Prefixo CIDR       : /{rede.prefixlen}
➡ Privada            : {"Sim" if rede.is_private else "Não"}
"""
    # --- IPv6 ---
    else:
        resultado = f"""
🌐 Resultados IPv6

➡ Endereço de Rede   : {rede.network_address}
➡ Prefixo CIDR       : /{rede.prefixlen}
➡ Tamanho do Bloco   : {rede.num_addresses:,} endereços
➡ Tipo de Endereço   : {"Privado" if rede.is_private else "Público"}
➡ Rede Global?       : {"Sim" if rede.is_global else "Não"}
➡ Multicast?         : {"Sim" if rede.is_multicast else "Não"}
➡ Loopback?          : {"Sim" if rede.is_loopback else "Não"}
➡ Versão             : IPv6
"""

    texto_resultado.config(state="normal")
    texto_resultado.delete(1.0, tk.END)
    texto_resultado.insert(tk.END, resultado.strip())
    texto_resultado.config(state="disabled")

def limpar():
    entrada.delete(0, tk.END)
    texto_resultado.config(state="normal")
    texto_resultado.delete(1.0, tk.END)
    texto_resultado.config(state="disabled")

# ===== Interface Moderna =====
janela = tk.Tk()
janela.title("Calculadora de Sub-redes IPv4/IPv6")
janela.geometry("640x560")
janela.configure(bg="#0f111a")
janela.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton",
                font=("Segoe UI", 11, "bold"),
                padding=10,
                borderwidth=0,
                background="#0078D7",
                foreground="white")
style.map("TButton",
          background=[("active", "#0b5cff"), ("pressed", "#004aad")])
style.configure("TEntry", fieldbackground="#1b1f2a", foreground="white")
style.configure("TLabel", background="#0f111a", foreground="white")

# ===== Cabeçalho =====
titulo = tk.Label(
    janela,
    text="🌐 Calculadora de Sub-redes IPv4 / IPv6",
    font=("Segoe UI", 20, "bold"),
    fg="#00aaff",
    bg="#0f111a"
)
titulo.pack(pady=(30, 5))

subtitulo = tk.Label(
    janela,
    text="Insere uma rede (ex.: 192.168.1.0/24 ou 2001:db8::/64)",
    font=("Segoe UI", 11),
    fg="#a0a0a0",
    bg="#0f111a"
)
subtitulo.pack()

# ===== Entrada =====
frame_input = tk.Frame(janela, bg="#0f111a")
frame_input.pack(pady=15)

entrada = ttk.Entry(frame_input, font=("Consolas", 14), width=35)
entrada.grid(row=0, column=0, padx=10)
entrada.insert(0, "192.168.1.0/24")

# ===== Botões =====
frame_botoes = tk.Frame(janela, bg="#0f111a")
frame_botoes.pack(pady=10)

btn_calcular = ttk.Button(frame_botoes, text="Calcular", command=calcular)
btn_calcular.grid(row=0, column=0, padx=10)

btn_limpar = ttk.Button(frame_botoes, text="Limpar", command=limpar)
btn_limpar.grid(row=0, column=1, padx=10)

# ===== Caixa de resultados =====
texto_resultado = tk.Text(
    janela,
    height=18,
    width=75,
    font=("Consolas", 11),
    bg="#141823",
    fg="#e8e8e8",
    relief="flat",
    wrap="word",
    insertbackground="white",
)
texto_resultado.pack(pady=10)
texto_resultado.config(state="disabled")

rodape = tk.Label(
    janela,
    text="Feito com ❤️ em Python + Tkinter • Suporte IPv4 e IPv6",
    font=("Segoe UI", 9),
    fg="#666",
    bg="#0f111a"
)
rodape.pack(side="bottom", pady=5)

janela.mainloop()