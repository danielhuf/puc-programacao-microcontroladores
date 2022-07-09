# importação de bibliotecas
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient
from Adafruit_CharLCD import Adafruit_CharLCD
from datetime import datetime, timedelta
from lirc import init, nextcode
from time import sleep


# a linha abaixo apaga todo o banco e reinsere os moradores
redefinir_banco()
init("aula", blocking=False)

# parâmetros iniciais do banco
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto03"]
colecao = banco["moradores"]


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
            if codigo == "KEY_OK":
                return s
            else:
                s += codigo[-1]
                lcd.message("*")
        sleep(0.1)
                

# criação de componentes
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

# loop infinito
while True:
    apt = coletar_digitos("Digite o apto:")
    if validar_apartamento(apt):
        senha = coletar_digitos("Digite a senha:")
        nome = retornar_nome_do_morador(apt, senha)
        if nome != None:
            lcd.clear()
            lcd.message("Bem-vindo(a)\n" + nome + "!")
        else:
            lcd.clear()
            lcd.message("Acesso negado")
    else:
        lcd.clear()
        lcd.message("Apartamento\ninvalido!")
    sleep(1)
