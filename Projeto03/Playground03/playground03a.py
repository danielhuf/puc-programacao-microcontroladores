# Neste playground 03 A, vamos trabalhar com data/hora, campainha e sensor de distância.
# Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


# Inicialização do simulador. Escreva todo o seu código dentro da main!
from extra.playground import rodar

@rodar
def main():
    
    # Começamos importando as bibliotecas, como sempre.
    from datetime import datetime, timedelta
    
    from gpiozero import LED, Button, Buzzer, DistanceSensor
    from Adafruit_CharLCD import Adafruit_CharLCD
    from time import sleep
    
    
    # Vamos começar com a parte de data/hora.
    # Eu posso criar uma data/hora atual ou num momento específico.
    agora = datetime.now()
    
    descobrimento_do_brasil = datetime(1500, 4, 22)  # ano, mês e dia (à meia-noite)
    pouso_em_marte = datetime(2021, 2, 18, 5, 55, 0) # ano, mês, dia, hora, minuto e segundo
    
    
    # Se eu passar a data/hora direto para o print, não fica muito bonito.
    print("Data/hora do pouso sem formatação:", pouso_em_marte)
    
    
    # Mas eu posso usar a strftime para formatar direitinho
    # Cada % ali diz respeito a uma parte da data (dia, mês, ano, etc)
    print("Data/hora do pouso formatada:", pouso_em_marte.strftime("%d/%m/%Y %H:%M:%S"))
    
    
    # Também posso passar o texto todo na strftime
    print(descobrimento_do_brasil.strftime("O Brasil foi descoberto em %d/%m/%Y"))
    
    
    
    # IMPRIMA A DATA/HORA ATUAL NO FORMATO "São __:__ do dia __/__/_____" 
    agora = datetime.now()
    print(agora.strftime("São %H:%M do dia %d/%m/%Y"))
    
    
    # Dá para adicionar ou subtrair um intervalo de tempo nas datas.
    # Para criar esse intervalo, usamos a timedelta com a variação de tempo desejada.
    # Dá para usar seconds, minutes, hours, days, weeks (não tem para mês e ano).
    ultimo_dia_sem_europeus = descobrimento_do_brasil - timedelta(days=1)
    dez_minutos_depois_do_pouso = pouso_em_marte + timedelta(minutes=10)
    
    
    
    # OBTENHA QUAL SERÁ A DATA DAQUI A 40 SEMANAS
    # EM SEGUIDA, IMPRIMA ESSA DATA NO SHELL COM A MENSAGEM "Parabéns! Você terá um bebê no dia __/__!"
    agora = datetime.now()
    mais_40 = agora + timedelta(weeks=40)
    print(mais_40.strftime("Parabéns! Você terá um bebê no dia %d/%m"))
    
    
    # Agora vamos passar para a parte de hardware.
    # Assim como o LED, a campainha pode ser ligada e desligada
    campainha = Buzzer(16)
    
    
    # DESCOMENTE AS LINHAS ABAIXO PARA VER A CAMPAINHA LIGAR E DESLIGAR.
    # DEPOIS DE TESTAR, COMENTE NOVAMENTE.

    campainha.on()
    sleep(1)
    campainha.off()
    
    
    # E eu posso ficar ligando e desligando sem usar a sleep (que trava o programa).
    # Similar ao método blink do LED, a campainha tem o comando beep.
    
    
    # DESCOMENTE AS LINHAS ABAIXO PARA OUVIR O BEEP.
    # DEPOIS DE TESTAR, COMENTE NOVAMENTE.
    
    campainha.beep(n=4, on_time=0.3, off_time=0.7)
    
    
    
    # O segundo e último dispositivo de hoje é o sensor de distância.
    # A gente inicializa com as duas portas onde ele está conectado.
    sensor_de_distancia = DistanceSensor(trigger=17, echo=18)
    
    
    # Para obter a distância de um objeto até ele, basta acessar a propriedade distance.
    # ATENÇÃO: esse valor vem sempre em metros!
    distancia_em_metros = sensor_de_distancia.distance
    
    
    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    
    
    # CONVERTA A DISTÂNCIA PARA CENTÍMETROS E MOSTRE-A NO LCD!
    # OBS: NÃO ESQUEÇA DE TRANSFORMAR EM STRING!
    distancia_em_cm = distancia_em_metros * 100
    lcd.clear() 
    lcd.message(str(distancia_em_cm) + " cm")
    
    
    # A qualquer momento do programa, você poderia acessar essa propriedade distance.
    # Mas em vez de ficar monitorando toda hora, o sensor pode avisar quando algo se aproximou demais.
    # A ideia é a mesma do botão: criar uma função e associá-la à propriedade when_in_range
    def algo_se_aproximou():
        
        # Daqui a pouco, você vai colocar mais código aqui na função.
        
        
        print("Está perto!")
        
        
    sensor_de_distancia.when_in_range = algo_se_aproximou
    
    
    # Só tem um detalhe extra: você precisa definir o limiar do que seria algo "próximo".
    # De novo, vale lembrar que a distância é sempre em METROS! 0.12m = 12cm.
    sensor_de_distancia.threshold = 0.12
    
    
    
    # MUDE O LIMIAR DO SENSOR PARA 7 CM.
    # CASO O SENSOR DETECTE PROXIMIDADE, BIPE A CAMPAINHA CONTINUAMENTE (SEM N) COM UM TEMPO CURTO DE ON E OFF
    # CASO O SENSOR DETECTE DISTÂNCIA, DESLIGUE A CAMPAINHA.
    sensor_de_distancia.threshold = 0.07

    def proximidade():
        campainha.beep(on_time=0.3, off_time=0.3)
    
    def distancia():
        campainha.off()

    sensor_de_distancia.when_in_range = proximidade
    sensor_de_distancia.when_out_of_range = distancia
    
    while True:
        sleep(0.1)