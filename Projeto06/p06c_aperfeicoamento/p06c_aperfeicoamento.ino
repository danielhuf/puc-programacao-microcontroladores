#define USE_TIMER_1 true

#include <ShiftDisplay.h>
#include <GFButton.h>
#include <TimerInterrupt.h>

int contagem[] = {0, 0, 0, 0};
bool andamento[] = {false, false, false, false};
int indiceAtual = 0;

int campainha = 3;

int leds[] = {13, 12, 11, 10};

GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);

ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  for (int i = 0; i < 4; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], HIGH);
  }
  digitalWrite(leds[0], LOW);

  pinMode(campainha, OUTPUT);
  digitalWrite(campainha, HIGH);

  float contagemTraduzida = float(contagem[indiceAtual] / 60) + float(contagem[indiceAtual] % 60)/100;
  
  display.set(contagemTraduzida, 2, true);
  ITimer1.init();
  ITimer1.attachInterruptInterval(1000, contagemRegressiva);
  botao1.setPressHandler(aumentaContagem);
  botao2.setPressHandler(diminuiContagem);
  botao3.setPressHandler(regulaContagem);
}

void loop() {
  // put your main code here, to run repeatedly:
  botao1.process();
  botao2.process();
  botao3.process();

  float contagemTraduzida = float(contagem[indiceAtual] / 60) + float(contagem[indiceAtual] % 60)/100;
  
  display.set(contagemTraduzida, 2, true);
  display.changeDot(1, true);
  display.update();
}

void aumentaContagem() {
  contagem[indiceAtual] += 15;
}

void diminuiContagem() {
  contagem[indiceAtual] -= 15;
  if (contagem[indiceAtual] < 0) {
    contagem[indiceAtual] = 0;
  }
}

void regulaContagem() {
  if (andamento[indiceAtual] || !contagem[indiceAtual]) {
    digitalWrite(leds[indiceAtual], HIGH);
    ++indiceAtual %= 4;
    digitalWrite(leds[indiceAtual], LOW);
  }
  else {
    andamento[indiceAtual] = !andamento[indiceAtual];
  }
}

void contagemRegressiva() {
  
  digitalWrite(campainha, HIGH);
  for (int i = 0; i < 4; i++) {
    if (andamento[i]) {
      contagem[i]--;
      if (contagem[i] <= 0) {
        contagem[i] = 0;
        andamento[i] = false;
        digitalWrite(campainha, LOW);
      }
    }
  }
}
