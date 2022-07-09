#Jerônimo

#Importação das bibliotecas
from gpiozero import LED, Button, Buzzer, LightSensor, MotionSensor
from time import sleep
from threading import Thread, Timer
from TonalBuzzer import TonalBuzzer, Tone
from requests import post
from py_irsend.irsend import send_once

from banco_componentes import *
from banco_horarios import *
from banco_ifttt import *
import comunicacao_spot as music


__all__ = ["cria_fixos", "inicializa_componente", "inicializa_componentes", "eternidade", "leds", "botoes", "sensores_luz", "sensores_movimento", "campainhas", 
           "acende_LED", "apaga_LED", "altera_LED", "liga_campainha", "desliga_campainha", "campainha_toque1", "liga_canal", "pisca_LED"]

#-------------Constantes-------------
chave = "cOdWKUvSx1UKJU4UL9MC-z"   #ifttt

qtd_ifttt = 3

nome_controle = "aquario"


#-------------------------Criação de componentes fixos-------------------


def cria_fixos():
    ndatas = confere_comp_data()
    if ndatas != 2: 
        adiciona_comp_data("Data periódica")
        adiciona_comp_data("Data específica")
    nifttts = confere_comp_ifttt()
    if nifttts == 0:
        adiciona_comp_ifttt("IFTTT")
    ifttts = busca_ifttts()
    if len(ifttts) < qtd_ifttt:
        for i in range(len(ifttts), qtd_ifttt):
            nome = "evento%02d"%(i+1)
            cria_ifttt(nome)
    ntv = confere_comp_tv()
    if ntv == 0:
        adiciona_comp_tv("TV")
    nspotify = confere_comp_spotify()
    if nspotify == 0:
        adiciona_comp_spotify("Spotify")
    #criar componente fixo de spotify
    return











#------------Funções de inicialização de componentes----------------

#Inicializa um led
def inicializa_led(dados):
    id_led = dados["_id"]
    pino = dados["pino"]
    estado = dados["estado"]
    nome = dados["nome"]
    led = LED(pino)
    if estado == 1:
        led.on()
    else:
        led.off()
    dic_led = {"led": led, "_id": id_led, "pino": pino, "nome": nome}
    leds.append(dic_led)
    return

#Inicializa um botão
def inicializa_botao(dados):
    id_botao = dados["_id"]
    pino = dados["pino"]
    nome = dados["nome"]
    botao = Button(pino)
    
    id_fP = dados["fP"]
    id_fS = dados["fS"]
    #fP = funcoes_trigger(id_fP)
    #fS = funcoes_trigger(id_fS)
    botao.when_pressed = botao_solto
    botao.when_released = botao_pressionado
    
    dic_botao = {"botao": botao, "_id": id_botao, "pino": pino, "nome": nome, "fP": id_fP, "fS": id_fS}
    botoes.append(dic_botao)
    return

#Inicializa um sensor de luz
def inicializa_sensor_luz(dados):
    id_sensor_luz = dados["_id"]
    pino = dados["pino"]
    nome = dados["nome"]
    limite = dados["limite"]
    sensor = LightSensor(pino)
    
    id_fClaro = dados["fClaro"]
    id_fEscuro = dados["fEscuro"]
    #fClaro = funcoes_trigger(id_fClaro)
    #fEscuro = funcoes_trigger(id_fEscuro)
    sensor.when_light = funcao_claro
    sensor.when_dark = funcao_escuro
    
    dic_sensor = {"sensor_luz": sensor, "_id": id_sensor_luz, "pino": pino, "nome": nome, "limite": limite, "fClaro": id_fClaro, "fEscuro": id_fEscuro}
    sensores_luz.append(dic_sensor)
    return

#Inicializa um sensor de movimento
def inicializa_sensor_movimento(dados):
    id_sensor_mov = dados["_id"]
    pino = dados["pino"]
    nome = dados["nome"]
    sensor = MotionSensor(pino)
    
    id_fCom = dados["fCom"]
    id_fSem = dados["fSem"]
    #fCom = funcoes_trigger(id_fCom)
    #fSem = funcoes_trigger(id_fSem)
    sensor.when_motion = funcao_com_movimento
    sensor.when_no_motion = funcao_sem_movimento
    
    dic_sensor = {"sensor_mov": sensor, "_id": id_sensor_mov, "pino": pino, "nome": nome, "fCom": id_fCom, "fSem": id_fSem}
    sensores_movimento.append(dic_sensor)
    return

#Inicializa uma campainha
def inicializa_campainha(dados):
    id_campainha = dados["_id"]
    pino = dados["pino"]
    nome = dados["nome"]
    #campainha = Buzzer(pino)
    campainha = TonalBuzzer(pino)
    
    dic_campainha = {"campainha": campainha, "_id": id_campainha, "pino": pino, "nome": nome}
    campainhas.append(dic_campainha)
    return




