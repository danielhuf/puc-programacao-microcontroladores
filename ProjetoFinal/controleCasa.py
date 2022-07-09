from tkinter import *
from datetime import datetime, timedelta
from time import *
from threading import Timer
from PIL import Image
from banco_componentes import *
from banco_triggers import *
from banco_horarios import *
from banco_ifttt import *
import canais_raspberry as cn
import comunicacao_spot as music
from remocoes import *

from funcoes_executaveis import *
eternidade.start()
inicializa_componentes() #Raspberry
cria_fixos()

#======================== Inicialização de variáveis =======================
preto = "gray15"
cinza = "#52595E"
neon = "#98F5FF"
font_default = "Terminal"

global timer, timer2, indice, indice2, shownGadgets, shownOptions, triggers_input_mn, triggers_output_mn, componentes
global cadastrados1, cadastrados2, cadastrados_var1, cadastrados_var2, portas_se_mn, portas_entao_mn, bd1_input_mn
global luzes_mn, luzes_var, tipo1, tipo2, todos_cadastrados_var, l_inputs_ativos, inputs_ativos_var, remove_triggers_mn
global portas_ativo_mn
timer = None
timer2 = None
triggers_input_mn = None
triggers_output_mn = None
portas_se_mn = None
portas_entao_mn = None
luzes_mn = None
luzes_var = None
bd1_input_mn = None
todos_cadastrados_var = None
inputs_ativos = None
remove_triggers_mn = None
portas_ativo_mn = None
tipo1 = tipo2 = None;

dic_menu_buttons = {}
dic_tv_itens = {}
dic_luzes_itens = {}
dic_musica_itens = {}
dic_alarmes_itens = {}
dic_portas_itens = {}
dic_bd_itens = {}
dic_triggers_itens = {}
dic_modos_itens = {}

cadastrados1 = []
cadastrados2 = []

def busca_componentes():
    global cadastrados1, cadastrados2, componentes
    componentes = busca_componentes_ativos()
    
    cadastrados1 = []
    cadastrados2 = []
    
    for comp in componentes:
        if comp["input"]:
            cadastrados1.append(comp["nome"])
        else:
            cadastrados2.append(comp["nome"])

busca_componentes()
controle = Tk()  #criacao da janela

# ========================= Definição de funções ========================

# Cria um botão genérico
def createButton(text, image, func, font_size):
    btn = Button(controle, text=text, image = image, bg=preto, activebackground=preto, highlightthickness = 0, bd=0, compound="left", fg=neon, activeforeground=cinza, font=(font_default, font_size), command = func, cursor="hand2")
    return btn


# Cria uma imagem genérica
def createImage(file, x, y):
    img = PhotoImage(file = file)
    return img


# Mostra os gadgets
def showGadgets():
    global shownGadgets
    
    if (shownGadgets):
        tv_btn.place_forget()
        light_btn.place_forget()
        music_btn.place_forget()
        alarm_btn.place_forget()
    else:
        tv_btn.place(x=65, y=220)
        light_btn.place(x=200, y=250)
        music_btn.place(x=250, y=360)
        alarm_btn.place(x=220, y=470)
        
    shownGadgets = not shownGadgets
    
    
# Mostra as opções de configuração
def showOptions():
    global shownOptions
    
    if (shownOptions):
        ports_btn.place_forget()
        database_btn.place_forget()
        automation_btn.place_forget()
        mode_btn.place_forget()
    else:
        ports_btn.place(x=460, y=280)
        database_btn.place(x=494, y=330)
        automation_btn.place(x=473, y=390)
        mode_btn.place(x=493, y=440)
        
    shownOptions = not shownOptions


def esquece(widget):
    if widget != None:
        widget.place_forget()
   
   
# Mostra o menu inicial do controle da casa
def mostraMenuInicial():
    global indice, indice2, shownGadgets, shownOptions, triggers_input_mn, triggers_output_mn
    
    shownGadgets = False
    shownOptions = True
    
    showOptions()
    voltar_btn.place_forget()
    
    if cn.sessao_esta_ativa:
        cn.finalizar_sessao()
    
    if music.is_session_active:
        music.leave_music()
    
    for dic in [dic_tv_itens, dic_luzes_itens, dic_musica_itens, dic_alarmes_itens, dic_portas_itens, dic_bd_itens, dic_triggers_itens, dic_modos_itens]:
        for item, cord in dic.items():
            item.place_forget()
    
    esquece(triggers_input_mn)
    esquece(triggers_output_mn)
    esquece(luzes_mn)
    esquece(bd1_input_mn)
    esquece(remove_triggers_mn)
    
    for btn, cord in dic_menu_buttons.items():
        btn.place(x=cord[0], y=cord[1])
        
    indice = 0
    indice2 = 0
    timer_recorrente(1)
    timer_recorrente(2)
    
    
# Esconde o menu inicial do controle da casa
def escondeMenuInicial():
    for btn in [time_lbl, status_lbl, hour_lbl, menu_btn, tv_btn, light_btn, music_btn, alarm_btn]:
        btn.place_forget()
        
    for btn, cord in dic_menu_buttons.items():
        btn.place_forget()
        
    voltar_btn.place(x=670, y=40)
    
    
