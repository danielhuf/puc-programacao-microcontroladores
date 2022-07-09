from json import load
from turtle import *

# Copie as funções da Implementação aqui
def desenha_retangulo(x, y, comprimento, altura, cor):
    penup()
    goto(x, y)
    pendown()
    fillcolor(cor)
    begin_fill()
    for i in range(0, 2):
        forward(comprimento)
        right(90)
        forward(altura)
        right(90)
    end_fill()
    return


def desenha_circulo(x, y, raio, cor):
    penup()
    goto(x, y-raio)
    pendown()
    fillcolor(cor)
    begin_fill()
    circle(raio)
    end_fill()
    return


def desenha_poligono(lista_pontos, cor):
    penup()
    goto(lista_pontos[0]['x'], lista_pontos[0]['y'])
    pendown()
    fillcolor(cor)
    begin_fill()
    for cord in lista_pontos[1:]:
        goto(cord['x'], cord['y'])
    goto(lista_pontos[0]['x'], lista_pontos[0]['y'])
    end_fill()
    return

# Implemente a função abaixo
def desenha_bandeira(dicionario_do_pais):
    for el in dicionario_do_pais['elementos']:
        if el['tipo'] == 'retângulo':
            desenha_retangulo(el['x'], el['y'], el['comprimento'], el['altura'], el['cor'])
        elif el['tipo'] == 'círculo':
            desenha_circulo(el['x'], el['y'], el['raio'], el['cor'])
        else:
            desenha_poligono(el['pontos'], el['cor'])
    return

dicionarios_de_paises = load(open('paises.json', encoding="UTF-8"))
desenha_bandeira(dicionarios_de_paises[0])


# Ao clicar na tela, solicitar o nome de um país, busque-o na lista de dicionários de países e desenhe-o.
def imprime_coordenadas(x, y):
    pais = textinput("Digite o nome de um país", "País")
    for dic in dicionarios_de_paises:
        if pais == dic['nome']:
            desenha_bandeira(dic)
            break
        
onscreenclick(imprime_coordenadas)


# DESAFIO EXTRA: adicione a bandeira da África do Sul no arquivo JSON e teste seu desenho.
# Bandeira adicionada no JSON!


# Mantém a janela do Turtle aberta
mainloop()