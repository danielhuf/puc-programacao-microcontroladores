# Neste playground, vamos trabalhar com o IFTTT.
# Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


# Inicialização do simulador. Escreva todo o seu código dentro da main!
from extra.playground import rodar

@rodar
def main():
    
    # Começamos importando as bibliotecas, como sempre.
    from requests import post
    from flask import Flask
    
    from gpiozero import LED, Button, DistanceSensor, LightSensor, Buzzer
    from Adafruit_CharLCD import Adafruit_CharLCD


    # Antes de começar a trabalhar com o IFTTT, você precisa criar um conta lá.
    # Baixe também o aplicativo dele no seu celular.
    # Se não tiver feito isso ainda, acesse o endereço ifttt.com (com 3 Ts).
    
    
    # Depois de criar uma conta, vá no site e crie um applet novo clicando em Create.
    # Na etapa "If This", busque e selecione "Webhooks", e chame o evento de "playground".
    # Na etapa "Then That", busque e selecione "Notifications", e escreva uma mensagem qualquer.
    # Não esqueça de clicar em Continue e depois em Finish.
    
    
    # Agora vamos chamar esse evento, gerando uma notificação no seu celular.
    # Para isso, precisamos da chave secreta, que nem fizemos no Telegram.
    # Acesse https://ifttt.com/services/maker_webhooks/settings no seu navegador.
    # A chave está no final do URL, depois do /use/. Copie-a e cole na variável abaixo.
    chave = "cOsV4PelmB1EWsDoCKeATe"
    
    
    # Agora podemos montar o endereço relativo esse applet.
    evento = "playground"
    endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/"  + chave
    
    
    # Agora só precisamos fazer um post para esse endereço.
    # Se tudo der certo, você receberá uma notificação do app IFTTT.
    # ATENÇÃO: não esqueça de instalar o app no seu celular e de entrar na sua conta!
    
    
    # DESCOMENTE AS LINHAS ABAIXO PARA CHAMAR O APPLET.
    # DEPOIS DE TESTAR, COMENTE NOVAMENTE.
    
    #resultado = post(endereco)
    #print("\n", resultado.text, "\n\n")
    
    
    # Agora vamos passar um parâmetro para o IFFT personalizar a mensagem do alerta.
    # Volte para o site, vá em My Applets, selecione o seu applet e clique em Settings.
    # Clique em Edit na parte do "Then".
    # Mude a frase para "Meu nome é ", clique em Add Ingredient e selecione Value1.
    # A frase ficará "Meu nome é {{Value1}}".
    # Clique em Update Action e depois em Update.
    
    
    # Agora vamos passar um dado para o Value1 no post.
    # Perceba que o "value1" aqui tem "v" minúsculo, ao contrário do texto no site.
    dados = {"value1": "Dani Huf"}
    
    
    # DESCOMENTE AS LINHAS ABAIXO PARA CHAMAR O APPLET.
    # DEPOIS DE TESTAR, COMENTE NOVAMENTE.
    
    #resultado = post(endereco, json=dados)
    #print("\n", resultado.text, "\n\n")
    
    
    # MUDE A VARIÁVEL dados, COLOCANDO O SEU NOME DEPOIS DO value1, E RODE NOVAMENTE.
    
    
    # Esse value1 poderia ser algum dado dos sensores, para fazer algum tipo de automação residencial.
    # Mas agora vamos testar o IFTTT no sentido inverso, recebendo um evento.
    
    
    # Rode o Ngrok no seu computador.
    #  - Windows: abra o arquivo rodar_ngrok.bat. Se aparecer um alerta, clique em More Info e Run Anyway.
    #  - Mac: clique no arquivo rodar_ngrok.command com o botão direito > Abrir.
    # Volte no site do IFTTT e crie um outro applet clicando em Create.
    # Na etapa "If This", busque e selecione "Google Drive", e deixe o campo Drive Folder Path em branco.
    # Na etapa "Then That", busque e selecione "Webhooks".
    # Copie e cole no campo URL o endereço gerado pelo NGrok, e adicione no final /novoDocumento/{{Filename}}
    # ATENÇÃO: verifique se não tem nenhum espaço em branco no endereço do campo.
    # Ignore os outros campos. Clique em Continue e depois em Finish.
    

    # Agora iniciamos um servidor Flask.
    app = Flask(__name__)


    # Esta página será chamada pelo IFTTT, recebendo o nome de um arquivo.
    # Arraste um arquivo qualquer para a pasta raiz do seu Google Drive, enquanto este programa estiver rodando.
    # Observe a mensagem impressa no Shell do Thonny.
    @app.route("/novoDocumento/<string:nome>")
    def novoDocumento(nome):
        
        print("Novo documento adicionado no Google Drive: " + nome)
        
        return "Texto qualquer, porque quem vai acessar esta página é o IFTTT."



    # EXPERIMENTE CRIAR OUTROS APPLET NO IFTTT!
    # OBS: A CONTA GRATUITA DO IFTTT PERMITE APENAS 3 APPLETS. REMOVA OS ANTIGOS SE NECESSÁRIO. 
    # Sugestão 1: ao apertar um dos botões, envie uma mensagem para o seu email com o dado do sensor de luz.
    def enviar_email():
        chave = "cOsV4PelmB1EWsDoCKeATe"
        evento = "alerta"
        endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/"  + chave
        dados = {"value1": "Valor do sensor de luz: {:.2f}".format(sensor_de_luz.value)}
        resultado = post(endereco, json=dados)
        print("\n", resultado.text, "\n\n")
        
    sensor_de_luz = LightSensor(8)
    botao1 = Button(11)
    
    botao1.when_pressed = enviar_email
    
    
    # Sugestão 2: faça com que a campainha toque brevemente quando você postar algo no Instagram ou Facebook.
    @app.route("/novoPost")
    def novoPost():
        
        print("Campainha acionada!")
        campainha.beep(n=3, on_time=0.5, off_time=0.5)
        
        return "Texto qualquer, porque quem vai acessar esta página é o IFTTT."
    
    campainha = Buzzer(16)

    # Não esqueça de dar run no servidor aqui no final!
    app.run(port=5000)


    # Não escreva nenhum código depois do run!
    # Ele é tipo um while True que segura o programa, então nada depois dele vai rodar.