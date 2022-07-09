from cv2 import *
stream = VideoCapture(0)

while True:
    _, imagem = stream.read()
    
    
    #imagem_cinza = cvtColor(imagem, COLOR_BGR2GRAY)
    #imagem_cinza = cvtColor(imagem_cinza, COLOR_GRAY2BGR)
    
    imagem_hsv = cvtColor(imagem, COLOR_BGR2HSV)
    
    laranja_escuro = (0, 100, 60) # valores no espaço HSV
    laranja_claro = (20, 255, 255) # valores no espaço HSV
        
    mascara = inRange(imagem_hsv, laranja_escuro, laranja_claro)
    
    mascara2 = bitwise_not(mascara)
    imagem2 = bitwise_and(imagem, imagem, mask=mascara2)
    
    imagem_cinza = cvtColor(imagem2, COLOR_BGR2GRAY)
    imagem_cinza = cvtColor(imagem_cinza, COLOR_GRAY2BGR)
    
    imagem_laranja = bitwise_and(imagem, imagem, mask=mascara)
    
    imagem3 = imagem_laranja + imagem_cinza
    
    putText(imagem3, "Beyonce", (200,50), color=(100,140,225), 
thickness=3, fontFace=FONT_HERSHEY_SIMPLEX, fontScale=2)

    
    imshow("Minha Janela", imagem3)
    if waitKey(1) & 0xFF == ord("q"):
        break


stream.release()
destroyAllWindows()