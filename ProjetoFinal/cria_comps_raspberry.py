#Jerônimo

#Importação das funções do banco
from banco_componentes import *
from banco_triggers import *
from banco_horarios import *
from banco_ifttt import *
from datetime import datetime

#Limpeza do banco
limpa_componentes()
limpa_triggers()
limpa_horarios()
limpa_ifttt()


#---------------Criação dos componentes---------------

#criação de leds

id_led1 = adiciona_LED(21, "LED Corredor", 0)
id_led2 = adiciona_LED(27, "LED Sala 1", 0)
id_led3 = adiciona_LED(19, "LED Sala 2", 0)
id_led4 = adiciona_LED(13, "LED Sala 3", 0)
id_led5 = adiciona_LED(6, "LED Sala 4", 0)
id_led6 = adiciona_LED(5, "LED Cozinha", 0)
id_led7 = adiciona_LED(9, "LED Entrada", 0)
id_led8 = adiciona_LED(25, "LED Banheiro", 0)
id_led9 = adiciona_LED(7, "LED Suíte", 0)
id_led10 = adiciona_LED(20, "LED Quarto", 0)
id_led11 = adiciona_LED(12, "LED Jardim", 0)


#Criação dos botões
id_botao = adiciona_botao(16, "Botão único")


#Criação do sensor de luz
id_sLuz = adiciona_sensor_luz(8, "Sensor de luz", None)


#Criação do sensor de movimento
id_sMov = adiciona_sensor_movimento(22, "Sensor de Movimento")


#Criação da campainha
id_camp1 = adiciona_campainha(15, "Campainha 1")
id_camp2 = adiciona_campainha(14, "Campainha 2")
id_camp3 = adiciona_campainha(24, "Campainha 3")



#-------Definição de funções para componentes----------

#'''
agora = datetime.now()
ano = agora.year
mes = agora.month
dia = agora.day
hora = agora.hour
minuto = agora.minute

id_hor1 = cria_horario_unico("Alarme em 1min", ano, mes, dia, hora, minuto + 1, 5)
id_hor2 = cria_horario_unico("Alarme em 2min", ano, mes, dia, hora, minuto + 2, 5)

funcao1 = {"funcao": "liga_campainha", "id_camp": id_camp1, "duracao": 5}
funcao2 = {"funcao": "liga_campainha", "id_camp": id_camp2, "duracao": 5}
funcao3 = {"funcao": "liga_campainha", "id_camp": id_camp3, "duracao": 5}

funcao4 = {"funcao": "campainha_toque1", "id_camp": id_camp1}
funcao5 = {"funcao": "campainha_toque1", "id_camp": id_camp2}
funcao6 = {"funcao": "campainha_toque1", "id_camp": id_camp3}

adiciona_fH(id_hor1, funcao1)
adiciona_fH(id_hor1, funcao2)
adiciona_fH(id_hor1, funcao3)

adiciona_fH(id_hor2, funcao4)
adiciona_fH(id_hor2, funcao5)
adiciona_fH(id_hor2, funcao6)

#'''