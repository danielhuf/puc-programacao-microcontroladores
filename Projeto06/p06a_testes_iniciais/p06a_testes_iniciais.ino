#define USE_TIMER_1 true

#include <ShiftDisplay.h>
#include <GFButton.h>
#include <TimerInterrupt.h>

int led1 = 13;
int led2 = 12;

GFButton botao2(A2);
GFButton botao3(A3);

bool led2aceso = false;

int contLed3 = 0;

ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  pinMode(led1, OUTPUT);
  digitalWrite(led1, LOW);

  pinMode(led2, OUTPUT);
  digitalWrite(led2, HIGH);

  display.set(-4.12, 2);
  display.show(2000);

  ITimer1.init();
  ITimer1.attachInterruptInterval(2000, imprimeCont);

  botao2.setPressHandler(checaLed2);
  botao3.setPressHandler(aumentaContLed3);
}

void loop() {
  // put your main code here, to run repeatedly:
  botao2.process();
  botao3.process();

  display.set(contLed3);
  display.update();
}

void checaLed2(GFButton& botaoDoEvento) {
  if (led2aceso) {
    digitalWrite(led2, HIGH);
  }
  else {
    digitalWrite(led2, LOW);
  }
  led2aceso = !led2aceso;
}

void aumentaContLed3(GFButton& botaoDoEvento) {
  contLed3++;
}

void imprimeCont() {
  Serial.println(contLed3);
}
