# Neste playground 03 B, vamos trabalhar com o banco de dados MongoDb.
# Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


# Inicialização do simulador. Escreva todo o seu código dentro da main!
from extra.playground import rodar

@rodar
def main():
    
    # Começamos importando as bibliotecas, como sempre.
    from pymongo import MongoClient, ASCENDING, DESCENDING
    from extra.redefinir_banco import redefinir_banco
    
    from gpiozero import LED, Button
    from Adafruit_CharLCD import Adafruit_CharLCD
    from time import sleep
    from datetime import datetime, timedelta
    from lirc import init, nextcode
    
    
    # A linha abaixo apaga todos os dados anteriores do banco de dados.
    # O objetivo é evitar que o banco fique lotado depois de rodar o código várias vezes.
    # Mas você pode comentar essa linha depois, se quiser.
    redefinir_banco()
    
    
    # Vamos começar criando um cliente para  o MongoDb.
    # Procuramos uma conexão local na porta 27017 (é o mesmo conceito do Projeto 02).
    cliente = MongoClient("localhost", 27017)
    
    
    # O MongoDb pode ter vários bancos de dados, para projetos diferentes.
    # Vamos preparar a criação de um banco chamado "playground" (poderia ser qualquer outro nome).
    # Obs: na verdade, o banco só vai ser criado de verdade depois que inserirmos dados.
    banco = cliente["playground"]
    
    
    # O nosso banco agora pode ter várias coleções, para lidar com vários tipos de dados.
    # Para quem já trabalhou com SQL, elas são equivalentes às tabelas.
    # E, de novo, eu posso criar coleções com o nome que eu quiser.
    colecao_de_filmes = banco["filmes"]
    colecao_de_albums = banco["albums"]
    
    
    # Agora vamos criar alguns documentos para as duas coleções.
    # Para isso, usarmos os dicionários de Python.
    filme1 = {"nome": "A Origem",               "diretor": "Christopher Nolan",  "ano": 2010,  "duração": 148,  "tem_no_netflix": True}
    filme2 = {"nome": "O Auto da Compadecida",  "diretor": "Guel Arraes",        "ano": 2000,  "duração": 104,  "tem_no_netflix": False}
    filme3 = {"nome": "Herói",                  "diretor": "Zhang Yimou",        "ano": 2002,  "duração": 99,   "tem_no_netflix": False}
    
    album1 = {"nome": "A Night at the Opera",  "artista": "Queen",               "estilo": "Rock",        "ano": 1975,  "tem_no_spotify": True}
    album2 = {"nome": "Moro no Brasil",        "artista": "Farofa Carioca",      "estilo": "Brasileiro",  "ano": 1998,  "tem_no_spotify": False}
    album3 = {"nome": "Mettavolution",         "artista": "Rodrigo y Gabriela",  "estilo": "Rock",        "ano": 2019,  "tem_no_spotify": True}
    
    
    # Para inserir os documentos nas coleções, usamos a insert_one ou a insert_many.
    # Na teoria, eu usei insert porque o Raspberry do laboratório usa um MongoDb mais antigo.
    # Você poderia usar a insert aqui também, mas daria um warning no Shell.
    colecao_de_filmes.insert_one(filme1)
    colecao_de_filmes.insert_many([filme2, filme3])
    
    colecao_de_albums.insert_many([album1, album2, album3])
    
    print("Dados iniciais inseridos com sucesso!")
    
    
    # RODE O CÓDIGO ATÉ AQUI E VEJA SE A MENSAGEM ACIMA APARECE NO SHELL.
    # DEPOIS, ABRA O APP MONGODB COMPASS E CLIQUE EM CONNECT (SEM DIGITAR NADA!).
    # CLIQUE NO BANCO "playground" NA ESQUERDA, CLIQUE NAS COLEÇÕES E VEJA OS DADOS INSERIDOS.
    
    
    # CRIE E INSIRA NOVOS DOCUMENTOS NAS DUAS COLEÇÕES, COM ALGUNS DOS SEUS FILMES E ALBUMS FAVORITOS.
    # DEPOIS VOLTE PARA O MONGODB COMPASS E CLIQUE NO BOTAO ⟳ PARA ATUALIZAR OS DADOS. 
    
    
    # Depois de inserir documentos no banco, podemos buscá-los de várias maneiras.
    # Para encontrar 1 documento em particular, podemos usar a função find_one.
    # Essa função recebe um dicionário com os parâmetros de busca, e retorna o dicionário do documento encontrado.
    dados_da_busca = {"nome": "Herói"}
    filme_de_espachins_bizarros = colecao_de_filmes.find_one(dados_da_busca)
    
    
    # IMPRIMA A VARIÁVEL ACIMA NO SHELL, PARA VER OS DADOS DO DOCUMENTO ENCONTRADO.
    # PERCEBA QUE HÁ UMA CHAVE "_id", GERADA PELO MONGODB.
    print(filme_de_espachins_bizarros)
    
    
    # Caso haja mais de 1 resultado para a busca, a find_one escolhe o primeiro que encontrar.
    # Esse resultado pode não ser necessariamente o primeiro que você inseriu. É meio imprevisível.
    dados_da_busca = {"estilo": "Rock"}
    qualquer_album_de_rock = colecao_de_albums.find_one(dados_da_busca)
    
    
    # Uma solução é colocar mais parâmetros na busca, para ser mais específico.
    dados_da_busca = {"estilo": "Rock", "artista": "Rodrigo y Gabriela"}
    album_genial_pouco_conhecido = colecao_de_albums.find_one(dados_da_busca)
    
    
    
    # BUSQUE E IMPRIMA O FILME DE 2010 DO DIRETOR "Christopher Nolan"
    dados_da_busca = {"ano": 2010, "diretor": "Christopher Nolan"}
    filme = colecao_de_filmes.find_one(dados_da_busca)
    print(filme)
    
    
    # Mas pode ser que você queira buscar vários documentos de uma vez só.
    # Para isso, é só usar a **find** em vez da find_one.
    # Obs: eu converto o resultado para lista, para ficar mais didático de lidar.
    dados_da_busca = {"estilo": "Rock"}
    todos_os_albuns_de_rock = list( colecao_de_albums.find(dados_da_busca) )
    
    
    # Agora é só percorrer a lista de resultados usando um for.
    for album in todos_os_albuns_de_rock:
        
        nome_do_album = album["nome"]
        
        # Poderia acessar também as outras chaves do documento, e fazer algo com isso...
        
        
    # Também dá para fazer buscas com valores maiores ou menores que algumas coisa.
    # Para isso, é só colocar um dicionário dentro do dicionário, com chaves $gt ou $lt.
    dados_da_busca = {"ano": {"$gt": 2000}}
    albuns_apos_ano_2000 = list( colecao_de_albums.find(dados_da_busca) )
    
    dados_da_busca = {"duração": {"$lt": 120}}
    filmes_com_menos_de_2_horas = list( colecao_de_filmes.find(dados_da_busca) )
    
    
    # Por fim, você pode pedir para ordenar os documentos por algum critério.
    # Agora usamos uma lista de listas, no formato abaixo.
    dados_da_busca = {"tem_no_netflix": True}
    ordenacao = [ ["duração", DESCENDING] ]
    filmes_mais_longos_do_netflix = list( colecao_de_filmes.find(dados_da_busca, sort=ordenacao) )
    
    
    # Achou estranho a ordenação ser uma lista de listas?
    # É que dá para usar outro critério, caso o anterior dê "empate" entre os documentos.
    # Outro detalhe: a busca pode ser um dicionário vazio, se você quiser pegar todos os dados.
    dados_da_busca = {}
    ordenacao = [ ["gênero", ASCENDING], ["artista", ASCENDING ] ]
    albuns_por_genero_e_artista = list( colecao_de_albums.find(dados_da_busca, sort=ordenacao) )
    
    
    
    # BUSQUE TODOS OS FILMES ANTERIORES AO ANO 2010 QUE NÃO ESTEJAM NO NETFLIX, EM ORDEM DECRESCENTE DE ANO.
    # PERCORRA OS RESULTADOS E IMPRIMA CADA UM NO FORMATO "NOME DO FILME (ANO): __ horas e __ minutos de duração"
    dados_da_busca = {"ano": {"$lt": 2010}, "tem_no_netflix": False}
    ordenacao = [ ["ano", DESCENDING] ]
    filmes_selec = list(colecao_de_filmes.find(dados_da_busca, sort=ordenacao))
    for filme in filmes_selec:
        hora = str(int(filme["duração"] // 60))
        minu = str(int(filme["duração"] % 60))
        print(filme["nome"] + " (" + str(filme["ano"]) + "): " + hora + " horas e " + minu + " minutos de duração")
    
    
    
    # EXPERIMENTE INTEGRAR OS DISPOSITIVOS COM O BANCO DE DADOS! BRINQUE À VONTADE!
    # OBS: CRIE OUTRO BANCO COM OUTRAS COLEÇÕES, PARA QUE OS DADOS NÃO SEJAM APAGADOS A CADA "RUN".
    # Sugestão 1: quando o usuário apertar uma tecla do controle remoto, salve o código dela e a data/hora atual numa coleção.
    init("aula", blocking=False)
    colecao_de_teclas = banco["teclas"]
    
    
    # Sugestão 2: ao apertar um dos botões, busque todos os códigos salvos em ordem descrescente de data/hora.
    # Sugestão 3: depois de buscar, exiba os códigos salvos no LCD um de cada vez, dando um sleep entre eles.
    def busca_dados():
        print("oi")
        busca = {}
        ordenacao = [ ["data", DESCENDING] ]
        documentos = list( colecao_de_teclas.find(busca, sort=ordenacao) )
        for d in documentos:
            lcd.clear()
            lcd.message(d["tecla"])
            sleep(1)
    
    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    botao1 = Button(11)
    botao1.when_pressed = busca_dados
    
    while True:
        lista_com_codigo = nextcode()
        if lista_com_codigo != []:
            codigo = lista_com_codigo[0]
            dados = {"tecla": codigo, "data": datetime.now()}
            colecao_de_teclas.insert_one(dados)
            print("Colocado no banco!")
        sleep(0.1)