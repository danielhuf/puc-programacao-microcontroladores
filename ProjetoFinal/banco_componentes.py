#Jerônimo

#Importação das bibliotecas
from pymongo import MongoClient, ASCENDING, DESCENDING
from banco_triggers import *

#-----------------Inicialização do banco de dados-----------------
cliente = MongoClient("localhost", 27017)
banco = cliente["casa_inteligente"]
colecao_comp = banco["componentes"]


#---------------------Modelos-----------------------

#Componentes

#LEDs
#{"_id": 123, "tipo": "LED", "pino": 21, "nome": "Lâmpada da cozinha", "inativo": False, "estado": 0, "input": False}

#Botões
#{"_id": 123, "tipo": "botao", "pino": 11, "nome": "Lâmpada da cozinha", "inativo": False, "fP": [], "fS": [], "input": True}

#Sensores de luz
#{"_id": 123, "tipo": "sensor_luz", "pino": 8, "nome": "Lâmpada da cozinha", "inativo": False, "limite": 0.3, "fClaro": [], "fEscuro": [], "input": True}

#Sensores de movimento
#{"_id": 123, "tipo": "sensor_movimento", "pino": 27, "nome": "Lâmpada da cozinha", "id": 0, "inativo": False, "fCom": [], "fSem": [], "input": True}

#Campainhas
#{"tipo": "campainha", "pino": 16, "nome": "Lâmpada da cozinha", "inativo": False, "input": False}

#Datas
#{"tipo": "data", "pino": None, "nome": "Data periódica", "inativo": False, "input": True}
#{"tipo": "data", "pino": None, "nome": "Data específica", "inativo": False, "input": True}


#IFTTT
#{"tipo": "ifttt", "pino": None, "nome": "IFTTT", "inativo": False, "input": False}


tipos_validos = ["LED", "botao", "sensor_luz", "sensor_movimento", "campainha", "data", "ifttt", "tv", "spotify"]



#-----------------Componentes em geral---------------------------

#Apaga dados referentes aos componentes no banco de dados
def limpa_componentes():
    colecao_comp.drop()
    print("Coleção 'componentes' removida")
    return

#Retorna lista com os pinos que já estão sendo usados por algum componente
def pinos_usados():
    busca = {"inativo": False}
    componentes = list( colecao_comp.find(busca) )
    pinos = []
    for componente in componentes:
        if componente["pino"] != None:
            pinos.append(componente["pino"])
    return pinos

#Adiciona um novo componente no banco de dados e retorna o id
def adiciona_componente(tipo, pino, nome):
    if tipo not in tipos_validos:
        print("Erro: Tipo de componente '%s' inválido"%tipo)
        return -1
    pinos = pinos_usados()
    if pino in pinos:
        print("Erro: Pino %s já está está sendo utilizado"%str(pino))
        return -2
    dados_componente = {"tipo": tipo, "pino": pino, "nome": nome, "inativo": False}
    res = colecao_comp.insert_one(dados_componente)
    #print("Componente '%s' do tipo '%s' criado no pino %d."%(nome,tipo,pino))
    return res.inserted_id

#Retorna os dados de um componente a partir do id
def busca_componente(id_comp):
    busca = {"_id": id_comp}
    componente = colecao_comp.find_one(busca)
    if componente == None:
        #print("Erro: componente não encontrado")
        return -1
    return componente

#Retorna uma lista dos coponentes que não foram "excluídos"
def busca_componentes_ativos():
    busca = {"inativo": False}
    componentes = list( colecao_comp.find(busca) )
    return componentes

#Remove ("exclui") um componente alterando "inativo" para True
def remove_componente(id_comp):
    componente = busca_componente(id_comp)
    if componente == -1:
        print("Erro: componente não encontrado")
        return -1
    elif componente["inativo"] == True:
        print("Erro: componente já removido")
        return -2
    busca = {"_id": id_comp}
    dados = {"inativo" : True}
    colecao_comp.update_one(busca, {"$set": dados})
    #print("'%s' removido"%componente["nome"])
    return 0

#Atualiza o nome de um componente a partir do id
def atualiza_nome(id_comp, nome):
    busca = {"_id": id_comp}
    dados = {"nome" : nome}
    colecao_comp.update_one(busca, {"$set": dados})
    return

#Altera o pino de um componente a partir do id
def altera_pino(id_comp, pino):
    pinos = pinos_usados()
    if pino in pinos:
        print("Erro: Pino %d já está está sendo utilizado"%pino)
        return -1
    busca = {"_id": id_comp}
    dados = {"pino" : pino}
    colecao_comp.update_one(busca, {"$set": dados})
    return 0






#----------------------LEDs---------------------------

