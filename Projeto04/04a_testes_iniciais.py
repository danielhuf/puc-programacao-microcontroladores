# importação de bibliotecas
from gpiozero import LED, Button,Buzzer
from Adafruit_CharLCD import Adafruit_CharLCD
from requests import get, post
from time import sleep
from os import system

# parâmetros iniciais do Telegram
chave = "5177772037:AAGTaTpNuSj17Ef40unWlMShxcb3jaKvsOQ" 
id_da_conversa = "5271993060"
global endereco_base
endereco_base = "https://api.telegram.org/bot" + chave
endereco_dados_do_bot = endereco_base + "/getMe"
led1 = LED(21)
botao1 = Button(11)
botao2 = Button(12)
bota3 = Button(13)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
campainha = Buzzer(16)

# definição de funções
def gravar():
    lcd.clear()
    lcd.message("Gravando...")
    system("arecord --duration 5 --format cd audio.wav")
    lcd.clear()
    
def tira_5_fotos():
    for i in range(5):
        system("fswebcam --resolution 640x480 --skip 10 foto" + str(i+1) + ".jpg")
        led1.blink(n=1, on_time=0.1, off_time=0.1)
        sleep(2)
    print('Fotos tiradas')
    
def envia_msg():
    global endereco_base
    dados = {"chat_id": id_da_conversa, "text": "Hello World"}
    endereco_para_mensagem = endereco_base + "/sendMessage"    
    
    print("\nEnviando mensagem...")
    resultado = post(endereco_para_mensagem, json=dados)
    print(resultado.text)
    
botao1.when_pressed = gravar
botao2.when_pressed = tira_5_fotos
bota3.when_pressed = envia_msg





