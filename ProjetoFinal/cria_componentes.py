#Jerônimo

#Importação das funções do banco
from banco_componentes import *
from banco_triggers import *
from banco_horarios import *
from banco_ifttt import *

#Limpeza do banco
limpa_componentes()
limpa_triggers()
limpa_horarios()
limpa_ifttt()


#---------------Criação dos componentes---------------

#criação de leds

id_led1 = adiciona_LED(21, "Lâmpada da sala", 1)
id_led2 = adiciona_LED(22, "Lâmpada da cozinha", 1)
id_led3 = adiciona_LED(23, "Lâmpada do corredor", 0)
id_led4 = adiciona_LED(24, "Lâmpada do quarto", 1)
id_led5 = adiciona_LED(25, "LED 5", 0)

atualiza_LED(id_led2, 0)


#Criação dos botões
id_botao1 = adiciona_botao(11, "Botão 01")
id_botao2 = adiciona_botao(12, "Botão 02")
id_botao3 = adiciona_botao(13, "Botão 03")
id_botao4 = adiciona_botao(14, "Botão 04")
id_botao5 = adiciona_botao(15, "Botão defeituso")

remove_componente(id_botao5)

#Criação do sensor de luz
id_sLuz = adiciona_sensor_luz(8, "Sensor de luz", None)
atualiza_sensor_luz(id_sLuz, 0.3)


#Criação do sensor de movimento
id_sMov = adiciona_sensor_movimento(37, "Sensor de Movimento")
altera_pino(id_sMov, 27)


#Criação da campainha
id_camp = adiciona_campainha(16, "Campaiha")
atualiza_nome(id_camp, "Campainha")



#adiciona_comp_data("1", "Data periódica")
#adiciona_comp_data("2", "Data específica")

#-------Definição de funções para componentes----------
#'''
#Botão 01
funcao1 = {"funcao": "acende_LED", "id_led": id_led3}
funcao2 = {"funcao": "apaga_LED", "id_led": id_led4}
funcao3 = {"funcao": "altera_LED", "id_led": id_led5}
adiciona_fP_botao(id_botao1, funcao1)
adiciona_fP_botao(id_botao1, funcao2)
adiciona_fP_botao(id_botao1, funcao3)

#Botão 02
funcao4 = {"funcao": "liga_campainha", "id_camp": id_camp}
funcao5 = {"funcao": "desliga_campainha", "id_camp": id_camp}
adiciona_fP_botao(id_botao2, funcao4)
adiciona_fS_botao(id_botao2, funcao5)

#Sensor de luz
funcao6 = {"funcao": "beep_campainha", "id_camp": id_camp, "n": 2}
funcao7 = {"funcao": "beep_campainha", "id_camp": id_camp, "n": 3}
adiciona_fClaro_sensor_luz(id_sLuz, funcao6)
adiciona_fEscuro_sensor_luz(id_sLuz, funcao7)

#Sensor de movimento
funcao8 = {"funcao": "acende_LED", "id_led": id_led2}
funcao9 = {"funcao": "apaga_LED", "id_led": id_led2}
adiciona_fCom_sensor_mov(id_sMov, funcao8)
adiciona_fSem_sensor_mov(id_sMov, funcao9)

#Botão 03
funcao10 = {"funcao": "print", "mensagem": "Ei! Tenha mais cuidado para não quebrar este botão!"}
adiciona_fP_botao(id_botao3, funcao10)

#'''








#'''
limpa_horarios()

id_hor1 = cria_horario_unico("Tocaaaaaa", 2022, 6, 24, 19, 14, 0)

funcao11 = {"funcao": "campainha_toque1", "id_camp": id_camp}
adiciona_fH(id_hor1, funcao11)

id_hor2 = cria_horario_semanal("Hoje é sexta", ["sexta", "sabado"], 19, 44, 0)

funcao12 = {"funcao": "campainha_toque2", "id_camp": id_camp}
adiciona_fH(id_hor2, funcao12)

#fH2 = busca_fH_horario(id_hor2)
#print(fH2)

#remove_horario(id_hor2)
#'''








#limpa_componentes()
#limpa_triggers()
#limpa_horarios()
#limpa_ifttt()