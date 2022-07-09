# importação de bibliotecas
from py_irsend.irsend import send_once
from flask import Flask
import threading as th


# criação do servidor
app = Flask(__name__)

# definição de funções das páginas
@app.route("/aumenta_volume")
def aumenta_volume():
    send_once("aquario", ["KEY_VOLUMEUP"])
    return "Volume aumentado."

@app.route("/diminui_volume")
def diminui_volume():
    send_once("aquario", ["KEY_VOLUMEDOWN"])
    return "Volume diminuído."

@app.route("/mudo")
def mudo():
    send_once("aquario", ["KEY_MUTE"])
    return "Mudo apertado."

@app.route("/muda_canal/<string:canal>")
def muda_canal(canal):
    for c in canal:
        send_once("aquario", ["KEY_" + c])
    send_once("aquario", ["KEY_OK"])
    return "Muda para canal " + canal + "."

@app.route("/desliga/<float:n>")
def desliga(n):
    def apos_n():
        send_once("aquario", ["KEY_POWER"])
    S = th.Timer(n, apos_n)
    S.start()
    return "TV desligará após " + str(n) + " segundos."

# rode o servidor
app.run(port=5000, debug=True)