# importação de bibliotecas
from gpiozero import LED, MotionSensor, LightSensor, DistanceSensor, Button 
from threading import Timer
from requests import post, get 


# definição de funções
def apaga2():
    led2.off()
    global timer1
    timer1 = None

def detecta_mov():
    led1.on()
    led2.on()
    global timer1
    if timer1 != None:
        timer1.cancel()
        timer1 = None

def detecta_in():
    led1.off()
    global timer1
    timer1 = Timer(4.0, apaga2)
    timer1.start()
    
def dados_sensor():
    evento = "sensores"
    endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/"  + chave

    dados = {"value1": "{:.2f}".format(sensorLuz.value*100),
             "value2": "{:.2f}".format(sensorDist.distance*100)}
    
    resultado = post(endereco, json=dados)
    print("\n", resultado.text, "\n\n")


# criação de componentes
led1 = LED(21)
led2 = LED(22)
sensor = MotionSensor(27)
sensorLuz = LightSensor(8)
sensorDist = DistanceSensor(trigger=17, echo=18)
botao2 = Button(12)

chave = "cOsV4PelmB1EWsDoCKeATe"


global timer1
timer1 = None
sensor.when_motion = detecta_mov
sensor.when_no_motion = detecta_in
botao2.when_pressed = dados_sensor

# loop infinito
