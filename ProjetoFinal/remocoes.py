#Jerônimo

#Importação das bibliotecas
from banco_componentes import *
from banco_triggers import *
from banco_horarios import *
from banco_ifttt import *
from funcoes_executaveis import *
#leds, botoes, sensores_luz, sensores_movimento, campainhas

#remove_LED, remove_botao, remove_campainha, remove_movimento, remove_luz,

tipos_removiveis = ["LED", "botao", "sensor_luz", "sensor_movimento", "campainha"]

def busca_removiveis():
    removiveis = []
    
    comps = busca_componentes_ativos()
    for comp in comps:
        if comp["tipo"] in tipos_removiveis:
            removiveis.append(comp)
    
    horarios = busca_horarios()
    removiveis.extend(horarios)
    
    return removiveis

#------------Remoções--------------------

def busca_pos(id_comp, lista):
    for i, el in enumerate(lista):
        if el["_id"] == id_comp:
            return i
    return -1
    


def remove_LED(id_led):
    pos = busca_pos(id_led, leds)
    if pos != -1:
        led = leds[pos]["led"]
        led.close()
        leds.pop(pos)
    return

def remove_botao(id_botao):
    pos = busca_pos(id_botao, botoes)
    if pos != -1:
        botao = botoes[pos]["botao"]
        botao.close()
        botoes.pop(pos)
    return

def remove_campainha(id_campainha):
    pos = busca_pos(id_campainha, campainhas)
    if pos != -1:
        campainha = campainhas[pos]["campainha"]
        campainha.close()
        campainhas.pop(pos)
    return

def remove_movimento(id_mov):
    pos = busca_pos(id_mov, sensores_movimento)
    if pos != -1:
        sMov = sensores_movimento[pos]["sensor_mov"]
        sMov.close()
        sensores_movimento.pop(pos)
    return

def remove_luz(id_luz):
    pos = busca_pos(id_luz, sensores_luz)
    if pos != -1:
        sLuz = sensores_luz[pos]["sensor_luz"]
        sLuz.close()
        sensores_luz.pop(pos)
    return





def removerComp(id_comp):
    comp = busca_componente(id_comp)
    tipo = comp["tipo"]
    if tipo == "LED":
        remove_LED(id_comp)
    
    elif tipo == "botao":
        remove_botao(id_comp)
    
    elif tipo == "sensor_luz":
        remove_luz(id_comp)
        
    elif tipo == "sensor_movimento":
        remove_movimento(id_comp)
        
    elif tipo == "campainha":
        remove_campainha(id_comp)
    
    else:
        print("Erro: componente não é removível")
        return -1
    
    remove_componente(id_comp)
    #print("'%s' removido"%comp["nome"])
    return 0


def comp_nao_vazios():
    comps = busca_componentes_ativos()
    nv = []
    for comp in comps:
        tipo = comp["tipo"]
        id_comp = comp["_id"]
        if tipo == "botao":
            if verifica_botao(id_comp):
                nv.append(comp)
        elif tipo == "sensor_luz":
            if verifica_luz(id_comp):
                nv.append(comp)
        elif tipo == "sensor_movimento":
            if verifica_mov(id_comp):
                nv.append(comp)
    
    horarios = busca_horarios()
    for horario in horarios:
        id_horario = horario["_id"]
        if verifica_fH(id_horario):
            nv.append(horario)
    
    return nv

#remove_horario(id_horario)

nvs=comp_nao_vazios()
#for nv in nvs:
#    print(nv["nome"])
    


