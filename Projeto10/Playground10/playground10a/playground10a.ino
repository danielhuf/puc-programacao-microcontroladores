// Neste playground 10 A, vamos trabalhar com desenhos no shield touch.
// Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.

// Começamos importando as bibliotecas, como sempre.
// Como o Simulide não tem o mesmo shield do laboratório, usaremos algumas bibliotecas alternativas.

// COPIE AS PASTAS DO DIRETÓRIO bibliotecasExtras PARA A SUA PASTA Documentos/Arduino/libraries


#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
#include <JKSButton.h>
#include <TouchScreen.h>


// Agora podemos criar as variáveis globais.
Adafruit_ILI9341 tela = Adafruit_ILI9341(8, 10, 9);
JKSButton botao1, botao2;
TouchScreen touch(25, 26, 27, 9, 300);
int r = 5;

void setup(void) {
  
  // Inicialização da comunicação serial, que é sempre bom ter.
  Serial.begin(9600);


  // A tela gráfica é inicializada com estes dois comandos.
  // Essa etapa pode demorar um pouquinho.
  // ATENÇÃO: perceba que o prefixo das cores é diferente do que vimos na teoria,
  tela.begin();
  tela.fillScreen(ILI9341_BLACK);

  
  // Agora podemos desenhar à vontade!
  // Lembre-se que a tela tem dimensões 240 x 320.
  
  // Vamos começar com algumas retas.
  // Parâmetros: x1, y1, x2, y2, cor.
  tela.drawLine(170, 20, 220, 40, ILI9341_PINK);
  tela.drawLine(130, 50, 200, 50, ILI9341_LIGHTGREY);


  // Formas como o círculos podem ser desenhadas com preenchimento e/ou contorno.
  // Lembrando que o contorno deve ser chamado depois do preenchimento!
  // Parâmetros: x (centro), y, raio, cor.
  tela.fillCircle(120, 100, 20, ILI9341_PURPLE);
  tela.drawCircle(120, 100, 20, ILI9341_WHITE);


  // Retângulos seguem a mesma ideia.
  // Parâmetros: x (canto esquerdo superior), y, comprimento, altura, cor.
  tela.fillRect(30, 110, 50, 90, ILI9341_RED);
  tela.drawRect(30, 110, 50, 90, ILI9341_GREEN);


  // Idem para triângulos.
  // Parâmetros: x1, y1, x2, y2, x3, y3, cor.
  tela.fillTriangle(190, 100, 190, 140, 220, 140, ILI9341_YELLOW);


  // EXPORTE O BINÁRIO COMPILADO, ATUALIZE O FIRMWARE NO SIMULIDE E VEJA O RESULTADO DOS DESENHOS.
  

  // CRIE 2 PEQUENAS RETAS VERMELHAS SE CRUZANDO NO CENTRO DA TELA, FORMANDO UM X.
  tela.drawLine(100, 140, 140, 180, ILI9341_RED);
  tela.drawLine(100, 180, 140, 140, ILI9341_RED);
  


  // CRIE UM CIRCULO DE RAIO 40 ENCOSTADO NAS LATERAIS ESQUERDA E INFERIOR.
  // COLOQUE O PREENCHIMENTO COM AZUL E A BORDA AMARELA.
  tela.fillCircle(40, 280, 40, ILI9341_BLUE);
  tela.drawCircle(40, 280, 40, ILI9341_YELLOW);



  // CRIE UM PADRÃO DE 10 RETÂNGULOS DESLOCADOS, SÓ COM CONTORNOS, CONFORME ILUSTRADO ABAIXO.
  // ESCOLHA A POSIÇÃO, DIMENSÕES E COR QUE VOCÊ QUISER.
  // DICA: USE 1 ÚNICO FOR PARA VARIAR A COORDENADA X E Y AO MESMO TEMPO.

  //   ┌-------------┐
  //   │ ┌-----------|-┐
  //   | | ┌---------|-|-┐
  //   | | |         | | |   -->  10 desses em sequência
  //   └-|-|---------┘-| |
  //     └-|-----------┘ |
  //       └-------------┘

  for (int i=0; i<10; i++)
    tela.drawRect(80+i*8, 220+i*4, 16, 8, ILI9341_WHITE);
  

  // Por fim, vamos criar um botão virtual desenhado na tela.
  botao1.init(&tela, &touch, 190, 200, 70, 20, ILI9341_WHITE, ILI9341_BLUE, ILI9341_WHITE, "Serial", 1);

  // Ao tocar nesse botão, chamaremos uma função que imprima algo na Serial.
  // Veja que o esquema aqui é igual ao da GFButton, incluindo o .process lá na loop.
  // Como o SimulIDE não tem suporte ainda ao touch, usaremos os botões físicos na parte de baixo para simular o toque.
  botao1.setPressHandler(imprimirNaSerial);


  // COMPILE, ATUALIZE O FIRMWARE E ABRA O MONITOR SERIAL.
  // SIMULE O TOQUE NO BOTÃO VIRTUAL CLICANDO NO BOTÃO 1 ABAIXO DO ARDUINO.


  // CRIE UM SEGUNDO BOTÃO ABAIXO DO ANTERIOR.
  // AO CLICAR NELE, DESENHE UMA CIRCUNFERÊNCIA DE RAIO 10 NA PARTE INFERIOR À DIREITA DA TELA.
  // AO CLICAR NOVAMENTE, APAGUE O DESENHO ANTERIOR, ADICIONE 5 NO RAIO E DESENHE NOVAMENTE.
  // DICA 1: NÃO ESQUEÇA DE CHAMAR A .process() NO LOOP!
  // DICA 2: VOCÊ PODE DESENHAR UMA CIRCUNFERÊNCIA PRETA EM CIMA DA ANTERIOR PARA APAGÁ-LA.
  botao2.init(&tela, &touch, 190, 230, 70, 20, ILI9341_WHITE, ILI9341_BLUE, ILI9341_WHITE, "Circ", 1);
  botao2.setPressHandler(desenhaCircunferencia);
  
}
 
void loop() {

  // A JKSButton foi inspirada na GFButton, e também precisa ser monitorada com o process.
  botao1.process();
  botao2.process();
  
}


void imprimirNaSerial(JKSButton& botao) {
  Serial.println("Clicou no botao desenhado na tela.");
}

void desenhaCircunferencia(JKSButton& botao) {
  tela.fillCircle(210, 290, r, ILI9341_BLACK);
  r += 5;
  tela.fillCircle(210, 290, r, ILI9341_RED);
}
