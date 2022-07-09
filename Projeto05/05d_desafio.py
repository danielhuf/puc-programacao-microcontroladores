# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# importação de bibliotecas
from gpiozero import LED, Button, MotionSensor, LightSensor
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from flask import Flask, render_template
from threading import Timer
from requests import post, get 

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
    print(estados)
    dados = {"data": datetime.now(), "estado_leds": estados}
    colecao.insert(dados)
    #print(estados)
    
def atualiza_ledA(i, estado):
    if estado:
        leds[i-1].on()
        estados[i-1] = True
    else:
        leds[i-1].off()
        estados[i-1] = False
    #print(estados)

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
    
def tot_segundos(n_led, data):
    tot = 0
    atual = datetime.now()
    busca = {"data": {"$gt": data}} 
    ordenacao = [ ["data", DESCENDING] ] 
    documentos = list( colecao.find(busca, sort=ordenacao) )
    for registro in documentos:
        if registro["estado_leds"][n_led]:
            tot += (atual - registro["data"]).total_seconds()
        atual = registro["data"]
        
    busca = {"data": {"$lt": data}} 
    ordenacao = [ ["data", DESCENDING] ] 
    documento = colecao.find_one(busca, sort=ordenacao)
    if documento != None:
        if documento["estado_leds"][n_led]:
            tot += (atual - data).total_seconds()
    return tot

def timer_recorrente():
    evento = "planilha"
    endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/"  + chave
    agora = datetime.now()
    data = agora - timedelta(minutes=1)
    val2 = ""
    for i in range(5):
        sec = tot_segundos(i, data)
        val2 += (str(int(sec)) + " ||| ")
    val2 = val2[:-5]
    dados = {"value1": str(agora),
             "value2": val2}
    
    resultado = post(endereco, json=dados)
    print("\n", resultado.text, "\n\n")
    
    global timer2
    timer2 = Timer(30.0, timer_recorrente)
    timer2.start()
    
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
        atualiza_ledA(pos+1, i)
        
global timer2
timer2 = None

chave = "cOsV4PelmB1EWsDoCKeATe"
timer_recorrente()

""" evento = "planilha"
# endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/"  + chave
dados = {"value1": "Data",
         "value2": "Luz 1 ||| Luz 2 ||| Luz 3 ||| Luz 4 ||| Luz 5"}
resultado = post(endereco, json=dados)
print("\n", resultado.text, "\n\n") """

# rode o servidor
app.run(port=5000, debug=True)