#Adiciona um LED no banco de dados e retorna o id
def adiciona_LED(pino, nome, estado):
    id_led = adiciona_componente("LED", pino, nome)
    if type(id_led) == int:
        return id_led
    busca = {"_id": id_led}
    dados = {"input": False, "estado" : estado}
    colecao_comp.update_one(busca, {"$set": dados})
    return id_led

#Atualiza o registro do estado de um LED no banco de dados a partir do id
def atualiza_LED(id_led, estado):
    busca = {"_id": id_led}
    dados = {"estado" : estado}
    colecao_comp.update_one(busca, {"$set": dados})
    return



def busca_leds():
    comps = busca_componentes_ativos()
    leds = []
    for comp in comps:
        if comp["tipo"] == "LED":
            leds.append(comp["_id"])
    return leds




#----------------------Botões---------------------------

#Adiciona um botão no banco de dados e retorna o id
def adiciona_botao(pino, nome):
    id_botao = adiciona_componente("botao", pino, nome)
    id_trigger1 = cria_trigger()
    id_trigger2 = cria_trigger()
    busca = {"_id": id_botao}
    dados = {"input": True, "fP" : id_trigger1, "fS": id_trigger2}
    colecao_comp.update_one(busca, {"$set": dados})
    return id_botao

#Adiciona uma função no trigger "fP" (when_pressed) de um botão
def adiciona_fP_botao(id_botao, funcao):
    dados = busca_componente(id_botao)
    id_trigger = dados["fP"]
    adiciona_funcao(id_trigger, funcao)
    return

#Adiciona uma função no trigger "fS" (when_released) de um botão
def adiciona_fS_botao(id_botao, funcao):
    dados = busca_componente(id_botao)
    id_trigger = dados["fS"]
    adiciona_funcao(id_trigger, funcao)
    return

def verifica_fP(id_botao):
    dados = busca_componente(id_botao)
    id_trigger = dados["fP"]
    return verifica_trigger(id_trigger)

def verifica_fS(id_botao):
    dados = busca_componente(id_botao)
    id_trigger = dados["fS"]
    return verifica_trigger(id_trigger)

def verifica_botao(id_botao):
    return verifica_fP(id_botao) or verifica_fS(id_botao)

def limpa_fP(id_comp):
    dados = busca_componente(id_comp)
    id_trigger = dados["fP"]
    remove_funcoes(id_trigger)
    return

def limpa_fS(id_comp):
    dados = busca_componente(id_comp)
    id_trigger = dados["fS"]
    remove_funcoes(id_trigger)
    return









#----------------------Sensores de luz---------------------------

#Adiciona um sensor de luz no banco de dados e retorna o id
def adiciona_sensor_luz(pino, nome, limite):
    id_sensor_luz = adiciona_componente("sensor_luz", pino, nome)
    if type(id_sensor_luz) == int:
        return id_sensor_luz
    id_trigger1 = cria_trigger()
    id_trigger2 = cria_trigger()
    busca = {"_id": id_sensor_luz}
    dados = {"input": True, "limite" : limite, "fClaro": id_trigger1, "fEscuro": id_trigger2}
    colecao_comp.update_one(busca, {"$set": dados})
    return id_sensor_luz

#Atualiza o threshold ou uma função do sensor de luz no banco de dados
def atualiza_sensor_luz(id_sensor_luz, limite):
    busca = {"_id": id_sensor_luz}
    dados = {"limite": limite}
    colecao_comp.update_one(busca, {"$set": dados})
    return

#Adiciona uma função no trigger "fClaro" (when_light) de um sensor de luz
def adiciona_fClaro_sensor_luz(id_sensor_luz, funcao):
    dados = busca_componente(id_sensor_luz)
    id_trigger = dados["fClaro"]
    adiciona_funcao(id_trigger, funcao)
    return

#Adiciona uma função no trigger "fEscuro" (when_dark) de um sensor de luz
def adiciona_fEscuro_sensor_luz(id_sensor_luz, funcao):
    dados = busca_componente(id_sensor_luz)
    id_trigger = dados["fEscuro"]
    adiciona_funcao(id_trigger, funcao)
    return


def verifica_fClaro(id_comp):
    dados = busca_componente(id_comp)
    id_trigger = dados["fClaro"]
    return verifica_trigger(id_trigger)

def verifica_fEscuro(id_comp):
    dados = busca_componente(id_comp)
    id_trigger = dados["fEscuro"]
    return verifica_trigger(id_trigger)

def verifica_luz(id_comp):
    return verifica_fClaro(id_comp) or verifica_fEscuro(id_comp)

def limpa_fClaro(id_comp):
    dados = busca_componente(id_comp)
    id_trigger = dados["fClaro"]
    remove_funcoes(id_trigger)
    return

