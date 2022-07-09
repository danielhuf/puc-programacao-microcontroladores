#include <AFMotor.h>

#define VEL 160

int sensorOtico = A11;
int sensorOtico2 = A12;

unsigned long instanteAnterior = 0;
unsigned long instanteAtual = 0;

AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  Serial1.begin(9600);
  Serial1.setTimeout(10);

  pinMode(sensorOtico, INPUT);
  pinMode(sensorOtico2, INPUT);
}

void loop() {
  instanteAtual = millis();
  if (instanteAtual >= instanteAnterior + 100){
    Serial.println(String(digitalRead(sensorOtico))+" " +String(digitalRead(sensorOtico2)));
    Serial1.println(String(digitalRead(sensorOtico))+" " +String(digitalRead(sensorOtico2)));
    instanteAnterior = instanteAtual;
  }
  
  if (Serial1.available() > 0) {
    String texto = Serial1.readStringUntil('\n');
    texto.trim();
    if (texto == "frente") {
      frente();
    }
    else if (texto == "tras") {
      tras();
    }
    else if (texto == "direita") {
      direita();
    }
    else if (texto == "esquerda") {
      esquerda();
    }
    else if (texto == "parar") {
      parar();
    }
  }
}

void frente() {
  motor3.run(FORWARD);
  motor3.setSpeed(VEL);
  motor4.run(FORWARD);
  motor4.setSpeed(VEL);
}

void tras() {
  motor3.run(BACKWARD);
  motor3.setSpeed(VEL);
  motor4.run(BACKWARD);
  motor4.setSpeed(VEL);
}

void esquerda() {
  motor3.run(RELEASE);
  motor4.run(FORWARD);
  motor4.setSpeed(VEL);
}

void direita() {
  motor4.run(RELEASE);
  motor3.run(FORWARD);
  motor3.setSpeed(VEL);
}

void parar() {
  motor4.run(RELEASE);
  motor3.run(RELEASE);
}
