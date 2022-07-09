// Neste playground 08 A, vamos trabalhar com os potenciômetros e com o joystick.
// Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


// Como sempre, a gente começa importando as bibliotecas e criando as variáveis globais.
#include <ShiftDisplay.h>
#include <GFButton.h>

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);

GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);

int potenciometro1 = A8;
int potenciometro2 = A9;
int analogicoX = A10;
int analogicoY = A11;

int leds[] = {13, 12, 11, 10};


// Usaremos esta variável para alternar a leitura analógica mostrada no display.
int leituraAtual = 1;
boolean mostrarEixoX = false;


void setup() {
  // É sempre bom inicializar a Serial, se precisar debugar alguma coisa.
  Serial.begin(9600);


  // Lembre sempre de colocar os LEDs como OUTPUT, senão eles não vão acender depois!
  for (int i = 0; i < 4; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], HIGH);
  }


  // Vamos usar os botões para alternar as leituras analógicas no display.
  botao1.setPressHandler(mostrarPotenciometro1);
  botao2.setPressHandler(mostrarPotenciometro2);
  botao3.setPressHandler(mostrarJoystick);
}


void mostrarPotenciometro1(GFButton &botao) {
  leituraAtual = 1;
}


void mostrarPotenciometro2(GFButton &botao) {
  leituraAtual = 2;
}


void mostrarJoystick(GFButton &botao) {
  leituraAtual = 3;
  mostrarEixoX = !mostrarEixoX;
}


void loop() {
  // Não esqueça de chamar a process dos botões!
  botao1.process();
  botao2.process();
  botao3.process();

  // Agora vamos fazer a escolha de leitura dos potenciômetros.
  if (leituraAtual == 1) {
    
    // Para o potenciômetro 1, vamos pegar a leitura direta e colocar no display.
    // A analogRead retorna um valor entre 0 e 1023.
    // Mas, na simulação e na vida real, é possível que não chegue certinho em 1023.
    int valorAnalogico1 = analogRead(potenciometro1);
    display.set(valorAnalogico1);
    
  }
  else if (leituraAtual == 2) {

    // Já para o potenciômetro 2, vamos mapear a leitura original para uma outra faixa.
    // Com a map, eu posso mapear o intervalo de 0 a 1023 para algo entre 100 e 200.
    int valorAnalogico2 = analogRead(potenciometro2);
    int valorMapeado2 = map(valorAnalogico2, 0, 1023, 100, 200);
    display.set(valorMapeado2);

    // COMPILE O CÓDIGO E RODE A SIMULAÇÃO.
    // APERTE OS BOTÕES 1 E 2, GIRE OS DOIS PRIMEIROS POTENCIÔMETROS E VEJA O DISPLAY.
    
  }
  else if (leituraAtual == 3) {

    // Aqui faremos a leitura dos dois eixos analógicos do joystick.
  
    // FAÇA A LEITURA DO EIXO X DO JOYSTICK
    // MAPEIE O VALOR DA FAIXA DE 0 A 1023 PARA -100 A 100
    // MOSTRE ISSO NO DISPLAY
    // COMPILE O CÓDIGO, RODE A SIMULAÇÃO E MEXA NO JOYSTICK NA HORIZONTAL.
    int valorAnalogicoX = analogRead(analogicoX);
    int valorMapeadoX = map(valorAnalogicoX, 0, 1023, -100, 100);

    // AGORA FAÇA A LEITURA DO EIXO Y DO JOYSTICK
    // MAPEIE TAMBÉM O VALOR DA FAIXA DE 0 A 1023 PARA -100 A 100.
    // MOSTRE ISSO NO DISPLAY.
    // COMPILE O CÓDIGO, RODE A SIMULAÇÃO E MEXA NO JOYSTICK NA VERTICAL.
    int valorAnalogicoY = analogRead(analogicoY);
    int valorMapeadoY = map(valorAnalogicoY, 0, 1023, -100, 100);

    // CRIE UMA VARIÁVEL BOOLEANA mostrarEixoX.
    // AO APERTAR O BOTÃO 3, ALTERNE ESSE BOOLEANO ENTRE TRUE E FALSE.
    // USE ESSE BOOLEANO PARA ESCOLHER QUAL DOS EIXOS MOSTRAR NO DISPLAY.
    if (mostrarEixoX) {
      display.set(valorMapeadoX);
    }
    else {
      display.set(valorMapeadoY);
    }

    // PERCEBA O ARRANJO DOS LEDS NO CIRCUITO.
    // ACENDA UM DOS LEDS DE ACORDO COM A POSIÇÃO DO JOYSTICK:
      // CASO OS VALORES MAPEADOS DE X E Y SEJAM MENORES QUE -50, ACENDA O LED 2 E APAGUE OS DEMAIS.
      // REPITA A MESMA LÓGICA PARA AS OUTRAS DIAGONAIS.
      // APAGUE TODOS OS LEDS CASO O JOYSTICK NÃO ESTEJA EM NENHUMA DAS DIAGONAIS.
    // NÃO ESQUEÇA DE APERTAR O BOTÃO 3 ANTES DE TESTAR!
    if (valorMapeadoX < -50 & valorMapeadoY > 50) {
      digitalWrite(leds[0], LOW);
      digitalWrite(leds[1], HIGH);
      digitalWrite(leds[2], HIGH);
      digitalWrite(leds[3], HIGH);
    }
    else if (valorMapeadoX > 50 & valorMapeadoY > 50) {
      digitalWrite(leds[0], HIGH);
      digitalWrite(leds[1], LOW);
      digitalWrite(leds[2], HIGH);
      digitalWrite(leds[3], HIGH);
    }
    else if (valorMapeadoX < -50 & valorMapeadoY < -50) {
      digitalWrite(leds[0], HIGH);
      digitalWrite(leds[1], HIGH);
      digitalWrite(leds[2], LOW);
      digitalWrite(leds[3], HIGH);
    }
    else if (valorMapeadoX > 50 & valorMapeadoY < -50) {
      digitalWrite(leds[0], HIGH);
      digitalWrite(leds[1], HIGH);
      digitalWrite(leds[2], HIGH);
      digitalWrite(leds[3], LOW);
    }
    else {
      digitalWrite(leds[0], HIGH);
      digitalWrite(leds[1], HIGH);
      digitalWrite(leds[2], HIGH);
      digitalWrite(leds[3], HIGH);
    }
  }

  display.update();
}
