# Neste playground, vamos trabalhar com um bot no Telegram.
# A configuração inicial é um pouco trabalhosa, mas você só precisa fazer 1 vez.
# Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


# Inicialização do simulador. Escreva todo o seu código dentro da main!
from extra.playground import rodar

@rodar
def main():
    
    # Começamos importando as bibliotecas, como sempre.
    from requests import get, post
    
    from gpiozero import LED, Button, Buzzer
    from Adafruit_CharLCD import Adafruit_CharLCD
    from time import sleep
    
    
    # Primeiro, siga o passo-a-passo do vídeo para criar um bot:
    # 1 - Baixe o aplicativo Telegram e crie uma conta lá.
    # 2 - Busque pelo BotFather e inicie uma conversa com ele.
    # 3 - Envie a mensagem /newbot e escolha o nome e o usuário do seu bot.
    # 4 - Copie a chave secreta para a variável abaixo (algo como "12345:ABCDEFGLK...")
    chave = "5177772037:AAGTaTpNuSj17Ef40unWlMShxcb3jaKvsOQ"
    
    
    # Aí a gente coloca a chave no endereço onde faremos as solicitações
    endereco_base = "https://api.telegram.org/bot" + chave
    
    
    # Podemos testar primeiro se a chave está ok fazendo um pedido para o /getMe
    # Rode o código e veja se a mensagem no Shell mostra os dados do seu bot
    endereco_dados_do_bot = endereco_base + "/getMe"

    print("Buscando dados sobre o bot...")
    resultado = get(endereco_dados_do_bot)
    print(resultado.text)
    
    
    # Agora vamos conversar com o bot
    # 5 - Abra o Telegram, busque o usuário do seu bot e inicie uma conversa com ele.
    # 6 - Envie uma ou mais mensagens quaisquer.
    # 7 - Abra o seu navegador e acesse http://api.telegram.org/botSUA_CHAVE_SECRETA/getUpdates
    # 8 - Copie o id do chat (procure por "chat": {"id":123456...}).
    id_da_conversa = "5271993060"
    
    
    # Pronto! Agora você pode enviar mensagens via programação!
    dados = {"chat_id": id_da_conversa, "text": "Mensagem enviada pelo Python!"}
    endereco_para_mensagem = endereco_base + "/sendMessage"
    
    # DESCOMENTE AS LINHAS ABAIXO PARA TESTAR, E DEPOIS COMENTE DE NOVO.
    
    #print("\nEnviando mensagem...")
    #resultado = post(endereco_para_mensagem, json=dados)
    #print(resultado.text)
    
    
    # Se você quiser enviar uma foto, é só abrir o arquivo e usar a sendPhoto.
    endereco_para_foto = endereco_base + "/sendPhoto"
    dados = {"chat_id": id_da_conversa}
    arquivo = {"photo": open("foto_telegram.jpg", "rb")} # foto de exemplo do Playground 04
    
    # DESCOMENTE AS LINHAS ABAIXO PARA TESTAR, E DEPOIS COMENTE DE NOVO.
    
    #print("\nEnviando foto...")
    #resultado = post(endereco_para_foto, data=dados, files=arquivo)
    #print(resultado.text)
    

    # Para obter as mensagens enviadas pelo usuário ao bot, usamos a getUpdates.
    # Na teoria, a gente usou o while True para ficar buscando mensagens continuamente.
    # Neste playground, vamos chamar só uma vez, para simplificar.
    proximo_id_de_update = 160649000 + 1
    endereco = endereco_base + "/getUpdates"
    dados = {"offset": proximo_id_de_update}
    
    # DESCOMENTE AS LINHAS ABAIXO PARA TESTAR, E DEPOIS COMENTE DE NOVO
    
    #print("\nBuscando novas mensagens...")
    #resposta = get(endereco, json=dados)
    #dicionario_da_resposta = resposta.json()
    #print(dicionario_da_resposta)


    # VERIFIQUE OS DADOS RETORNADOS E ENCONTRE O PRIMEIRO "update_id".
    # AGORA ATUALIZE A VARIÁVEL proximo_id_de_update ALI EM CIMA PARA ESSE VALOR + 1.
    # RODE NOVAMENTE O PROGRAMA E VEJA QUE O PRIMEIRO RESULTADO NÃO APARECE MAIS.
    # OBS: uma vez que você fornece um offset, as mensagens anteriores nunca mais serão retornadas.
    
    
    
    # EXPERIMENTE INTEGRAR O BOT COM OS DISPOSITIVOS DO SIMULADOR!
    # Sugestão 1: enviar uma mensagem ao apertar um botão.
    # Sugestão 2: usar o while True para tocar a campainha sempre que o usuário enviar uma mensagem pelo celular.
    
    botao1 = Button(11)
    botao2 = Button(12)
    botao3 = Button(13)
    botao4 = Button(14)
    
    def send_1():
        dados = {"chat_id": id_da_conversa, "text": "Botão 1 apertado!"}
        endereco_para_mensagem = endereco_base + "/sendMessage"
        resultado = post(endereco_para_mensagem, json=dados)
        
    def send_2():
        dados = {"chat_id": id_da_conversa, "text": "Botão 2 apertado!"}
        endereco_para_mensagem = endereco_base + "/sendMessage"
        resultado = post(endereco_para_mensagem, json=dados)

    def send_3():
        dados = {"chat_id": id_da_conversa, "text": "Botão 3 apertado!"}
        endereco_para_mensagem = endereco_base + "/sendMessage"
        resultado = post(endereco_para_mensagem, json=dados)
        
    def send_4():
        dados = {"chat_id": id_da_conversa, "text": "Botão 4 apertado!"}
        endereco_para_mensagem = endereco_base + "/sendMessage"
        resultado = post(endereco_para_mensagem, json=dados)
        
    botao1.when_pressed = send_1
    botao2.when_pressed = send_2
    botao3.when_pressed = send_3
    botao4.when_pressed = send_4
    
    buzzer = Buzzer(16)    
    proximo_id_de_update = 0
    
    while True:
        endereco = endereco_base + "/getUpdates"
        dados = {"offset": proximo_id_de_update}
        resposta = get(endereco, json=dados)
        dicionario_da_resposta = resposta.json()
        if dicionario_da_resposta['result'] != []:
            proximo_id_de_update = dicionario_da_resposta['result'][0]['update_id'] + 1
            buzzer.beep(n=1,on_time=0.5,off_time=0.5)
        sleep(0.1)
