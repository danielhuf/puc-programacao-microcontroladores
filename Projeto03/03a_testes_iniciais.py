# importação de bibliotecas
from gpiozero import Buzzer, Button, DistanceSensor, LED
from pymongo import MongoClient, ASCENDING, DESCENDING
from Adafruit_CharLCD import Adafruit_CharLCD
from datetime import datetime, timedelta



# definição de funções
def tocar():
    buzzer.beep(n=1,on_time=0.5,off_time=0.5)
    
def piscar_led():
    led1.blink(n=2)

def med_distancia():
    d = sensor.distance *100
    lcd.clear()
    lcd.message("%.1f cm"%d)
    dados = {"distancia": d, "tempo": datetime.now()}
    colecao.insert(dados)


# criação de componentes

button1 = Button(11)
button2 = Button(12)
led1 = LED(21)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
buzzer = Buzzer(16)
sensor = DistanceSensor(trigger=17, echo=18)
cliente = MongoClient("localhost", 27017)
banco = cliente["aula"]
colecao = banco["distancias"]


button1.when_pressed = tocar
button2.when_pressed = med_distancia
sensor.threshold_distance = 0.1
sensor.when_in_range = piscar_led
sensor.when_out_of_range = piscar_led