# Timer recorrente utilizado para rolar a mensagem de boas-vindas
def timer_recorrente(arg):
    global timer, timer2, indice, indice2
    
    if arg == 1:
        txt = time_msg[:indice]
        time_lbl.configure(text=txt)
        indice += 1
    
        if txt == time_msg:
            parar_timer(1)
            
        else:
            timer = Timer(0.05, timer_recorrente, [1])
            timer.start()
            
    elif arg == 2:
        txt = status_txt[:indice2]
        status_lbl.configure(text=txt)
        indice2 += 1
        
        if txt == status_txt:
            parar_timer(2)
        else:
            timer2 = Timer(0.05, timer_recorrente, [2])
            timer2.start()
            
            
# Interrompe o timer recorrente
def parar_timer(arg):
    global timer, timer2
    
    if arg == 1:
        if timer != None:
            timer.cancel()
            timer = None
            
    elif arg == 2:
        if timer2 != None:
            timer2.cancel()
            timer2 = None
        
        
# Abre tela de seleção das portas       
def abreMenuPortas():
    global shownOptions
    
    escondeMenuInicial()
    shownOptions = True
    showOptions()
    
    for item, cord in dic_portas_itens.items():
        item.place(x=cord[0], y=cord[1])
        
    components_var.set(components[0]) # default value
    ports_var.set(ports[0])
    input_ap.delete(1.0,"end")
    input_ap.insert(1.0, "")
    

# Abre tela para consulta e seleção dos componentes e triggers cadastrados no BD
def abreMenuBD():
    global shownOptions, bd1_input_mn, todos_cadastrados_var, l_inputs_ativos, inputs_ativos_var, remove_triggers_mn
    
    escondeMenuInicial()
    shownOptions = True
    showOptions()
    
    for item, cord in dic_bd_itens.items():
        item.place(x=cord[0], y=cord[1])
    
    esquece(bd1_input_mn)
    esquece(remove_triggers_mn)
    esquece(portas_ativo_mn)
    
    l_todos_componentes = []
    todos_componentes = busca_removiveis()
    for comp in todos_componentes:
        l_todos_componentes.append(comp["nome"])

    if l_todos_componentes != []:
        todos_cadastrados_var = StringVar(controle)
        todos_cadastrados_var.set("")
        
        bd1_input_mn = OptionMenu(controle, todos_cadastrados_var, *l_todos_componentes)
        bd1_input_mn.config(bg="white", activebackground=neon, font=(font_default, 16))
        bd1_input_mn["menu"].config(bg="white", activebackground=neon, font=(font_default, 16))
        bd1_input_mn.place(x=40, y=160)
        
    else:
        todos_cadastrados_var = None
        
    l_inputs_ativos = []
    todos_inputs = comp_nao_vazios()
    for input1 in todos_inputs:
        l_inputs_ativos.append(input1["nome"])
    
    if l_inputs_ativos != []:
        inputs_ativos_var = StringVar(controle)
        inputs_ativos_var.set("")
        trigger_var.set('')
        
        remove_triggers_mn = OptionMenu(controle, inputs_ativos_var, *l_inputs_ativos, command=atualiza_ativo)
        remove_triggers_mn.config(bg="white", activebackground=neon, font=(font_default, 16))
        remove_triggers_mn["menu"].config(bg="white", activebackground=neon, font=(font_default, 16))
        remove_triggers_mn.place(x=400, y=160)
    
    
# Abre tela para criar automação  
def abreMenuTriggers():
    global shownOptions, triggers_input_mn, triggers_output_mn, cadastrados1, cadastrados2, cadastrados_var1, cadastrados_var2
    
    escondeMenuInicial()
    shownOptions = True
    showOptions()
    
    for item, cord in dic_triggers_itens.items():
        item.place(x=cord[0], y=cord[1])
        
    busca_componentes()
    if cadastrados1 != []:
        cadastrados_var1 = StringVar(controle)
        cadastrados_var1.set('')
        se_var.set('')
        
        triggers_input_mn = OptionMenu(controle, cadastrados_var1, *cadastrados1, command=atualiza_se)
        triggers_input_mn.config(bg="white", activebackground=neon, font=(font_default, 20))
        triggers_input_mn["menu"].config(bg="white", activebackground=neon, font=(font_default, 20))
        triggers_input_mn.place(x=40, y=160)
        
    if cadastrados2 != []:
        cadastrados_var2 = StringVar(controle)
        cadastrados_var2.set('')
        entao_var.set('')
        
        triggers_output_mn = OptionMenu(controle, cadastrados_var2, *cadastrados2, command=atualiza_entao)
        triggers_output_mn.config(bg="white", activebackground=neon, font=(font_default, 20))
        triggers_output_mn["menu"].config(bg="white", activebackground=neon, font=(font_default, 20))
        triggers_output_mn.place(x=400, y=160)

