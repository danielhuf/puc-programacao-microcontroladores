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
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
campainha = Buzzer(16)

# definição de funções
def desliga_led():
    led1.off()
    
def liga_campainha():
    campainha.on()

def desliga_campainha():
    global endereco_base
    campainha.off()
    
    dados = {"chat_id": id_da_conversa, "text": "Alguém está na porta!"}
    endereco_para_mensagem = endereco_base + "/sendMessage"    
    
    print("\nEnviando mensagem...")
    resultado = post(endereco_para_mensagem, json=dados)
    print(resultado.text)
    system("fswebcam --resolution 640x480 --skip 10 foto.jpg")
    arquivo  = {"photo": open("foto.jpg", "rb")}
    endereco_para_foto = endereco_base + "/sendPhoto"
    dados = {"chat_id": id_da_conversa}
    
    print("\nEnviando foto...")
    resultado = post(endereco_para_foto, data=dados, files=arquivo)
    print(resultado.text)
    
botao1.when_pressed = liga_campainha
botao1.when_released = desliga_campainha
botao2.when_pressed = desliga_led
    
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
            elif texto == "Alarme":
                campainha.beep(n=5, on_time = 0.1, off_time = 0.1)
        elif "voice" in mensagem: 
            id_do_arquivo = mensagem["voice"]["file_id"] 
            # depois baixa o arquivo e faz algo com ele...
        elif "photo" in mensagem: 
            foto_mais_resolucao = mensagem["photo"][-1] 
            id_do_arquivo = foto_mais_resolucao["file_id"] 
            # depois baixa o arquivo e faz algo com ele...
        proximo_id_de_update = resultado["update_id"] + 1
    sleep(1)
        
    
    









