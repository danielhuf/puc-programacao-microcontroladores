from serial import Serial
from threading import Thread, Timer
from extra.tello import Tello
from time import sleep
from cv2 import *
from traceback import format_exc
    
def serial():
    while True:
        if meu_serial != None:
            texto_recebido = meu_serial.readline().decode().strip()
            if texto_recebido != "":
                print(texto_recebido)
                # ESCREVA AQUI O SEU CÓDIGO DA SERIAL!
                if texto_recebido == "decolar":
                    drone.takeoff()
                elif texto_recebido == "pousar":
                    drone.land()
                elif texto_recebido == "esquerda":
                    drone.rc(0, 0, 0, 40)
                elif texto_recebido == "direita":
                    drone.rc(0, 0, 0, -40)
                elif texto_recebido == "frente":
                    drone.rc(0, 40, 0, 0)
                elif texto_recebido == "parar":
                    drone.rc(0, 0, 0, 0)
            
    sleep(0.1)
    

# CASO A SERIAL NÃO FUNCIONE, COMENTE A LINHA ABAIXO E DESCOMENTE A SEGUINTE

meu_serial = Serial("COM3", baudrate=9600, timeout=0.1)
#meu_serial = None

print("[INFO] Serial: ok")

thread = Thread(target=serial)
thread.daemon = True
thread.start()  

#drone = Tello("TELLO-C7AC08", test_mode=True)
drone = Tello("TELLO-D023AE", test_mode=False)
drone.inicia_cmds()
print("[INFO] Drone pronto")


def imprime_e_envia_coordenadas():

  # ESCREVA AQUI O CÓDIGO DO TIMER RECORRENTE
  x = dados[0] * (200/comp_imagem)
  y = dados[1] * (150/alt_imagem)
  comp = dados[2] * (200/comp_imagem)
  alt = dados[3] * (150/alt_imagem)
  msg = "retangulo " + str(int(x)).zfill(3) + " " + str(int(y)).zfill(3) + " " + str(int(comp)).zfill(3) + " " + str(int(alt)).zfill(3)
  print(msg)
  meu_serial.write( msg.encode("UTF-8") )
  
  timer = Timer(3, imprime_e_envia_coordenadas)
  timer.start()
   

imagem = drone.current_image
alt_imagem = imagem.shape[0]
comp_imagem = imagem.shape[1]
dados = [0, 0, 0, 0]
imprime_e_envia_coordenadas()

try:
  while True:

    # COLOQUE AQUI O CÓDIGO DO WHILE DA IMPLEMENTACAO
    # A linha abaixo já faz o papel do VideoCapture e do stream.read
    imagem = drone.current_image
  
    # COLOQUE AQUI O CÓDIGO DO OPENCV
    
    imagem_hsv = cvtColor(imagem, COLOR_BGR2HSV)
    
    laranja_escuro = (0, 100, 60) # valores no espaço HSV
    laranja_claro = (20, 255, 255) # valores no espaço HSV
        
    mascara = inRange(imagem_hsv, laranja_escuro, laranja_claro)

    contornos,_ = findContours(mascara, RETR_TREE, CHAIN_APPROX_SIMPLE)
    m_area = 0
    
    for contorno in contornos:
        x, y, comprimento, altura = boundingRect(contorno)
        if comprimento*altura > m_area:
            m_area = comprimento*altura
            dados = [x,y,comprimento,altura]
    if m_area > 2000:
        rectangle(imagem, pt1=(dados[0],dados[1]), pt2=(dados[0]+dados[2], dados[1]+dados[3]), color=(0,255,0), thickness=3);

    imshow("Minha Janela", imagem)
    if waitKey(1) & 0xFF == ord("q"):
        break
        
except:
  if meu_serial != None:
    meu_serial.close()
  
  print("FIM!")
  print(format_exc())
  drone.land()
   