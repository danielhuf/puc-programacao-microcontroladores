# importação de bibliotecas
from gpiozero import LED, Button
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from flask import Flask

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

# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
estados = []
for i in range(len(leds)):
    estados.append(leds[i].is_lit)
    
# https://3424-139-82-11-60.ngrok.io/led/2/off

# rode o servidor
app.run(port=5000, debug=False)