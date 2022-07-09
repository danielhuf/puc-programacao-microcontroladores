from tkinter import font
import pymongo as mg
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from py_irsend.irsend import send_once
from funcoes_executaveis import liga_canal

# -------------- VARIAVEIS GLOBAIS -----------------

preto = "gray15"
cinza = "#52595E"
neon = "#98F5FF"
font_default = "Terminal"

controle = None
tabela_canais = None
ctlRemoto = None
espaco_inputs = None

number_img = []
del_img = None
botoes_canal = []
buton_img2 = list()

sessao_esta_ativa = False
key_stream = ""

nome_controle = "aquario"

# ------------- FUNCOES AUXILIARES -------------------------


def createImage(file, x, y):
    img = tk.PhotoImage(file=file)
    return img


def criar_etiqueta(janela, texto, coluna, linha, padx=10, pady=0, colunas_ocupadas=1):
    etiqueta_canal = tk.Label(
        janela, text=texto, bg="grey15", fg="white", font="Terminal"
    )
    etiqueta_canal.grid(
        column=coluna,
        row=linha,
        sticky=tk.W,
        padx=padx,
        pady=pady,
        columnspan=colunas_ocupadas,
    )
    return etiqueta_canal


def criar_botao(janela, texto, coluna, linha, padx=10, pady=0, colunas_ocupadas=1, canal=None):
    etiqueta_canal = tk.Button(
        janela, text=texto, bg="#98F5FF", border=None, font="Terminal", command = lambda x=canal: liga_canal(x)
    )
    etiqueta_canal.grid(
        column=coluna,
        row=linha,
        sticky=tk.W,
        padx=padx,
        pady=pady,
        columnspan=colunas_ocupadas,
    )
    return etiqueta_canal


# ----------- TABELA DE CANAIS ------------------

def lista_canais():
    global canais
    listaC = []
    for i, canal in enumerate(canais.find()):
        listaC.append(canal)
    return listaC


def mostrar_canais():
    global tabela_canais
    global del_img
    global canais

    for i, canal in enumerate(canais.find()):
        botaoNome = criar_botao(
            tabela_canais, texto=canal["nome"], coluna=0, linha=i + 1, padx=10, pady=5, canal=canal["numero"]
        )
        etiqueta = criar_etiqueta(
            tabela_canais, texto=canal["numero"], coluna=1, linha=i + 1, padx=10, pady=5
        )

        botao = tk.Button(
            tabela_canais,
            image=del_img,
            bg="gray15",
            activebackground="gray15",
            highlightthickness=0,
            bd=0,
            activeforeground="#52595E",
            cursor="hand2",
            # command=apagar_canal
            command=lambda x=canal: apagar_canal(x["numero"]),
        )
        botao.grid(column=2, row=i + 1, sticky=tk.W, padx=10)
        botoes_canal.append(botaoNome)
        botoes_canal.append(etiqueta)
        botoes_canal.append(botao)


def apagar_canal(canal):
    print(canal)
    query = {"numero": canal}
    canais.delete_one(query)
    apagar_botoes()
    atualizar_tela()


def apagar_botoes():
    for botao in botoes_canal:
        botao.destroy()


def criar_tabela_canais():

    global del_img
    tabela_canais.place(x=320, y=135)

    del_img = createImage("Imagens/deletar.png", 12, 12)

    tabela_canais.columnconfigure(0, weight=1)
    tabela_canais.columnconfigure(1, weight=1)
    tabela_canais.columnconfigure(2, weight=1)
    tabela_canais.columnconfigure(3, weight=1)

    adicionar_inputs()
    global espaco_inputs

    botao1 = tk.Button(
        espaco_inputs,
        text="Salvar",
        command=salvar_canal,
        font="Terminal",
        width=10,
        bg="#98F5FF",
        border=None,
    )
    # botao1.grid(column=3, row=3, sticky=W, padx=10, pady=0)

    botao1.grid(column=1, row=3, sticky=tk.W, padx=20, pady=10)

    mostrar_canais()


def canal_valido(nome, numero):

    vazio = nome == "" or numero == ""
    tipo_incorreto = not numero.isnumeric() or nome.isnumeric()
    repetido = canais.find_one({"nome": nome}) is not None

    if vazio or tipo_incorreto or repetido:
        return False

    return True


# ----------------- INPUT DE NOVO CANAL --------------------


def atualizar_tela():
    adicionar_inputs()
    mostrar_canais()


