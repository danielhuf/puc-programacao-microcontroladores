#include <GFButton.h>
#include <ShiftDisplay.h>

int estado = 0;
String estados[] = {"frente", "tras", "esquerda", "direita"};
ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);
GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);

boolean Auto = false;

unsigned long atual = 0;
unsigned long anterior = 0;
unsigned long anterior2 = 0;


int led1 = 13;
int led2 = 12;

void setup() {
  Serial1.begin(9600);
  Serial1.setTimeout(9600);
  display.set(estados[0]);
  botao1.setPressHandler(alternar_estado);
  botao2.setPressHandler(enviar_serial);
  botao2.setReleaseHandler(enviar_parar);
  botao3.setPressHandler(alternar_auto);
  pinMode(led1, OUTPUT);
  digitalWrite(led1, HIGH);
  pinMode(led2, OUTPUT);
  digitalWrite(led2, HIGH); 
}

void alternar_estado() {
  ++estado %= 4;
  if (!Auto){
    display.set(estados[estado]);
  }
}

void enviar_serial() {
  if (!Auto){
    Serial1.println(estados[estado]);
  }
}

void enviar_parar() {
  Serial1.println("parar");
}

void alternar_auto() {
  Auto = !Auto;
  anterior2 = atual;
  if (Auto){
    display.set("auto");
  }
  else {
    display.set(estados[estado]);
  }
}

void loop() {
  display.update();
  botao1.process();
  botao2.process();
  botao3.process();

  atual = millis();
  if (atual >= anterior + 50){
    if(Auto){
      Serial1.println("auto");
      if (atual >= anterior2 + 5000){
        Auto = false;
        display.set(estados[estado]);
      }
    }
    else{
      if (botao2.isPressed()){
        Serial1.println(estados[estado]);
      }
      else{
        Serial1.println("parar");
      }
    }
    anterior = atual;
  }

  if (Serial1.available() > 0) {
    String texto = Serial1.readStringUntil('\n');
    texto.trim();
    if (texto.substring(0,1) == "0") {
      digitalWrite(led1, LOW);
    }else {
      digitalWrite(led1, HIGH);
      anterior2 = atual;
    }
    if (texto.substring(2) == "0") {
      digitalWrite(led2, LOW);
    }else {
      digitalWrite(led2, HIGH);
      anterior2 = atual;
    }
  }
}
