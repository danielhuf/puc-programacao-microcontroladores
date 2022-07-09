# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS
# importação de bibliotecas
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient, ASCENDING, DESCENDING
from Adafruit_CharLCD import Adafruit_CharLCD
from datetime import datetime, timedelta
from lirc import init, nextcode
from time import sleep
from gpiozero import Buzzer, Button, DistanceSensor


# a linha abaixo apaga todo o banco e reinsere os moradores
#redefinir_banco()
init("aula", blocking=False)

# parâmetros iniciais do banco
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto03"]
colecao = banco["moradores"]
colecao2 = banco["acessos"]


# definição de funções
def validar_apartamento(num_ap):
    dados = {"apartamento":num_ap}
    resp = colecao.find_one(dados)
    if resp != None:
        return True
    else:
        return False
    
def retornar_nome_do_morador(num_ap, senha):
    dados = {"apartamento":num_ap, "senha":senha}
    resp = colecao.find_one(dados)
    if resp != None:
        return resp["nome"]
    else:
        return None
    
def coletar_digitos(msg):
    lcd.clear()
    lcd.message(msg + "\n")
    s = ''
    while True:
        lista_com_codigo = nextcode()
        if lista_com_codigo != []:
            codigo = lista_com_codigo[0]
            buzzer.beep(n=1, on_time=0.2, off_time=0.2)
            if codigo == "KEY_OK":
                return s
            else:
                s += codigo[-1]
                lcd.message("*")
        sleep(0.1)

def inicia():
    apt = coletar_digitos("Digite o apto:")
    dados={}
    if validar_apartamento(apt):
        dados["apt"] = apt
        dados["tempo"] = datetime.now()
        senha = coletar_digitos("Digite a senha:")
        nome = retornar_nome_do_morador(apt, senha)
        if nome != None:
            dados["nome"] = nome
            lcd.clear()
            lcd.message("Bem-vindo(a)\n" + nome + "!")
        else:
            lcd.clear()
            lcd.message("Acesso negado")
            buzzer.beep(n=2, on_time=0.4, off_time=0.4)
        colecao2.insert(dados)
    else:
        lcd.clear()
        lcd.message("Apartamento\ninvalido!")
        buzzer.beep(n=2, on_time=0.4, off_time=0.4)
    sleep(1)
    lcd.clear()

def admin():
    apt = coletar_digitos("Digite o apto:")
    if validar_apartamento(apt):
        busca = {"apt":apt}
        ordenacao = [["tempo",DESCENDING]]
        doc = list(colecao2.find(busca,sort=ordenacao))
        for d in doc:
            nome = d.get("nome","SENHA INCORRETA")
            print(d["tempo"].strftime("%d/%m (%H:%M): ") + nome)
                   

# criação de componentes
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
lcd.clear()
button1 = Button(11)
buzzer = Buzzer(16)
sensor = DistanceSensor(trigger=17, echo=18)
sensor.threshold_distance = 0.1
sensor.when_in_range = inicia

button1.when_pressed = admin

# loop infinito
while True:
    sleep(0.1)