# Atualiza o input do trigger conforme o tipo de componente escolhido
def atualiza_se(nome):
    global portas_se_mn, tipo1
    esquece(portas_se_mn)
    
    id_comp = busca_id(nome)
    comp = busca_componente(id_comp)
    tipo1 = comp["tipo"]

    if tipo1 == "botao":
        se = ["Botão pressionado", "Botão solto"]
    
    elif tipo1 == "sensor_luz":
        se = ["Luz detectada", "Escuridão detectada"]
        
    elif tipo1 == "sensor_movimento":
        se = ["Movimento detectado", "Inércia detectada"]
        
    elif tipo1 == "data":
        tipo1 = comp["nome"]
        if comp["nome"] == "Data periódica":
            semanais = busca_semanais()
            se = []
            for semanal in semanais:
                se.append(semanal["nome"])
                
        else:
            especificos = busca_especificos()
            se = []
            for especifico in especificos:
                se.append(especifico["nome"])
        if len(se) == 0:
            se.append("")
        
    portas_se_mn = OptionMenu(controle, se_var, *se)
    portas_se_mn.config(bg="white", activebackground=neon, font=(font_default, 20))
    portas_se_mn["menu"].config(bg="white", activebackground=neon, font=(font_default, 20))
    dic_triggers_itens[portas_se_mn] = [40, 280]
    portas_se_mn.place(x=40, y=280)
    se_var.set(se[0])
    
# Atualiza o trigger conforme o tipo de componente escolhido
def atualiza_entao(nome):
    global portas_entao_mn, tipo2
    esquece(portas_entao_mn)
    
    id_comp = busca_id(nome)
    comp = busca_componente(id_comp)
    tipo2 = comp["tipo"]
    
    if tipo2 == "LED":
        entao = ["LED aceso", "LED desligado", "LED altera"]
        
    elif tipo2 == "campainha":
        entao = ["Tocar campainha", "Campainha para", "Toque 1"]
        
    elif tipo2 == "ifttt":
        entao = busca_ifttts()
    
    elif tipo2 == "tv":
        entao = ["Power"]
        listaC = cn.lista_canais()
        for canal in listaC:
            entao.append(canal["nome"])
    
    elif tipo2 == "spotify":
        entao = ["Play", "Pause", "Pular"]
    
    portas_entao_mn = OptionMenu(controle, entao_var, *entao)
    portas_entao_mn.config(bg="white", activebackground=neon, font=(font_default, 20))
    portas_entao_mn["menu"].config(bg="white", activebackground=neon, font=(font_default, 20))
    dic_triggers_itens[portas_entao_mn] = [400, 280]
    portas_entao_mn.place(x=400, y=280)
    entao_var.set(entao[0])


# Atualiza o trigger para remoção conforme o tipo de componente escolhido
def atualiza_ativo(nome):
    global portas_ativo_mn
    esquece(portas_ativo_mn)
    
    id_comp = busca_id2(nome)
    
    triggers = []
    
    comp = busca_componente(id_comp)
    if comp != -1:
        tipo = comp["tipo"]
        if tipo == "botao":
            if verifica_fP(id_comp):
                triggers.append("Botão pressionado")
            if verifica_fS(id_comp):
                triggers.append("Botão solto")
            
        elif tipo == "sensor_luz":
            if verifica_fClaro(id_comp):
                triggers.append("Luz detectada")
            if verifica_fEscuro(id_comp):
                triggers.append("Escuridão detectada")
        
        elif tipo == "sensor_movimento":
            if verifica_fCom(id_comp):
                triggers.append("Movimento detectado")
            if verifica_fSem(id_comp):
                triggers.append("Inércia detectada")
        
    else:
        hor = busca_horario(id_comp)
        triggers.append(hor["nome"])
    print(triggers)
    
    portas_ativo_mn = OptionMenu(controle, trigger_var, *triggers)
    portas_ativo_mn.config(bg="white", activebackground=neon, font=(font_default, 16))
    portas_ativo_mn["menu"].config(bg="white", activebackground=neon, font=(font_default, 16))
    dic_bd_itens[portas_ativo_mn] = [400, 280]
    portas_ativo_mn.place(x=400, y=280)
    trigger_var.set(triggers[0])
        

# Abre tela para criar modos  
def abreMenuModos():
    global shownOptions
    
    escondeMenuInicial()
    shownOptions = True
    showOptions()
    
    for item, cord in dic_modos_itens.items():
        item.place(x=cord[0], y=cord[1])


# Registra uma porta com um componente no banco de dados
def registrarPorta():
    tipo = components_var.get()
    pino = ports_var.get()
    nome = input_ap.get(1.0, "end-1c")
    
    if tipo == "LED":
        id_comp = adiciona_LED(pino, nome, 0)
    
    elif tipo == "Botão":
        id_comp = adiciona_botao(pino, nome)
    
    elif tipo == "Sensor de Luz":
        id_comp = adiciona_sensor_luz(pino, nome, None)
        
    elif tipo == "Sensor de Movimento":
        id_comp = adiciona_sensor_movimento(pino, nome)
        
    elif tipo == "Campainha":
        id_comp = adiciona_campainha(pino, nome)
        
    else:
        return
    
    if type(id_comp) is int:
        msg = "Erro: Pino " + str(pino) + " já está está sendo utilizado"
        
    else: 
        msg = nome + " (" + tipo + ")\nregistrado na porta " + str(pino)
        comp = busca_componente(id_comp)
        inicializa_componente(comp)
        
        if comp["input"]:
            cadastrados1.append(comp["nome"])
        else:
            cadastrados2.append(comp["nome"])

    busted_display = Label(controle, text=msg, fg=neon, bg=preto, font=(font_default, 20), justify=LEFT)
    busted_display.place(x=40, y=440)
    controle.after(2000, busted_display.destroy)
    
    