def inicializa_componente(componente):
    tipo = componente["tipo"]
        
    if tipo == "LED":
        inicializa_led(componente)
    
    elif tipo == "botao":
        inicializa_botao(componente)
    
    elif tipo == "sensor_luz":
        inicializa_sensor_luz(componente)
        
    elif tipo == "sensor_movimento":
        inicializa_sensor_movimento(componente)
        
    elif tipo == "campainha":
        inicializa_campainha(componente)
    return

#Inicializa todos os compontes ativos registrados no banco de dados
def inicializa_componentes():
    componentes = busca_componentes_ativos()
    
    for componente in componentes:
        inicializa_componente(componente)
    return













#------------Funções de busca dos componentes----------

#Busca um botão nas lista botoes
def busca_botao(botao):
    for b in botoes:
        if botao == b["botao"]:
            return b
    print("Erro: Botão não encontrado")
    return -1

#Busca um LED na lista leds
def busca_LED(id_led):
    for l in leds:
        if id_led == l["_id"]:
            return l
    print("Erro: LED não encontrado")
    print(id_led)
    return -1

#Busca um sensor de luz na lista sensores_luz
def busca_sensor_luz(sensor):
    for s in sensores_luz:
        if sensor == s["sensor_luz"]:
            return s
    print("Erro: Sensor_luz não encontrado")
    return -1

#Busca um sensor de movimento na lista sensores_movimento
def busca_sensor_mov(sensor):
    for s in sensores_movimento:
        if sensor == s["sensor_mov"]:
            return s
    print("Erro: Sensor_mov não encontrado")
    return -1

#Busca uma campainha na lista campainhas
def busca_campainha(id_campainha):
    for c in campainhas:
        if id_campainha == c["_id"]:
            return c
    print("Erro: Campainha não encontrado")
    print(id_campainha)
    return -1




#-----------------------Funções executáveis---------------------------------

#-----Funções com LED-----

#{"funcao": "acende_led", "id_led": 1}
def acende_LED(id_led):
    dados = busca_LED(id_led)
    led = dados["led"]
    led.on()
    atualiza_LED(id_led, 1)
    return

#{"funcao": "apaga_led", "id_led": 1}
def apaga_LED(id_led):
    dados = busca_LED(id_led)
    led = dados["led"]
    led.off()
    atualiza_LED(id_led, 0)
    return

def altera_LED(id_led):
    dados = busca_LED(id_led)
    led = dados["led"]
    led.toggle()
    if led.is_lit:
        estado = 1
    else:
        estado = 0
    atualiza_LED(id_led, estado)
    return

def pisca_LED(id_led):
    dados = busca_LED(id_led)
    led = dados["led"]
    led.blink(on_time=0.234, off_time=0.234)
    return


#-----Funções com campainha-----

def liga_campainha(id_campainha, duracao=0):
    dados = busca_campainha(id_campainha)
    campainha = dados["campainha"]
    #campainha.on()
    campainha.play(Tone("A4"))
    if duracao != 0:
        timer = Timer(duracao, desliga_campainha, args=[id_campainha])
        timer.start()
    return

def desliga_campainha(id_campainha):
    dados = busca_campainha(id_campainha)
    campainha = dados["campainha"]
    #campainha.off()
    campainha.stop()
    return

def play(tune, tb):
    for note, duration in tune:
            print(note)
            tb.play(note)
            sleep(float(duration))
    tb.stop()

def campainha_toque1(id_campainha):
    dados = busca_campainha(id_campainha)
    campainha = dados["campainha"]
    tune = [('C#4', 0.2), ('D4', 0.2), (None, 0.2),
        ('Eb4', 0.2), ('E4', 0.2), (None, 0.6),
        ('F#4', 0.2), ('G4', 0.2), (None, 0.6),
        ('Eb4', 0.2), ('E4', 0.2), (None, 0.2),
        ('F#4', 0.2), ('G4', 0.2), (None, 0.2),
        ('C4', 0.2), ('B4', 0.2), (None, 0.2),
        ('F#4', 0.2), ('G4', 0.2), (None, 0.2),
        ('B4', 0.2), ('Bb4', 0.5), (None, 0.6),
        ('A4', 0.2), ('G4', 0.2), ('E4', 0.2), 
        ('D4', 0.2), ('E4', 0.2)]
    play(tune, campainha)
    return



#--------------------spotify-------------------

#{"funcao": "spotify_play"}
#def spotify_play():
#    playOneTrack()




#-----Mensagem-----

def imprime(mensagem):
    print(mensagem)


#-------ifttt--------

#{"funcao": "executa_ifttt", "evento": "evento01"}
def executa_ifttt(evento):
    endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/" + chave
    res = post(endereco)
    #print(res)
    return


#-----------------------TV----------------

def liga_canal(numero_canal):
    for tecla in numero_canal:
        send_once(nome_controle, ["KEY_%s"%tecla])
        print("KEY_%s"%tecla)
        sleep(0.2)
    send_once(nome_controle, ["KEY_OK"])
    print("KEY_OK")

def power_tv():
    send_once(nome_controle, ["KEY_POWER"])
    print("KEY_POWER")
    sleep(0.2)


#------------------triggers-------------





