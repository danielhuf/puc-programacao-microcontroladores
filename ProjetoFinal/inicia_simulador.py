#Jerônimo

# Inicialização do simulador e importação das funções do banco
from extra.playground import rodar
from banco_componentes import *
from banco_horarios import *
from threading import Thread, Timer
from remocoes import removerComp
from funcoes_executaveis import *

@rodar
def main():
    #Importação das bibliotecas
    from gpiozero import LED, Button, Buzzer, LightSensor, MotionSensor
    from time import sleep 
    
    #inicializa_componentes, eternidade
    #inicializa_componentes()
    eternidade.start()
    inicializa_componentes()
    
    #botao1 = Button(11)
    
    #print(leds)
    #botaoc = botoes[0]["botao"]
    
    #botaoc.close()
    
    #botao1 = Button(11)
    #botao1.when_pressed = leds[1]["led"].toggle
    #led1 = LED(21)
    #led1.off()
    
    
    

    global comps
    def print_comps():
        global comps
        comps = leds.copy()
        comps.extend(campainhas.copy())
        comps.extend(botoes.copy())
        comps.extend(sensores_movimento.copy())
        comps.extend(sensores_luz.copy())
        for comp in comps:
            print(comp)
    
    #print_comps()
    
    #id1 = comps[0]["_id"]
    
    #removerComp(id1)
    
    print("\n")
        
    #print(comps)
    
    #-------------Loop infinito-------------
    while True:
        sleep(0.1)
    
    