# ======================== Menu inicial ===========================
 
# BORDAS
for i in [[1, 750, 0, 0], [600, 1, 739, 0], [600, 1, 0, 0], [1, 900, 0, 589]]:
    b = Label(controle, height=i[0], width=i[1], bg=cinza)
    b.place(x=i[2], y=i[3])

# HORA
curr_time = datetime.now().hour
if 5 <= curr_time < 12:
    time_msg = "Bom dia"
elif 12 <= curr_time < 18:
    time_msg = "Boa tarde"
else:
    time_msg = "Boa noite"
time_msg += ", Jan"
time_lbl = Label(controle, text="", fg=neon, bg=preto, font=(font_default, 36))
dic_menu_buttons[time_lbl] = [40, 70]

# STATUS
status_txt = "Tudo parece em ordem, sua casa\nestá pronta para configurar!"
status_lbl = Label(controle, text="", fg=neon, bg=preto, font=(font_default, 17), justify=LEFT)
dic_menu_buttons[status_lbl] = [40, 130]

# HORA
hour_lbl = Label(controle, text=datetime.now().strftime("%d/%m/%Y %H:%M"), fg=neon, bg=preto, font=(font_default, 17))
dic_menu_buttons[hour_lbl] = [490, 100]

# MENU
menu_img = createImage("Imagens/menu.png", 160, 160)
menu_btn = Button(controle, image = menu_img, bg=preto, activebackground=preto, highlightthickness = 0, bd=0, command = showGadgets, cursor="hand2")
dic_menu_buttons[menu_btn] = [70, 320]

settings_img = createImage("Imagens/settings2.png", 60, 60)
settings_btn = Button(controle, image = settings_img, bg=preto, activebackground=preto, highlightthickness = 0, bd=0, command = showOptions, cursor="hand2")
dic_menu_buttons[settings_btn] = [685, 500]

voltar_img = createImage("Imagens/home.png", 60, 60)
voltar_btn = Button(controle, image = voltar_img, bg=preto, activebackground=preto, highlightthickness = 0, bd=0, command = mostraMenuInicial, cursor="hand2")

ports_img = createImage("Imagens/ports.png", 40, 40)
ports_btn = Button(controle, text = "Configurar portas", image = ports_img, bg=preto, activebackground=preto, highlightthickness = 0, bd=0, compound="right", fg=neon, activeforeground=cinza, font=(font_default, 17), command=abreMenuPortas, cursor="hand2")

database_img = createImage("Imagens/database.png", 40, 40)
database_btn = Button(controle, text = "Acessar banco\nde dados", image = database_img, bg=preto, activebackground=preto, highlightthickness = 0, bd=0, compound="right", fg=neon, activeforeground=cinza, font=(font_default, 17), command = abreMenuBD, justify=LEFT, cursor="hand2")

automation_img = createImage("Imagens/automation.png", 40, 40)
automation_btn = Button(controle, text = "Criar automação", image = automation_img, bg=preto, activebackground=preto, highlightthickness = 0, bd=0, compound="right", fg=neon, activeforeground=cinza, font=(font_default, 17), command=abreMenuTriggers, cursor="hand2")

mode_img = createImage("Imagens/mode.png", 40, 40)
mode_btn = Button(controle, text = "Escolher modo", image = mode_img, bg=preto, activebackground=preto, highlightthickness = 0, bd=0, compound="right", fg=neon, activeforeground=cinza, font=(font_default, 17), command=abreMenuModos, cursor="hand2")

mostraMenuInicial()


# ============================ Menu TV ==============================
def abreMenuTV():
    global shownOptions
    shownOptions = True

    escondeMenuInicial()
    showOptions()
    cn.iniciar_sessao(controle)

tv_img = createImage("Imagens/television.png", 70, 70)
tv_btn = createButton("TV", tv_img, abreMenuTV, 17)

dic_tv_itens[Label(controle, text="TV", fg=neon, bg=preto, font=(font_default, 30), justify=LEFT)] = [40, 40]

number_img = []
for i in range(15):
    number_img.append(createImage("Imagens/" + str(i) + ".png", 40, 40))

buton_img = []
for i in range(15):
    buton_img.append(Button(controle, image=number_img[i], bg=preto, activebackground=preto, highlightthickness=0, bd=0, activeforeground=cinza, cursor="hand2"))

dic_pos = {
    0: [260, 140],
    1: [200, 200],
    2: [260, 200],
    3: [320, 200],
    4: [200, 260],
    5: [260, 260],
    6: [320, 260],
    7: [200, 320],
    8: [260, 320],
    9: [320, 320],
    10: [200, 140],
    11: [200, 380],
    12: [260, 380],
    13: [320, 380],
    14: [320, 140],
}
for i in range(15):
    dic_tv_itens[buton_img[i]] = [dic_pos[i][0], dic_pos[i][1]]