def executa_funcao(funcao):
    nome = funcao["funcao"]
    
    if nome == "acende_LED":
        acende_LED(funcao["id_led"])
    elif nome == "apaga_LED":
        apaga_LED(funcao["id_led"])
    elif nome == "altera_LED":
        altera_LED(funcao["id_led"])
    
    elif nome == "liga_campainha":
        if "duracao" in funcao:
            liga_campainha(funcao["id_camp"], funcao["duracao"])
        else:
            liga_campainha(funcao["id_camp"])
    elif nome == "desliga_campainha":
        desliga_campainha(funcao["id_camp"])
        
    elif nome == "campainha_toque1":
        campainha_toque1(funcao["id_camp"])
    
    elif nome == "print":
        print(funcao["mensagem"])
        print("Função '%s' não encontrada"%nome)
    
    elif nome == "executa_ifttt":
        executa_ifttt(funcao["evento"])
        
    elif nome == "power_tv":
        power_tv()
        
    elif nome == "liga_canal":
        liga_canal(funcao["numero"])
    
    elif nome == "playOneTrack":
        music.playOneTrack()
        
    elif nome == "pauseTrack":
        music.pauseTrack()
        
    elif nome == "skipTrack":
        music.skipTrack()
    
    
    
    return


def executa_trigger(id_trigger):
    funcoes = funcoes_trigger(id_trigger)
    for funcao in funcoes:
        executa_funcao(funcao)

def botao_pressionado(botao):
    dados = busca_botao(botao)
    print("'%s' pressionado"%dados["nome"])
    id_trigger = dados["fP"]
    executa_trigger(id_trigger)
    return

def botao_solto(botao):
    dados = busca_botao(botao)
    print("'%s' solto"%dados["nome"])
    id_trigger = dados["fS"]
    executa_trigger(id_trigger)
    return

def funcao_claro(sensor):
    dados = busca_sensor_luz(sensor)
    print("Ficou claro em '%s'"%dados["nome"])
    id_trigger = dados["fClaro"]
    executa_trigger(id_trigger)
    return

def funcao_escuro(sensor):
    dados = busca_sensor_luz(sensor)
    print("Ficou escuro em '%s'"%dados["nome"])
    id_trigger = dados["fEscuro"]
    executa_trigger(id_trigger)
    return

def funcao_com_movimento(sensor):
    dados = busca_sensor_mov(sensor)
    print("Há movimento em '%s'"%dados["nome"])
    id_trigger = dados["fCom"]
    executa_trigger(id_trigger)
    return

def funcao_sem_movimento(sensor):
    dados = busca_sensor_mov(sensor)
    print("Movimento parou em '%s'"%dados["nome"])
    id_trigger = dados["fSem"]
    executa_trigger(id_trigger)
    return




#--------------------Tempo e horário---------------


def funcao_eterna():
    semana = ["segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo"]
    while True:
        dados_horarios = busca_horarios_NE()
        agora = datetime.now()
        data_hoje = agora.date()
        hora = agora.hour
        minuto = agora.minute
        horario = [hora, minuto]
        dia_hoje = semana[agora.weekday()]
        
        for dados_horario in dados_horarios:
            hora_min = dados_horario["horario"] 
            
            if "data" in dados_horario:
                data = dados_horario["data"].date()
                
                if data == data_hoje and hora_min == horario:
                    print(dados_horario["nome"])
                    id_hor = dados_horario["_id"]
                    executou_horario(id_hor)
                    
                    id_trigger = dados_horario["fH"]
                    executa_trigger(id_trigger)
                    
            #elif "dias_semana" in dados_horario:
            else:
                dias = dados_horario["dias_semana"]
                if dia_hoje in dias and hora_min == horario:
                    print(dados_horario["nome"])
                    
                    id_hor = dados_horario["_id"]
                    executou_horario(id_hor)
                    
                    id_trigger = dados_horario["fH"]
                    executa_trigger(id_trigger)
        sleep(10)











#--------------------Modelos---------------------------

#dic_led = {"led": led, "_id": id_led, "pino": pino, "nome": nome}
#dic_botao = {"botao": botao, "_id": id_botao, "pino": pino, "nome": nome, "fP": [], "fS": []}
#dic_sensor_luz = {"sensor_luz": sensor, "_id": id_sensor_luz, "pino": pino, "nome": nome, "limite": limite, "fClaro": [], "fEscuro": []}
#dic_sensor_mov = {"sensor_mov": sensor, "_id": id_sensor_mov, "pino": pino, "nome": nome, "fCom": [], "fSem": []}
#dic_campainha = {"campainha": campainha, "_id": id_campainha, "pino": pino, "nome": nome}

#-------------Inicialização das listas de componentes-------------

global leds, botoes, sensores_luz, sensores_movimento, campainhas, eternidade

leds = []

botoes = []

sensores_luz = []

sensores_movimento = []

campainhas = []

eternidade = Thread(target=funcao_eterna)



#Inicialização dos componentes
#eternidade.start()
#inicializa_componentes()
