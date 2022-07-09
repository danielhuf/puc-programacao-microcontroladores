#define USE_TIMER_1 true

#include <ShiftDisplay.h>
#include <GFButton.h>
#include <TimerInterrupt.h>

int contagem = 0;
float contagemTraduzida = 0;
int campainha = 3;
bool andamento = false;

GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);

ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(campainha, OUTPUT);
  digitalWrite(campainha, HIGH);
  
  display.set(contagemTraduzida, 2, true);
  ITimer1.init();
  ITimer1.attachInterruptInterval(1000, contagemRegressiva);
  botao1.setPressHandler(aumentaContagem);
  botao2.setPressHandler(diminuiContagem);
  botao3.setPressHandler(iniciaContagem);
}

void loop() {
  // put your main code here, to run repeatedly:
  botao1.process();
  botao2.process();
  botao3.process();

  contagemTraduzida = float(contagem / 60) + float(contagem % 60)/100;
  display.set(contagemTraduzida, 2, true);
  display.changeDot(1, true);
  display.update();
}

void aumentaContagem() {
  contagem += 15;
}

void diminuiContagem() {
  contagem -= 15;
  if (contagem < 0) {
    contagem = 0;
  }
}

void iniciaContagem() {
  andamento = !andamento;
}

void contagemRegressiva() {
  
  digitalWrite(campainha, HIGH);
  if (andamento) {
    contagem--;
    if (contagem<=0) {
      contagem = 0;
      andamento = false;
      digitalWrite(campainha, LOW);
    }
  }
}
