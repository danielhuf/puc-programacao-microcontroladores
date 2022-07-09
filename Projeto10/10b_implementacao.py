from extra.tello import Tello
from time import sleep
from cv2 import *
from traceback import format_exc

    
drone = Tello("TELLO-C7AC08", test_mode=True)
#drone = Tello("TELLO-D023AE", test_mode=True)
drone.inicia_cmds()
print("[INFO] - Drone pronto")

while True:
    
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
            dados = [x,y,x+comprimento,y+altura]
    if m_area > 2000:
        rectangle(imagem, pt1=(dados[0],dados[1]), pt2=(dados[2],dados[3]), color=(0,255,0), thickness=3);

    imshow("Minha Janela", imagem)
    if waitKey(1) & 0xFF == ord("q"):
        break
