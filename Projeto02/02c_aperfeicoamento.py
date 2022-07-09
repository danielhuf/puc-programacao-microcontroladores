# importação de bibliotecas
from py_irsend.irsend import send_once
from flask import Flask, render_template, redirect
import threading as th


# criação do servidor
app = Flask(__name__)

# definição de funções das páginas
@app.route("/aumenta_volume")
def aumenta_volume():
    send_once("aquario", ["KEY_VOLUMEUP"])
    return redirect("/menu")

@app.route("/diminui_volume")
def diminui_volume():
    send_once("aquario", ["KEY_VOLUMEDOWN"])
    return redirect("/menu")

@app.route("/mudo")
def mudo():
    send_once("aquario", ["KEY_MUTE"])
    return redirect("/menu")

@app.route("/muda_canal/<string:canal>")
def muda_canal(canal):
    for c in canal:
        send_once("aquario", ["KEY_" + c])
    send_once("aquario", ["KEY_OK"])
    return redirect("/menu")

@app.route("/desliga/<float:n>")
def desliga(n):
    def apos_n():
        send_once("aquario", ["KEY_POWER"])
    S = th.Timer(n, apos_n)
    S.start()
    return redirect("/menu")

@app.route("/menu")
def menu():
    return render_template("menu.html")

# rode o servidor
app.run(port=5000, debug=True)