def limpa_fEscuro(id_comp):
    dados = busca_componente(id_comp)
    id_trigger = dados["fEscuro"]
    remove_funcoes(id_trigger)
    return










#----------------------Sensores de movimento---------------------------

#Adiciona um sensor de movimentos no banco de dados e retorna o id
def adiciona_sensor_movimento(pino, nome):
    id_sensor_movimento = adiciona_componente("sensor_movimento", pino, nome)
    id_trigger1 = cria_trigger()
    id_trigger2 = cria_trigger()
    busca = {"_id": id_sensor_movimento}
    dados = {"input": True, "fCom" : id_trigger1, "fSem": id_trigger2}
    colecao_comp.update_one(busca, {"$set": dados})
    return id_sensor_movimento

#Adiciona uma função no trigger "fCom" (when_motion) de um sensor de luz
def adiciona_fCom_sensor_mov(id_sensor_mov, funcao):
    dados = busca_componente(id_sensor_mov)
    id_trigger = dados["fCom"]
    adiciona_funcao(id_trigger, funcao)
    return

#Adiciona uma função no trigger "fSem" (when_no_motion) de um sensor de luz
def adiciona_fSem_sensor_mov(id_sensor_mov, funcao):
    dados = busca_componente(id_sensor_mov)
    id_trigger = dados["fSem"]
    adiciona_funcao(id_trigger, funcao)
    return


def verifica_fCom(id_comp):
    dados = busca_componente(id_comp)
    id_trigger = dados["fCom"]
    return verifica_trigger(id_trigger)

def verifica_fSem(id_comp):
    dados = busca_componente(id_comp)
    id_trigger = dados["fSem"]
    return verifica_trigger(id_trigger)

def verifica_mov(id_comp):
    return verifica_fCom(id_comp) or verifica_fSem(id_comp)


def limpa_fCom(id_comp):
    dados = busca_componente(id_comp)
    id_trigger = dados["fCom"]
    remove_funcoes(id_trigger)
    return

def limpa_fSem(id_comp):
    dados = busca_componente(id_comp)
    id_trigger = dados["fSem"]
    remove_funcoes(id_trigger)
    return



#------------------------Campainhas---------------------------

#Adiciona uma campainha no banco de dados e retorna o id
def adiciona_campainha(pino, nome):
    id_campainha = adiciona_componente("campainha", pino, nome)
    if type(id_campainha) == int:
        return id_campainha
    busca = {"_id": id_campainha}
    dados = {"input": False}
    colecao_comp.update_one(busca, {"$set": dados})
    return id_campainha

def busca_campainhas():
    comps = busca_componentes_ativos()
    camps = []
    for comp in comps:
        if comp["tipo"] == "campainha":
            camps.append(comp["_id"])
    return camps




#--------------------Datas----------------------


def adiciona_comp_data(nome):
    id_data = adiciona_componente("data", None, nome)
    if type(id_data) == int:
        return id_data
    busca = {"_id": id_data}
    dados = {"input": True}
    colecao_comp.update_one(busca, {"$set": dados})
    return id_data

def confere_comp_data():
    busca = {"tipo": "data"}
    datas = list( colecao_comp.find(busca) )
    return len(datas)
    






#--------------------IFTTT----------------------

def adiciona_comp_ifttt(nome):
    id_ifttt = adiciona_componente("ifttt", None, nome)
    if type(id_ifttt) == int:
        return id_ifttt
    busca = {"_id": id_ifttt}
    dados = {"input": False}
    colecao_comp.update_one(busca, {"$set": dados})
    return id_ifttt

def confere_comp_ifttt():
    busca = {"tipo": "ifttt"}
    ifttts = list( colecao_comp.find(busca) )
    return len(ifttts)





#--------------------TV----------------------

def adiciona_comp_tv(nome):
    id_tv = adiciona_componente("tv", None, nome)
    if type(id_tv) == int:
        return id_tv
    busca = {"_id": id_tv}
    dados = {"input": False}
    colecao_comp.update_one(busca, {"$set": dados})
    return id_tv

def confere_comp_tv():
    busca = {"tipo": "tv"}
    tvs = list( colecao_comp.find(busca) )
    return len(tvs)
    
#--------------------TV----------------------

def adiciona_comp_spotify(nome):
    id_spotify = adiciona_componente("spotify", None, nome)
    if type(id_spotify) == int:
        return id_spotify
    busca = {"_id": id_spotify}
    dados = {"input": False}
    colecao_comp.update_one(busca, {"$set": dados})
    return id_spotify

def confere_comp_spotify():
    busca = {"tipo": "spotify"}
    spotifys = list( colecao_comp.find(busca) )
    return len(spotifys)

    
    
    
    
    
    
    
    
    
    
    

    
