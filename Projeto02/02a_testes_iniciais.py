# importação de bibliotecas
from gpiozero import LED, Button
from time import sleep
from lirc import init, nextcode
from Adafruit_CharLCD import Adafruit_CharLCD

# definição de funções
def liga_tudo():
    for l in leds:
        l.on()
        
def desliga_tudo():
    for l in leds:
        l.off()

# criação de componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

botao2.when_pressed = liga_tudo
botao3.when_pressed = desliga_tudo

init("aula", blocking=False)
pos = -1

# loop infinito
while True:
    lista_codigo = nextcode()
    if lista_codigo != []:
        codigo = lista_codigo[0]
        if codigo == "KEY_1":
            lcd.clear()
            lcd.message("LED 1\nselecionado")
            pos = 0
        elif codigo == "KEY_2":
            lcd.clear()
            lcd.message("LED 2\nselecionado")
            pos = 1
        elif codigo == "KEY_3":
            lcd.clear()
            lcd.message("LED 3\nselecionado")
            pos = 2
        elif codigo == "KEY_4":
            lcd.clear()
            lcd.message("LED 4\nselecionado")
            pos = 3
        elif codigo == "KEY_5":
            lcd.clear()
            lcd.message("LED 5\nselecionado")
            pos = 4
        elif codigo == "KEY_OK":
            if pos != -1:
                leds[pos].toggle()
        elif codigo == "KEY_UP":
            if pos < 4:
                pos += 1
                lcd.clear()
                lcd.message("LED " + str(pos+1) + "\nselecionado")
        elif codigo == "KEY_DOWN":
            if pos > 0:
                pos -= 1
                lcd.clear()
                lcd.message("LED " + str(pos+1) + "\nselecionado")
    sleep(0.2)