# ============================ Menu luzes ==============================
def altera_luz():
    if luzes_var != None:
        nome = luzes_var.get()
        id_led = busca_id(nome)
        altera_LED(id_led) #Raspberry
        if busca_componente(id_led)["estado"]:
            msg = nome + " ligado!"
        else:
            msg = nome + " desligado!"
        
    busted_display = Label(controle, text=msg, fg=neon, bg=preto, font=(font_default, 16), justify=LEFT)
    busted_display.place(x=40, y=500)
    controle.after(2000, busted_display.destroy)

def abreMenuLuzes():
    global shownOptions, luzes_mn, luzes_var
    shownOptions = True
    
    escondeMenuInicial()
    showOptions()
    
    for item, cord in dic_luzes_itens.items():
        item.place(x=cord[0], y=cord[1])
        
    esquece(luzes_mn)
    
    luzes_banco = []
    for componente in busca_componentes_ativos():
        tipo = componente["tipo"]
        if tipo == "LED":
            luzes_banco.append(componente["nome"])
    
    if luzes_banco != []:
        luzes_var = StringVar(controle)
        luzes_var.set(luzes_banco[0])
        luzes_mn = OptionMenu(controle, luzes_var, *luzes_banco)
        luzes_mn.config(bg="white", activebackground=neon, font=(font_default, 20))
        luzes_mn["menu"].config(bg="white", activebackground=neon, font=(font_default, 20))
        luzes_mn.place(x=70, y=280)
    else:
        luzes_mn = None
        luzes_var = None
            
light_img = createImage("Imagens/light.png", 70, 70)
light_btn = createButton("Luzes", light_img, abreMenuLuzes, 17)
dic_luzes_itens[Label(controle, text="Luzes", fg=neon, bg=preto, font=(font_default, 30), justify=LEFT)] = [40, 40]
dic_luzes_itens[Label(controle, text="Selecionar LED:", fg=neon, bg=preto, font=(font_default, 25), justify=LEFT)] = [60, 200]
power_img = createImage("Imagens/off_mode.png", 50, 50)
power_btn = createButton("ligar / desligar", power_img, altera_luz, 20)
dic_luzes_itens[power_btn] = [70, 400]
  
# ============================ Menu musica ==============================
def abreMenuMusica():
    global shownOptions
    shownOptions = True

    escondeMenuInicial()
    showOptions()

    for item, cord in dic_musica_itens.items():
        item.place(x=cord[0], y=cord[1])

    music.start_music(controle)

music_img = createImage("Imagens/music.png", 70, 70)
music_btn = createButton("Música", music_img, abreMenuMusica, 17)
dic_musica_itens[Label(controle, text="Musica", fg=neon, bg=preto, font=(font_default, 30), justify=LEFT)] = [40, 40]


# ============================ Menu alarmes ==============================
def registrarAlarme(): 
    semana = ["segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo"]
    dias_semana=[]
    hora = hora_var.get()
    minuto = minuto_var.get()
    nome = nome_var.get()
    duracao = duracao_var.get()
    
    try:
        hora = int(hora_var.get())
        minuto = int(minuto_var.get())
    except:
        print("Hora e minutos devem ser inteiros")
        return
    
    try:
        dia = int(dia_var.get())
        mes = int(mes_var.get())
        ano = 2000 + int(ano_var.get())
        datetime(ano, mes, dia)
        especifico = True
    except:
        especifico = False
        
    funcs = []
    try:
        duracao = int(duracao_var.get())
        if duracao != 0:
            camps = busca_campainhas()
            
            for camp in camps:
                func = {"funcao": "liga_campainha", "id_camp": camp, "duracao": duracao}
                funcs.append(func)
    except:
        pass
    
    semanal = False
    for i in range(len(dias_semana_var)):
        if dias_semana_var[i].get() == 1:
            semanal = True
            dias_semana.append(semana[i])
    
    if semanal:
        id_hor = cria_horario_semanal(nome, dias_semana, hora, minuto, duracao)
        for func in funcs:
            adiciona_fH(id_hor, func)
        print("Alarme semanal registrado!")
   
    if especifico:
        id_hor = cria_horario_unico(nome, ano, mes, dia, hora, minuto, duracao)
        for func in funcs:
            adiciona_fH(id_hor, func)
        print("Alarme com data específica registrado!")
    #print(funcs)
    if not semanal and not especifico:
        return
    
    busted_display = Label(controle, text="%s criado"%nome, fg=neon, bg=preto, font=(font_default, 20), justify=LEFT)
    busted_display.place(x=300, y=530)
    controle.after(2000, busted_display.destroy)
    
    return

def abreMenuAlarmes():
    global shownOptions
    shownOptions = True
    
    escondeMenuInicial()
    showOptions()
    
    for item, cord in dic_alarmes_itens.items():
        item.place(x=cord[0], y=cord[1])
        
    duracao_var.set("5")
    hora_var.set("00")
    minuto_var.set("00")
    dia_var.set("dd")
    mes_var.set("mm")
    ano_var.set("aa")
    
    for i in range(len(dias_semana_var)):
        dias_semana_var[i].set(0)
        
