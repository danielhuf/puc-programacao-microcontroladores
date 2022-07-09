# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# importação de bibliotecas
from gpiozero import LED, Button, MotionSensor, LightSensor
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from flask import Flask, render_template
from threading import Timer

# criação do servidor
cliente = MongoClient("localhost", 27017)
banco = cliente["proj05"]
colecao = banco["leds"]

app = Flask(__name__)

# definição de funções das páginas
def atualiza_led(i, estado):
    if estado:
        leds[i-1].on()
        estados[i-1] = True
    else:
        leds[i-1].off()
        estados[i-1] = False
    dados = {"data": datetime.now(), "estado_leds": estados}
    colecao.insert(dados)

@app.route("/led/<int:x>/<string:s>") 
def led(x, s):
    if x < 1 or x > 5 or s not in ["on", "off"]:
        return "Parâmetro invalido!"
    if s == "on":
        e = True
    else:
        e = False
    atualiza_led(x, e)
    return ("Led " + str(x) + " " + s + "!")

@app.route("/estados")
def estados():
    html = "<ul> "
    for pos, e in enumerate(estados):
        if e:
            est = "acesa"
        else:
            est = "apagada"
        html += ("<li> Luz " + str(pos+1) + ": " + est + "</li>\n")
    html+="</ul>"
    return html

def apaga1():
    atualiza_led(1, False)
    global timer1
    timer1 = None

def detecta_mov():
    atualiza_led(1, True)
    global timer1
    if timer1 != None:
        timer1.cancel()
        timer1 = None

def detecta_in():
    global timer1
    timer1 = Timer(6.0, apaga1)
    timer1.start()

def claro():
    atualiza_led(2, False)
    
def escuro():
    atualiza_led(2, True)

# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
estados = []
for i in range(len(leds)):
    estados.append(leds[i].is_lit)


sensorMov = MotionSensor(27)
sensorLuz = LightSensor(8)


global timer1
timer1 = None
sensorMov.when_motion = detecta_mov
sensorMov.when_no_motion = detecta_in

sensorLuz.threshold = 0.5
sensorLuz.when_light = claro
sensorLuz.when_dark = escuro

# https://3424-139-82-11-60.ngrok.io/led/2/off


busca = {} 
ordenacao = [ ["data", DESCENDING] ] 
documento = colecao.find_one(busca, sort=ordenacao)
#print(documento)

if documento != None:
    for pos, i in enumerate(documento["estado_leds"]):
        atualiza_led(pos+1, i)

# rode o servidor
app.run(port=5000, debug=True)

# DEPOIS FAÇA OS NOVOS RECURSOS