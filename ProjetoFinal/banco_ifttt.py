#Jerônimo

#Importação das bibliotecas
from pymongo import MongoClient, ASCENDING, DESCENDING
#from banco_triggers import *


#-----------------Inicialização do banco de dados-----------------
cliente = MongoClient("localhost", 27017)
banco = cliente["casa_inteligente"]
colecao_ifttt = banco["ifttt"]



#{"nome": "evento01"}



def limpa_ifttt():
    colecao_ifttt.drop()
    print("Coleção 'ifttt' removida")
    return

def busca_ifttt(id_ifttt):
    busca = {"_id": id_ifttt}
    ifttt = colecao_ifttt.find_one(busca)
    if ifttt == None:
        print("Erro: IFTTT não encontrado")
        return -1
    return ifttt

def busca_ifttts():
    busca = {}
    ifttts = list( colecao_ifttt.find(busca) )
    nomes = []
    for ifttt in ifttts:
        nomes.append(ifttt["nome"])
    return nomes


def cria_ifttt(nome):
    dados = {"nome": nome}
    res = colecao_ifttt.insert_one(dados)
    return res.inserted_id


def remove_ifttt(id_ifttt):
    busca = {"_id": id_horario}
    colecao_hor.delete_one(busca)
    print("IFTTT removido")
    return






