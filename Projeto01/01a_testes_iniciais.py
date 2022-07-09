# importação de bibliotecas
from gpiozero import LED, Button
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD


# definição de funções
global conta
conta = 0

def tog():
    led2.toggle()
    
def pisca():
    global conta
    lcd.clear()
    led3.blink(n=4)
    conta += 1
    lcd.message(str(int(conta)))

# criação de componentes
led = LED(21)
led2 = LED(22)
led3 = LED(23)
led5 = LED(25)

botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)

lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

led.blink(on_time=1.0, off_time=3.0)
botao2.when_pressed = tog
botao3.when_pressed = pisca

# loop infinito
while True:
    if botao1.is_pressed and led.is_lit:
        led5.on()
    else:
        led5.off()
    sleep(0.2)