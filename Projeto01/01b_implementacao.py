# importação de bibliotecas
from os import system
from time import sleep
from mplayer import Player
from gpiozero import LED, Button
from Adafruit_CharLCD import Adafruit_CharLCD


# para de tocar músicas que tenham ficado tocando da vez passada
system("killall mplayer")

# definição de funções
def tocapausa():
    player.pause()
    if player.paused:
        led.blink()
    else:
        led.on()
        
def pulafaixa():
    player.pt_step(1)
    
def voltafaixa():
    tempo_atual = player.time_pos
    if tempo_atual != None:
        if tempo_atual > 2:
            player.time_pos = 0
        else:
            player.pt_step(-1)

# criação de componentes
player = Player()
player.loadlist("playlist.txt")

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
botao3.when_pressed = pulafaixa

lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

# loop infinito
while True:
    nome = None
    metadados = player.metadata
    if metadados != None:
        if nome != metadados["Title"]:
            lcd.clear()
            lcd.message(metadados["Title"])
            nome = metadados["Title"]
    sleep(0.2)