def adicionar_inputs():
    global nomeCanal
    global numeroCanal
    global controle
    global espaco_inputs

    espaco_inputs.place(x=320, y=420)

    # --------------- Ajustar a localizacao ------------------

    # criar_etiqueta(janela, texto="Nome", coluna=2, linha=1)

    etiqueta_canal = tk.Label(
        espaco_inputs, text="Nome", bg="grey15", fg="white", font="Terminal"
    )
    etiqueta_canal.grid(column=0, row=0, sticky=tk.W, pady=2)

    nomeCanal = (
        tk.StringVar()
    )  # essa variável vai guardar o texto digitado pelo usuário
    campo_nome = tk.Entry(espaco_inputs, width=15, textvariable=nomeCanal)
    # campo_nome.grid(column=3, row=1, sticky=tk.W, padx=10, pady=0)
    campo_nome.grid(column=0, row=1, sticky=tk.W, pady=2)

    etiqueta_num = tk.Label(
        espaco_inputs, text="Número", bg="grey15", fg="white", font="Terminal"
    )
    etiqueta_num.grid(column=0, row=2, sticky=tk.W, pady=2)

    # criar_etiqueta(janela, texto="Número", coluna=2, linha=2)

    numeroCanal = (
        tk.StringVar()
    )  # essa variável vai guardar o texto digitado pelo usuário
    campo_nome = tk.Entry(espaco_inputs, width=15, textvariable=numeroCanal)
    # campo_nome.grid(column=3, row=2, sticky=tk.W, padx=10, pady=0)
    campo_nome.grid(column=0, row=3, sticky=tk.W, pady=2)

    # ------------------------------------------


def salvar_canal():
    global canais
    global tabela_canais
    nome = nomeCanal.get().strip().capitalize()
    numero = numeroCanal.get().strip()
    if canal_valido(nome, numero):
        novoCanal = {"nome": nome, "numero": numero}
        canais.insert_one(novoCanal)
        atualizar_tela()


# ----------------- CONTROLE REMOTO --------------------------


def criar_botoes():
    global ctlRemoto
    for i in range(15):
        buton_img2.append(
            tk.Button(
                ctlRemoto,
                image=number_img[i],
                bg=preto,
                activebackground=preto,
                highlightthickness=0,
                bd=0,
                activeforeground=cinza,
                cursor="hand2",
                command=lambda x=i: send_key(x),
            )
        )
    for j in range(15):
        linha = j // 3
        coluna = j % 3
        buton_img2[j].grid(column=coluna, row=linha, sticky=tk.W, padx=10, pady=10)


def criar_controle_remoto():
    ctlRemoto.place(x=85, y=135)

    for i in range(15):
        number_img.append(createImage("Imagens/" + str(i) + ".png", 40, 40))

    ctlRemoto.columnconfigure(0, weight=1)
    ctlRemoto.columnconfigure(1, weight=1)
    ctlRemoto.columnconfigure(2, weight=1)

    criar_botoes()


def send_key(key):
    #global key_stream
    
    if key < 10:
        tecla = "KEY_%s"%key
    elif key == 10:
        tecla = "KEY_POWER"
    elif key == 11:
        tecla = "KEY_MUTE"
    elif key == 12:
        tecla = "KEY_VOLUMEDOWN"
    elif key == 13:
        tecla = "KEY_VOLUMEUP"
    elif key == 14:
        tecla = "KEY_OK"
    
    send_once(nome_controle, [tecla])
    print(tecla)
    #if key == 14:
    #    print(f"chamou {key_stream}")
        
    #    key_stream = ""
    #else:
    #    key_stream += str(key)


# ------------- VALIDANDO A SESSAO ---------------


def iniciar_sessao(janela):
    global controle
    global tabela_canais
    global ctlRemoto
    global espaco_inputs
    global sessao_esta_ativa
    controle = janela
    sessao_esta_ativa = True
    tabela_canais = tk.Canvas(
        controle, width=270, height=400, background=preto, highlightthickness=0
    )
    ctlRemoto = tk.Canvas(
        controle, width=270, height=400, background=preto, highlightthickness=0
    )
    espaco_inputs = tk.Canvas(
        controle, width=270, height=400, background=preto, highlightthickness=0
    )

    criar_controle_remoto()
    criar_tabela_canais()


def destruir_elementos(widget):
    elementos = widget.winfo_children()
    for elemento in elementos:
        elemento.destroy()
    widget.destroy()


def reiniciar_variaveis():

    global controle
    global tabela_canais
    global ctlRemoto
    global espaco_inputs
    global number_img
    global del_img
    global botoes_canal
    global buton_img2
    global key_stream

    controle = None
    tabela_canais = None
    ctlRemoto = None
    espaco_inputs = None
    number_img = []
    del_img = None
    botoes_canal = []
    buton_img2 = list()
    key_stream = ""


def finalizar_sessao():
    global sessao_esta_ativa
    sessao_esta_ativa = False

    destruir_elementos(tabela_canais)
    destruir_elementos(ctlRemoto)
    destruir_elementos(espaco_inputs)

    reiniciar_variaveis()


# -------------------- BASE DE DADOS -------------------------------

cliente = mg.MongoClient("mongodb://localhost:27017/")
db = cliente["projetoFinal"]
canais = db["CANAIS"]
