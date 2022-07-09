from turtle import *

# Parte 1: desenhe o retângulo no topo
penup()
goto(-300, 350)
pendown()
for i in range(0, 2):
    forward(200)
    left(90)
    forward(100)
    left(90)


# Parte 2: desenhe o triângulo equilátero à direita
penup()
goto(100, 0)
pendown()
for i in range (0, 3):
    forward(100) # draw base
    left(120)
    
    
# Parte 3: desenhe o círculo na parte debaixo
penup()
goto(-250, -350)
pendown()
r = 50
circle(r)


# Parte 4: desenhe a espiral na esquerda
penup()
goto(-250, 0)
pendown()
for i in range(100):
    forward(i/5)
    right(10)


# Parte 5: ao clicar em um ponto da tela, desenhe um texto com o valor das coordenadas x e y
def imprime_coordenadas(x, y):
    penup()
    goto(x, y)
    pendown()
    write("x = " + str(x) + " y = " + str(y))
    
onscreenclick(imprime_coordenadas)

# Mantém a janela do Turtle aberta
mainloop()