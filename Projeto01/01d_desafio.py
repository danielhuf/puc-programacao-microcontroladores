# COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO
# DEPOIS FAÇA OS NOVOS RECURSOS
# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS
# importação de bibliotecas
from os import system
from time import sleep
from mplayer import Player
from gpiozero import LED, Button
from Adafruit_CharLCD import Adafruit_CharLCD
import random


# para de tocar músicas que tenham ficado tocando da vez passada
system("killall mplayer")

# definição de funções
def tocapausa():
    player.pause()
    if player.paused:
        led.blink()
    else:
        led.on()
        
def ajusta():
    if player.speed > 1:
        player.speed = 1
    else:
        player.pt_step(1)
    
def voltafaixa():
    tempo_atual = player.time_pos
    if tempo_atual != None:
        if tempo_atual > 2:
            player.time_pos = 0
        else:
            player.pt_step(-1)
            
def acelera():
    player.speed = 2

# criação de componentes
with open('playlist.txt') as f:
    lines = f.readlines()
random.shuffle(lines)
with open("shuffle.txt", "w") as output:
    for el in lines:
        output.write(el)

player = Player()
player.loadlist("shuffle.txt")

led = LED(21)
led2 = LED(22)
led3 = LED(23)
led5 = LED(25)

botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)

led.on()
botao1.when_pressed = voltafaixa
botao2.when_pressed = tocapausa
botao3.when_held = acelera
botao3.when_released = ajusta

lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

tempo = 0
cont = 0
nome = None
# loop infinito
while True:
    metadados = player.metadata
    if metadados != None:
        if nome != metadados["Title"]:
            nome = metadados["Title"]
            cont = 0
            
    duracao_total = player.length
    duracao = player.time_pos
    if duracao_total != None and duracao != None and metadados != None:
        minutos = int(duracao // 60)
        segundos = int(duracao % 60)
        minutos_tot = int(duracao_total // 60)
        segundos_tot = int(duracao_total % 60)
        lcd.clear()
        if len(metadados["Title"]) > 16 and (tempo % 4) == 0:
            if cont > len(metadados["Title"]):
                cont = 0
            lcd.message(metadados["Title"][cont:cont+16])
            cont += 1
        elif len(metadados["Title"]) > 16:
            lcd.message(metadados["Title"][cont:cont+16])
        else:
            lcd.message(metadados["Title"])
        lcd.message("\n{:02d}:{:02d} de {:02d}:{:02d}".format(minutos, segundos, minutos_tot, segundos_tot))
    tempo += 1
    sleep(0.2)