alarm_img = createImage("Imagens/alarm.png", 70, 70)
alarm_btn = createButton("Alarmes", alarm_img, abreMenuAlarmes, 17)
dic_alarmes_itens[Label(controle, text="Alarmes", fg=neon, bg=preto, font=(font_default, 30), justify=LEFT)] = [40, 40]
dic_alarmes_itens[Label(controle, text="Nome: \n\nDurante [s]:\n\nÀs:\n\nEm:", fg=neon, bg=preto, font=(font_default, 30), justify=LEFT)] = [60, 100]
alarmes_registrar_btn = Button(controle, text = "Cadastrar", bg=neon, activebackground=cinza, font=(font_default, 25), command=registrarAlarme, cursor="hand2")
dic_alarmes_itens[alarmes_registrar_btn] = [60, 520]

nome_var = StringVar()
duracao_var = StringVar()
hora_var = StringVar()
minuto_var = StringVar()
dia_var = StringVar()
mes_var = StringVar()
ano_var = StringVar()
dic_relogio = {1: hora_var, 2: minuto_var, 3: dia_var, 4: mes_var, 5: ano_var}

max_len = 2
def on_write(tipo, *args):
    s = dic_relogio[tipo].get()
    if len(s) > max_len:
        dic_relogio[tipo].set(s[:max_len])
hora_var.trace_variable("w", lambda *args, tipo = 1: on_write(tipo, *args))
minuto_var.trace_variable("w", lambda *args, tipo = 2: on_write(tipo, *args))
dia_var.trace_variable("w", lambda *args, tipo = 3: on_write(tipo, *args))
mes_var.trace_variable("w", lambda *args, tipo = 4: on_write(tipo, *args))
ano_var.trace_variable("w", lambda *args, tipo = 5: on_write(tipo, *args))

input_nome_alarme = Entry(controle, textvariable=nome_var, width=10, font=(font_default, 15))
input_duracao_alarme = Entry(controle, textvariable=duracao_var, width=8, font=(font_default, 15))
input_hora_alarme = Entry(controle, textvariable=hora_var, width=2, font=(font_default, 15))
input_minuto_alarme = Entry(controle, textvariable=minuto_var, width=2, font=(font_default, 15))
input_dia_alarme = Entry(controle, textvariable=dia_var, width=2, font=(font_default, 15))
input_mes_alarme = Entry(controle, textvariable=mes_var, width=2, font=(font_default, 15))
input_ano_alarme = Entry(controle, textvariable=ano_var, width=2, font=(font_default, 15))

dias_semana_var = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
pos_dias = [[150, 390], [340, 390], [505, 390], [150, 430], [340, 430], [505, 430], [150, 470]]
l_dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira   ", "Sexta-feira", "Sábado       ", "Domingo        "]

for pos, dia in enumerate(l_dias_semana):
    ck = Checkbutton(controle, text=dia, variable=dias_semana_var[pos], onvalue=1, offvalue=0, fg=preto, bg="white", activebackground=neon, font=(font_default, 14), cursor="hand2")
    dic_alarmes_itens[ck] = pos_dias[pos]

dic_alarmes_itens[input_nome_alarme] = [320, 110]
dic_alarmes_itens[input_duracao_alarme] = [320, 210]
dic_alarmes_itens[input_hora_alarme] = [320, 300]
dic_alarmes_itens[input_minuto_alarme] = [370, 300]
dic_alarmes_itens[input_dia_alarme] = [340, 470]
dic_alarmes_itens[input_mes_alarme] = [390, 470]
dic_alarmes_itens[input_ano_alarme] = [440, 470]

# ============================ Menu portas ==============================
dic_portas_itens[Label(controle, text="Configurar portas", fg=neon, bg=preto, font=(font_default, 30), justify=LEFT)] = [40, 40]

dic_portas_itens[Label(controle, text="Componente:", fg=neon, bg=preto, font=(font_default, 25), justify=LEFT)] = [40, 120]
components = ["LED", "Botão", "Sensor de Luz", "Sensor de Movimento", "Campainha"]
components_var = StringVar(controle)
portas_comp_mn = OptionMenu(controle, components_var, *components)
portas_comp_mn.config(bg="white", activebackground=neon, font=(font_default, 20))
portas_comp_mn["menu"].config(bg="white", activebackground=neon, font=(font_default, 20))
dic_portas_itens[portas_comp_mn] = [40, 160]

dic_portas_itens[Label(controle, text="Porta:", fg=neon, bg=preto, font=(font_default, 25), justify=LEFT)] = [400, 120]
ports = [8, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24, 25, 26]
ports_var = IntVar(controle)
portas_port_mn = OptionMenu(controle, ports_var, *ports)
portas_port_mn.config(bg="white", activebackground=neon, font=(font_default, 20))
portas_port_mn["menu"].config(bg="white", activebackground=neon, font=(font_default, 20))
dic_portas_itens[portas_port_mn] = [400, 160]

