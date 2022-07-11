# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS

# importação de bibliotecas
from gpiozero import LED, Button,Buzzer,DistanceSensor
from Adafruit_CharLCD import Adafruit_CharLCD
from requests import get, post
from time import sleep
from os import system
from subprocess import Popen
from urllib.request import urlretrieve
from mplayer import Player
from datetime import datetime, timedelta
from unidecode import unidecode

global aplicativo
aplicativo = None

player = Player()

global tempo
tempo = None

# parâmetros iniciais do Telegram
chave = "******" 
id_da_conversa = "5271993060"
global endereco_base
endereco_base = "https://api.telegram.org/bot" + chave
endereco_dados_do_bot = endereco_base + "/getMe"
led1 = LED(21)
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
campainha = Buzzer(16)
sensor = DistanceSensor(trigger=17, echo=18)
sensor.threshold_distance = 0.1

# definição de funções
def desliga_led():
    led1.off()
    
def liga_campainha():
    campainha.on()

def desliga_campainha():
    global endereco_base
    campainha.off()
    
    dados3 = {"chat_id": id_da_conversa, "text": "Alguém está na porta!", "reply_markup":{"keyboard": [["Abrir"], ["Soar Alarme"], ["Ignorar"]], "one_time_keyboard":True}}
    endereco_para_mensagem = endereco_base + "/sendMessage"    
    
    print("\nEnviando mensagem...", dados3)
    resultado = post(endereco_para_mensagem, json=dados3)
    print(resultado.text)
    system("fswebcam --resolution 640x480 --skip 10 foto.jpg")
    arquivo  = {"photo": open("foto.jpg", "rb")}
    endereco_para_foto = endereco_base + "/sendPhoto"
    dados = {"chat_id": id_da_conversa}
    
    print("\nEnviando foto...")
    #resultado = post(endereco_para_foto, data=dados, files=arquivo)
    print(resultado.text)
    
def comeca_gravar():
    global aplciativo
    comando = ["arecord", "--duration", "30", "audio.wav"] 
    aplicativo = Popen(comando)
    
def para_gravar():
    global aplicativo
    global endereco_base
    if aplicativo != None:
        aplicativo.terminate()
        aplicativo = None
        
    system("opusenc audio.wav audio.ogg")
    endereco = endereco_base + "/sendVoice"
    dados = {"chat_id":id_da_conversa}
    arquivo = {"voice":open("audio.ogg","rb")}
    resposta = post(endereco, data=dados, files=arquivo)
    
def captura_tempo():
    global tempo
    tempo  = datetime.now()
    print("entrou")

def envia_alerta():
    global tempo
    global endereco_base
    duracao = (datetime.now() - tempo).total_seconds()
    print("saiu")
    if duracao >= 10:
        dados = {"chat_id": id_da_conversa, "text": "Pessoa saiu"}
        endereco_para_mensagem = endereco_base + "/sendMessage"    
        print("\nEnviando mensagem...")
        resultado = post(endereco_para_mensagem, json=dados)
        print(resultado.text)
        
botao1.when_pressed = liga_campainha
botao1.when_released = desliga_campainha
botao2.when_pressed = desliga_led
botao3.when_pressed = comeca_gravar
botao3.when_released = para_gravar
sensor.when_in_range = captura_tempo
sensor.when_out_of_range = envia_alerta

proximo_id_de_update = 0 
while True: 
    endereco = endereco_base + "/getUpdates"
    dados = {"offset": proximo_id_de_update} 
    resposta = get(endereco, json=dados)
    dicionario_da_resposta = resposta.json() 
    for resultado in dicionario_da_resposta["result"]: 
        mensagem = resultado["message"] 
        if "text" in mensagem: 
            texto = mensagem["text"]
            if texto == "Abrir":
                led1.on()
            elif texto == "Soar Alarme":
                campainha.beep(n=5, on_time = 0.1, off_time = 0.1)
            elif texto == "Ignorar":
                pass
            else:
                lcd.clear()
                lcd.message("Mensagem Recebida")
                campainha.beep(n=1, on_time = 0.1)
                sleep(0.5)
                lcd.clear()
                sleep(0.5)
                lcd.message("Mensagem Recebida")
                campainha.beep(n=1, on_time = 0.1)
                sleep(0.5)
                lcd.clear()
                sleep(0.5)
                conv = unidecode(texto)
                if len(conv) <= 16:
                    lcd.message(conv)
                else:
                    for i in range(len(conv)-15):
                        lcd.clear()
                        lcd.message(conv[i:i+16])
                        sleep(0.2)
                
        elif "voice" in mensagem: 
            id_do_arquivo = mensagem["voice"]["file_id"]
            endereco = endereco_base + "/getFile"
            dados = {"file_id": id_do_arquivo} 
            resposta = get(endereco, json=dados)
            dicionario = resposta.json()
            final_do_link = dicionario["result"]["file_path"]
            link_do_arquivo = "https://api.telegram.org/file/bot" + chave + "/" + final_do_link
            arquivo_de_destino = "meu_arquivo.ogg"
            urlretrieve(link_do_arquivo, arquivo_de_destino)
            player.loadfile(arquivo_de_destino)
            
        elif "photo" in mensagem: 
            foto_mais_resolucao = mensagem["photo"][-1] 
            id_do_arquivo = foto_mais_resolucao["file_id"] 
            # depois baixa o arquivo e faz algo com ele...
        proximo_id_de_update = resultado["update_id"] + 1
    sleep(1)
        
    
    
