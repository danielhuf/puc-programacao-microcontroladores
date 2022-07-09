#Jerônimo

#Importação das bibliotecas
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta, date
from time import sleep
from threading import Thread, Timer

from banco_triggers import *


#-----------------Inicialização do banco de dados-----------------
cliente = MongoClient("localhost", 27017)
banco = cliente["casa_inteligente"]
colecao_hor = banco["horarios"]

#indices = {"segunda": 0, "terça": 1, "quarta": 2, "quinta": 3, "sexta": 4, "sábado": 5, "domingo": 6}



#{"nome": "Entrega da meta","data": date, "horario": [hora, minuto], "fH": id_trigger, "executado": False}
#{"nome": "Aula de micro", "dias_semana": [segunda,quarta], "horario": [14, 30], "fH": id_trigger, "executado": False}



#agora = datetime.now()

#tempo = datetime(2018, 3, 28, 15, 35, 12)

#texto = tempo.strftime("%d/%m/%Y %H:%M")

#print(texto)

def limpa_horarios():
    colecao_hor.drop()
    print("Coleção 'horarios' removida")
    return

def busca_horario(id_horario):
    busca = {"_id": id_horario}
    horario = colecao_hor.find_one(busca)
    if horario == None:
        print("Erro: horário não encontrado")
        return -1
    return horario

def busca_horarios_NE(): #não executados
    busca = {"executado": False}
    horarios = list( colecao_hor.find(busca) )
    return horarios

def busca_horarios(): #não executados
    busca = {}
    horarios = list( colecao_hor.find(busca) )
    return horarios

def busca_semanais():
    busca = {"dias_semana": {"$exists": True}}
    horarios_semanais = list( colecao_hor.find(busca) )
    return horarios_semanais

def busca_especificos():
    busca = {"data": {"$exists": True}, "executado": False}
    horarios_especificos = list( colecao_hor.find(busca) )
    return horarios_especificos








#trigger para ser executado uma única vez em dia e horário específicos
def cria_horario_unico(nome, ano, mes, dia, hora, minuto, duracao):
    data = datetime(ano, mes, dia)
    id_trigger = cria_trigger()
    dados = {"nome": nome, "data": data, "horario": [hora, minuto], "duracao": duracao, "fH": id_trigger, "executado": False}
    res = colecao_hor.insert_one(dados)
    return res.inserted_id

#Trigger para ser executado repetidamente em dias da semana definidos
def cria_horario_semanal(nome, dias_semana, hora, minuto, duracao):
    id_trigger = cria_trigger()
    dados = {"nome": nome, "dias_semana": dias_semana, "horario": [hora, minuto], "duracao": duracao, "fH": id_trigger, "executado": False}
    res = colecao_hor.insert_one(dados)
    return res.inserted_id




def executou_horario(id_horario):
    busca = {"_id": id_horario}
    dados = {"executado": True}
    colecao_hor.update_one(busca, {"$set": dados})
    
    dados = colecao_hor.find_one(busca)
    if "dias_semana" in dados:
        timer = Timer(61, ja_passou, args=[id_horario])
        timer.start()
    return


def ja_passou(id_horario):
    busca = {"_id": id_horario}
    dados = {"executado": False}
    colecao_hor.update_one(busca, {"$set": dados})
    return


def altera_nome_horario(id_horario,novo_nome):
    busca = {"_id": id_horario}
    dados = {"nome": novo_nome}
    colecao_hor.update_one(busca, {"$set": dados})
    return


def altera_semana_horario(id_horario, semana):
    busca = {"_id": id_horario}
    dados = {"dias_semana": semana}
    colecao_hor.update_one(busca, {"$set": dados})
    return

def remove_horario(id_horario):
    busca = {"_id": id_horario}
    colecao_hor.delete_one(busca)
    #print("Horário removido")
    return

def altera_data_horario(id_horario, ano, mes, dia):
    busca = {"_id": id_horario}
    data = datetime(ano, mes, dia)
    dados = {"data": data}
    colecao_hor.update_one(busca)
    return

def altera_hora_min_horario(id_horario, hora, minuto):
    busca = {"_id": id_horario}
    data = datetime(ano, mes, dia)
    dados = {"horario": [hora, minuto]}
    colecao_hor.update_one(busca)
    return


#---------------fH----------

def adiciona_fH(id_horario, funcao):
    dados = busca_horario(id_horario)
    id_trigger = dados["fH"]
    adiciona_funcao(id_trigger, funcao)
    return


def busca_fH_horario(id_horario):
    horario = busca_horario(id_horario)
    if type(horario) == int:
        return -1
    id_trigger = horario["fH"]
    funcoes = funcoes_trigger(id_trigger)
    if type(funcoes) == int:
        return -2
    return funcoes


def remove_funcao_fH_horario(id_horario, pos):
    horario = busca_horario(id_horario)
    if type(horario) == int:
        return -1
    id_trigger = horario["fH"]
    res = remove_funcao(id_trigger, pos)
    if res == -1:
        return -2
    return 0


def remove_funcoes_fH_horario(id_horario):
    horario = busca_horario(id_horario)
    if type(horario) == int:
        return -1
    id_trigger = horario["fH"]
    remove_funcoes(id_trigger)
    return 0


def verifica_fH(id_horario):
    horario = busca_horario(id_horario)
    id_trigger = horario["fH"]
    return verifica_trigger(id_trigger)

def limpa_fH(id_horario):
    horario = busca_horario(id_horario)
    id_trigger = horario["fH"]
    remove_funcoes(id_trigger)
    return
