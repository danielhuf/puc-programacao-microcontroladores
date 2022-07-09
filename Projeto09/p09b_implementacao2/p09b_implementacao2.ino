#include <GFButton.h>
#include <ShiftDisplay.h>

int estado = 0;
String estados[] = {"frente", "tras", "esquerda", "direita"};
ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);
GFButton botao1(A1);
GFButton botao2(A2);

int led1 = 13;
int led2 = 12;

void setup() {
  Serial1.begin(9600);
  display.set(estados[0]);
  botao1.setPressHandler(alternar_estado);
  botao2.setPressHandler(enviar_serial);
  botao2.setReleaseHandler(enviar_parar);
  pinMode(led1, OUTPUT);
  digitalWrite(led1, HIGH);
  pinMode(led2, OUTPUT);
  digitalWrite(led2, HIGH); 
}

void alternar_estado() {
  ++estado %= 4;
  display.set(estados[estado]);
}

void enviar_serial() {
  Serial1.println(estados[estado]);
}

void enviar_parar() {
  Serial1.println("parar");
}

void loop() {
  display.update();
  botao1.process();
  botao2.process();

  if (Serial1.available() > 0) {
    String texto = Serial1.readStringUntil('\n');
    texto.trim();
    if (texto.substring(0,1) == "0") {
      digitalWrite(led1, LOW);
    }else {
      digitalWrite(led1, HIGH);
    }
    if (texto.substring(2) == "0") {
      digitalWrite(led2, LOW);
    }else {
      digitalWrite(led2, HIGH);
    }
  }
}
