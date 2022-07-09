#Jerônimo

#Importação das bibliotecas
from pymongo import MongoClient, ASCENDING, DESCENDING

#-----------------Inicialização do banco de dados-----------------
cliente = MongoClient("localhost", 27017)
banco = cliente["casa_inteligente"]
colecao_trig = banco["triggers"]



#-----------------------Modelo-------------------------

#trigger
#{"_id": abc, "funcoes": []}



#-----------------Funções com triggers-------------------------

#Apaga dados referentes aos triggers no banco de dados
def limpa_triggers():
    colecao_trig.drop()
    print("Coleção 'triggers' removida")
    return

#Cria um trigger vazio (sem funções) e retorna o id
def cria_trigger():
    dados = {"funcoes": []}
    res = colecao_trig.insert_one(dados)
    return res.inserted_id

#Retorna a lista de funções de um trigger
def funcoes_trigger(id_trigger):
    busca = {"_id": id_trigger}
    trigger = colecao_trig.find_one(busca)
    if trigger == None:
        print("Erro: trigger não encontrado")
        return -1
    funcoes = trigger["funcoes"]
    return funcoes

#Adiciona uma função à lista de funções de um trigger
def adiciona_funcao(id_trigger, funcao):
    funcoes = funcoes_trigger(id_trigger)
    if type(funcoes) == int:
        print("Erro ao adicionar função")
        return -1
    funcoes.append(funcao)
    busca = {"_id": id_trigger}
    dados = {"funcoes": funcoes}
    colecao_trig.update_one(busca, {"$set": dados})
    return 0

#Remove todas as funções da lista de funções de um trigger
def remove_funcoes(id_trigger):
    busca = {"_id": id_trigger}
    dados = {"funcoes": []}
    colecao_trig.update_one(busca, {"$set": dados})
    return

def remove_funcao(id_trigger, pos):
    funcoes = funcoes_trigger(id_trigger)
    if pos + 1 > len(funcoes):
        print("Erro: função não está no trigger")
        return -1
    funcoes.pop(pos)
    busca = {"_id": id_trigger}
    dados = {"funcoes": funcoes}
    colecao_trig.update_one(busca, {"$set": dados})
    return 0




def verifica_trigger(id_trigger):
    funcoes = funcoes_trigger(id_trigger)
    if len(funcoes) == 0:
        return False
    return True
    
    
    
    
    
    
    