dic_portas_itens[Label(controle, text="Apelido:", fg=neon, bg=preto, font=(font_default, 25), justify=LEFT)] = [40, 240]
input_ap = Text(controle, height=1, width=20, font=(font_default, 25))
dic_portas_itens[input_ap] = [40, 280]

portas_registrar_btn = Button(controle, text = "Registrar", bg=neon, activebackground=cinza, font=(font_default, 25), command=registrarPorta, cursor="hand2")
dic_portas_itens[portas_registrar_btn] = [40, 360]


# ========================== Menu banco de dados ===========================
def removerComponente():
    nome = todos_cadastrados_var.get()
    id_comp = busca_id2(nome)
    
    comp = busca_componente(id_comp)
    if comp == -1:
        remove_horario(id_comp)
    else:
        removerComp(id_comp)
    
    busted_display = Label(controle, text="%s removido"%nome, fg=neon, bg=preto, font=(font_default, 20), justify=LEFT)
    busted_display.place(x=40, y=520)
    controle.after(2000, busted_display.destroy)
    
    abreMenuBD()
    
def removerTrigger():
    global portas_ativo_mn
    
    esquece(portas_ativo_mn)
    nome = inputs_ativos_var.get()
    id_comp = busca_id2(nome)
    
    trigger = trigger_var.get()
    
    comp = busca_componente(id_comp)
    if comp != -1:
        if trigger == "Botão pressionado":
            limpa_fP(id_comp)
        elif trigger == "Botão solto":
            limpa_fS(id_comp)
        elif trigger == "Luz detectada":
            limpa_fClaro(id_comp)
        elif trigger == "Escuridão detectada":
            limpa_fEscuro(id_comp)
        elif trigger == "Movimento detectado":
            limpa_fCom(id_comp)
        elif trigger == "Inércia detectada":
            limpa_fSem(id_comp)
        
    else:
        limpa_fH(id_comp)
    
    esquece(portas_ativo_mn)
    
    busted_display = Label(controle, text="Trigger removido", fg=neon, bg=preto, font=(font_default, 20), justify=LEFT)
    busted_display.place(x=40, y=520)
    controle.after(2000, busted_display.destroy)
    
    abreMenuBD()

dic_bd_itens[Label(controle, text="Acessar Banco de Dados", fg=neon, bg=preto, font=(font_default, 30), justify=LEFT)] = [40, 40]
dic_bd_itens[Label(controle, text="Componentes:", fg=neon, bg=preto, font=(font_default, 18))] = [100, 120]
dic_bd_itens[Label(controle, text="Triggers:", fg=neon, bg=preto, font=(font_default, 18))] = [400, 120]

bd_remover_comp_btn = Button(controle, text = "Remover", bg=neon, activebackground=cinza, font=(font_default, 20), command=removerComponente, cursor="hand2")
dic_bd_itens[bd_remover_comp_btn] = [80, 430]

bd_remover_trigger_btn = Button(controle, text = "Remover", bg=neon, activebackground=cinza, font=(font_default, 20), command=removerTrigger, cursor="hand2")
dic_bd_itens[bd_remover_trigger_btn] = [380, 430]


# ============================ Menu automações ==============================
def busca_id(nome):
    for comp in componentes:
        if nome == comp["nome"]:
            return comp["_id"]
    print("Erro")
    return -1

def busca_id2(nome):
    for comp in busca_removiveis():
        if nome == comp["nome"]:
            return comp["_id"]
    print("Erro")
    return -1

#se = ["Botão pressionado", "Botão solto", "Luz detectada", "Escuridão detectada", "Movimento detectado", "Inércia detectada"]
#entao = ["LED aceso", "LED desligado", "LED altera", "Tocar campainha", "Campainha para"]

def cria_automacao():
    se = ["Botão pressionado", "Botão solto", "Luz detectada", "Escuridão detectada", "Movimento detectado", "Inércia detectada"]
    entao = ["LED aceso", "LED desligado", "LED altera", "Tocar campainha", "Campainha para", "Toque 1"]
    se1 = se_var.get()
    entao1 = entao_var.get()
    input1 = busca_id(cadastrados_var1.get())
    output1 = busca_id(cadastrados_var2.get())
    
    if entao1 == entao[0]:
        funcao = {"funcao": "acende_LED", "id_led": output1}
    elif entao1 == entao[1]:
        funcao = {"funcao": "apaga_LED", "id_led": output1}
    elif entao1 == entao[2]:
        funcao = {"funcao": "altera_LED", "id_led": output1}
    elif entao1 == entao[3]:
        funcao = {"funcao": "liga_campainha", "id_camp": output1}
    elif entao1 == entao[4]:
        funcao = {"funcao": "desliga_campainha", "id_camp": output1}
    elif entao1 == entao[5]:
        funcao = {"funcao": "campainha_toque1", "id_camp": output1}
    elif tipo2 == "ifttt":
        funcao = {"funcao": "executa_ifttt", "evento": entao1}
    elif tipo2 == "tv":
        if entao1 == "Power":
            funcao = {"funcao": "power_tv"}
        else:
            listaC = cn.lista_canais()
            for canal in listaC:
                if entao1 == canal["nome"]:
                    funcao = {"funcao": "liga_canal", "numero": canal["numero"]}
    elif entao1 == "Play":
        funcao = {"funcao": "playOneTrack"}
    elif entao1 == "Pause":
        funcao = {"funcao": "pauseTrack"}
    elif entao1 == "Pular":
        funcao = {"funcao": "skipTrack"}
   
    else:
        return
    
    if se1 == "":
        return
    
    if se1 == se[0]:
        adiciona_fP_botao(input1, funcao)
    elif se1 == se[1]:
        adiciona_fS_botao(input1, funcao)
    elif se1 == se[2]:
        adiciona_fClaro_sensor_luz(input1, funcao)
    elif se1 == se[3]:
        adiciona_fEscuro_sensor_luz(input1, funcao)
    elif se1 == se[4]:
        adiciona_fCom_sensor_mov(input1, funcao)
    elif se1 == se[5]:
        adiciona_fSem_sensor_mov(input1, funcao)
    elif tipo1 == "Data periódica":
        semanais = busca_semanais()
        for semanal in semanais:
            if se1 == semanal["nome"]:
                adiciona_fH(semanal["_id"], funcao)     
    elif tipo1 == "Data específica":
        especificos = busca_especificos()
        for especifico in especificos:
            if se1 == especifico["nome"]:
                adiciona_fH(especifico["_id"], funcao)
    
    cadastrados_var1.set('')
    se_var.set('')
    cadastrados_var2.set('')
    entao_var.set('')
    esquece(portas_se_mn)
    esquece(portas_entao_mn)
    
    busted_display = Label(controle, text="Trigger cadastrado", fg=neon, bg=preto, font=(font_default, 20), justify=LEFT)
    busted_display.place(x=40, y=440)
    controle.after(2000, busted_display.destroy)
    
    return
    
dic_triggers_itens[Label(controle, text="Criar automação", fg=neon, bg=preto, font=(font_default, 30), justify=LEFT)] = [40, 40]
dic_triggers_itens[Label(controle, text="Input:", fg=neon, bg=preto, font=(font_default, 25), justify=LEFT)] = [40, 120]
dic_triggers_itens[Label(controle, text="Output:", fg=neon, bg=preto, font=(font_default, 25), justify=LEFT)] = [400, 120]
dic_triggers_itens[Label(controle, text="Se:", fg=neon, bg=preto, font=(font_default, 25), justify=LEFT)] = [40, 240]
dic_triggers_itens[Label(controle, text="Então:", fg=neon, bg=preto, font=(font_default, 25), justify=LEFT)] = [400, 240]

triggers_registrar_btn = Button(controle, text = "Registrar", bg=neon, activebackground=cinza, font=(font_default, 25), command = cria_automacao, cursor="hand2")
dic_triggers_itens[triggers_registrar_btn] = [40, 360]

#se = ["Botão pressionado", "Botão solto", "Luz detectada", "Escuridão detectada", "Movimento detectado", "Inércia detectada"]
se_var = StringVar(controle)

#entao = ["LED aceso", "LED desligado", "LED altera", "Tocar campainha", "Campainha para"]
entao_var = StringVar(controle)

trigger_var = StringVar(controle)
            
# ============================ Menu modos ==============================
def modoAcordar():
    print("Bom dia!")
    leds = busca_leds()
    for l in leds:
        acende_LED(l)
    camps = busca_campainhas()
    for camp in camps:
        liga_campainha(camp,2)
        #campainha_toque1(camp)
        
    
    
def modoSono():
    print("Boa noite!")
    leds = busca_leds()
    for l in leds:
        apaga_LED(l)
    try:
        music.pauseTrack()
    except:
        pass
    
    
def modoFesta():
    print("Party time!")
    try:
        music.playTracks("44ZrtRi24bojlfNcOacaME")
    except:
        pass
    leds = busca_leds()
    for l in leds: 
        pisca_LED(l)
        sleep(0.234)
    

def modoDesligar():
    print("Até breve!")
    exit()
    
dic_modos_itens[Label(controle, text="Escolher modo", fg=neon, bg=preto, font=(font_default, 30), justify=LEFT)] = [40, 40]

wake_img = createImage("Imagens/wake_mode.png", 70, 70)
wake_btn = createButton("Acordar", wake_img, modoAcordar, 20)    
dic_modos_itens[wake_btn] = [100, 130]

sleep_img = createImage("Imagens/sleep_mode.png", 70, 70)
sleep_btn = createButton("Dormir", sleep_img, modoSono, 20)    
dic_modos_itens[sleep_btn] = [100, 230]

party_img = createImage("Imagens/party_mode.png", 70, 70)
party_btn = createButton("Festa", party_img, modoFesta, 20)    
dic_modos_itens[party_btn] = [100, 330]

off_img = createImage("Imagens/off_mode.png", 70, 70)
off_btn = createButton("Desligar sistema", off_img, modoDesligar, 20)    
dic_modos_itens[off_btn] = [100, 430]

# ================= Propriedades e instanciação da janela ===============
controle.title("Controle da Casa Inteligente")   
controle.geometry("750x600+300+60")
controle.configure(bg=preto)
controle.resizable(False,False)  # impede que a janela seja redimensionada
controle.mainloop()